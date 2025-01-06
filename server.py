from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import mysql.connector

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "motor_shop"
}

# Initialize FastAPI app
app = FastAPI()

class Motor(BaseModel):
    id: int = None  
    name: str
    brand: str
    category: str
    engine_capacity: int
    year_of_production: int
    price: float

class MotorCreate(BaseModel):
    name: str
    brand: str
    category: str
    engine_capacity: int
    year_of_production: int
    price: float

class Accessory(BaseModel):
    id: int = None 
    name: str
    type: str
    description: str
    price: float

class AccessoryCreate(BaseModel):
    name: str
    type: str
    description: str
    price: float

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.post("/motors", response_model=Motor)
def create_motor(motor: MotorCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        INSERT INTO motors (name, brand, category, engine_capacity, year_of_production, price)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        motor.name, motor.brand, motor.category,
        motor.engine_capacity, motor.year_of_production, motor.price
    ))
    connection.commit()
    motor_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**motor.dict(), "id": motor_id}

@app.get("/motors", response_model=List[Motor])
def get_all_motors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM motors"
    cursor.execute(query)
    motors = cursor.fetchall()
    cursor.close()
    connection.close()
    return motors

@app.get("/motors/{motor_id}", response_model=Motor)
def get_motor(motor_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM motors WHERE id = %s"
    cursor.execute(query, (motor_id,))
    motor = cursor.fetchone()
    cursor.close()
    connection.close()
    if not motor:
        raise HTTPException(status_code=404, detail="Motor not found")
    return motor

@app.put("/motors/{motor_id}", response_model=Motor)
def update_motor(motor_id: int, motor: MotorCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        UPDATE motors
        SET name = %s, brand = %s, category = %s,
            engine_capacity = %s, year_of_production = %s, price = %s
        WHERE id = %s
    """
    cursor.execute(query, (
        motor.name, motor.brand, motor.category,
        motor.engine_capacity, motor.year_of_production, motor.price, motor_id
    ))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Motor not found")
    cursor.close()
    connection.close()
    return {**motor.dict(), "id": motor_id}

@app.delete("/motors/{motor_id}")
def delete_motor(motor_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM motors WHERE id = %s"
    cursor.execute(query, (motor_id,))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Motor not found")
    cursor.close()
    connection.close()
    return {"message": "Motor deleted successfully"}

@app.post("/accessories", response_model=Accessory)
def create_accessory(accessory: AccessoryCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        INSERT INTO accessories (name, type, description, price)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        accessory.name, accessory.type, accessory.description, accessory.price
    ))
    connection.commit()
    accessory_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {**accessory.dict(), "id": accessory_id}

@app.get("/accessories", response_model=List[Accessory])
def get_all_accessories():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM accessories"
    cursor.execute(query)
    accessories = cursor.fetchall()
    cursor.close()
    connection.close()
    return accessories

@app.get("/accessories/{accessory_id}", response_model=Accessory)
def get_accessory(accessory_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM accessories WHERE id = %s"
    cursor.execute(query, (accessory_id,))
    accessory = cursor.fetchone()
    cursor.close()
    connection.close()
    if not accessory:
        raise HTTPException(status_code=404, detail="Accessory not found")
    return accessory

@app.put("/accessories/{accessory_id}", response_model=Accessory)
def update_accessory(accessory_id: int, accessory: AccessoryCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        UPDATE accessories
        SET name = %s, type = %s, description = %s, price = %s
        WHERE id = %s
    """
    cursor.execute(query, (
        accessory.name, accessory.type, accessory.description, accessory.price, accessory_id
    ))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Accessory not found")
    cursor.close()
    connection.close()
    return {**accessory.dict(), "id": accessory_id}

@app.delete("/accessories/{accessory_id}")
def delete_accessory(accessory_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "DELETE FROM accessories WHERE id = %s"
    cursor.execute(query, (accessory_id,))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Accessory not found")
    cursor.close()
    connection.close()
    return {"message": "Accessory deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
