from fastapi import FastAPI
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

app = FastAPI()

@app.get("/users")
def get_users():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 'List of users from PostgreSQL';")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"message": result[0]}
    except Exception as e:
        return {"error": str(e)}
