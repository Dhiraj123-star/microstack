from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User
from schemas import UserCreate, UserUpdate, UserOut
from dotenv import load_dotenv
import os
import time
from sqlalchemy.exc import OperationalError
import redis
import json

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Redis client
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Retry logic for database connection and metadata creation
MAX_RETRIES = 20
DELAY = 2

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Connected to the database and initialized schema.")
        break
    except OperationalError as e:
        print(f"⏳ Attempt {attempt}/{MAX_RETRIES} - Database not ready yet: {e}")
        time.sleep(DELAY)
else:
    raise Exception("❌ Could not connect to the database after multiple attempts.")

app = FastAPI(root_path="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"message": "List of users from PostgreSQL"}

# GET all users
@app.get("/all", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    cache_key = "users:all"
    cached = r.get(cache_key)
    if cached:
        print("📦 Serving /all from Redis cache")
        return json.loads(cached)

    users = db.query(User).all()
    result = [UserOut.from_orm(user).dict() for user in users]
    r.set(cache_key, json.dumps(result))
    return result

# POST create user
@app.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Invalidate Redis cache
    r.delete("users:all")
    return new_user

# GET user by ID
@app.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    cache_key = f"users:{user_id}"
    cached = r.get(cache_key)
    if cached:
        print(f"📦 Serving /{user_id} from Redis cache")
        return json.loads(cached)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    result = UserOut.from_orm(user).dict()
    r.set(cache_key, json.dumps(result))
    return result

# PUT update user
@app.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    db.commit()
    db.refresh(user)

    # Invalidate Redis cache
    r.delete("users:all")
    r.delete(f"users:{user_id}")
    return user

# DELETE user
@app.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

    # Invalidate Redis cache
    r.delete("users:all")
    r.delete(f"users:{user_id}")
    return {"detail": "User deleted"}
