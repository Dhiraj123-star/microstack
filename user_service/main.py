from fastapi import FastAPI
import redis
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

app = FastAPI()

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

@app.get("/orders")
def get_orders():
    try:
        cached = r.get("recent_order")
        if cached:
            return {"message": f"From Redis Cache: {cached.decode()}"}
        else:
            return {"message": "No recent orders in cache"}
    except Exception as e:
        return {"error": str(e)}
