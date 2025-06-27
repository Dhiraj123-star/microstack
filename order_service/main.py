from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Order
from schemas import OrderCreate, OrderUpdate, OrderOut
from dotenv import load_dotenv
import os
import time
from sqlalchemy.exc import OperationalError
import httpx

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Retry mechanism for DB connection
MAX_RETRIES = 20
DELAY = 2

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ OrderService: Database connection successful.")
        break
    except OperationalError as e:
        print(f"🔁 OrderService: Retry ({attempt}/{MAX_RETRIES}) - DB connection failed: {e}")
        time.sleep(DELAY)
else:
    raise Exception("❌ OrderService: Could not connect to the database after multiple retries.")

app = FastAPI(root_path="/orders")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"message": "List of orders from PostgreSQL"}

@app.get("/all", response_model=list[OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Validate user_id from user_service
    try:
        response = httpx.get(f"http://user_service:8000/users/{order.user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid user_id. User does not exist.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"User service unreachable: {str(e)}")

    new_order = Order(user_id=order.user_id, item_name=order.item_name, quantity=order.quantity)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order_data.item_name:
        order.item_name = order_data.item_name
    if order_data.quantity:
        order.quantity = order_data.quantity
    if order_data.status:
        order.status = order_data.status
    db.commit()
    db.refresh(order)
    return order

@app.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted"}
