from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/check_db")
def check_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )
        if connection.is_connected():
            return {"status": "success"}
    except Error as e:
        return {"status": "miss", "error": str(e)}
    finally:
        if connection.is_connected():
            connection.close()

# Define a model for the incoming JSON data
class Record(BaseModel):
    id: str
    moji: str
    sansyou: str

@app.post("/insert_data")
def insert_data(record: Record):
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )

        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO users (id, moji, sansyou) 
                VALUES (%s, %s, %s)
            """
            values = (record.id, record.moji, record.sansyou)
            cursor.execute(insert_query, values)
            connection.commit()

            return {"status": "success", "user_id": cursor.lastrowid}
    except mysql.connector.Error as e:
        return {"status": "miss", "error": str(e)}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()