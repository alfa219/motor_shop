from flask import Flask, jsonify, request, abort
from flask_restx import Api, Resource, fields
import mysql.connector

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "motor_shop"
}

# Initialize Flask app and Api
app = Flask(__name__)
api = Api(app, title="Motor Shop API", description="API Documentation for Motor Shop", version="1.0")

# Namespaces for better organization
motor_ns = api.namespace("motors", description="Motor operations")
accessory_ns = api.namespace("accessories", description="Accessory operations")

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Swagger Models
motor_model = api.model("Motor", {
    "name": fields.String(required=True, description="The name of the motor"),
    "brand": fields.String(required=True, description="The brand of the motor"),
    "category": fields.String(required=True, description="The category of the motor"),
    "engine_capacity": fields.String(required=True, description="The engine capacity of the motor"),
    "year_of_production": fields.Integer(required=True, description="The year of production of the motor"),
    "price": fields.Float(required=True, description="The price of the motor")
})

accessory_model = api.model("Accessory", {
    "name": fields.String(required=True, description="The name of the accessory"),
    "type": fields.String(required=True, description="The type of the accessory"),
    "description": fields.String(required=True, description="The description of the accessory"),
    "price": fields.Float(required=True, description="The price of the accessory")
})

# Motor Endpoints
@motor_ns.route("/")
class MotorList(Resource):
    @motor_ns.marshal_list_with(motor_model)
    def get(self):
        """Get all motors"""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM motors")
        motors = cursor.fetchall()
        cursor.close()
        connection.close()
        return motors

    @motor_ns.expect(motor_model)
    def post(self):
        """Create a new motor"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = (
            "INSERT INTO motors (name, brand, category, engine_capacity, year_of_production, price) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (
            data["name"], data["brand"], data["category"],
            data["engine_capacity"], data["year_of_production"], data["price"]
        ))
        connection.commit()
        motor_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {**data, "id": motor_id}, 201

@motor_ns.route("/<int:motor_id>")
class Motor(Resource):
    def get(self, motor_id):
        """Get a motor by ID"""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM motors WHERE id = %s", (motor_id,))
        motor = cursor.fetchone()
        cursor.close()
        connection.close()
        if not motor:
            abort(404, "Motor not found")
        return motor

    @motor_ns.expect(motor_model)
    def put(self, motor_id):
        """Update a motor"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = (
            "UPDATE motors SET name = %s, brand = %s, category = %s, "
            "engine_capacity = %s, year_of_production = %s, price = %s WHERE id = %s"
        )
        cursor.execute(query, (
            data["name"], data["brand"], data["category"],
            data["engine_capacity"], data["year_of_production"], data["price"], motor_id
        ))
        connection.commit()
        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            abort(404, "Motor not found")
        cursor.close()
        connection.close()
        return {**data, "id": motor_id}

    def delete(self, motor_id):
        """Delete a motor"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM motors WHERE id = %s", (motor_id,))
        connection.commit()
        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            abort(404, "Motor not found")
        cursor.close()
        connection.close()
        return {"message": "Motor deleted successfully"}

# Accessory Endpoints
@accessory_ns.route("/")
class AccessoryList(Resource):
    @accessory_ns.marshal_list_with(accessory_model)
    def get(self):
        """Get all accessories"""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accessories")
        accessories = cursor.fetchall()
        cursor.close()
        connection.close()
        return accessories

    @accessory_ns.expect(accessory_model)
    def post(self):
        """Create a new accessory"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = (
            "INSERT INTO accessories (name, type, description, price) "
            "VALUES (%s, %s, %s, %s)"
        )
        cursor.execute(query, (
            data["name"], data["type"], data["description"], data["price"]
        ))
        connection.commit()
        accessory_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return {**data, "id": accessory_id}, 201

@accessory_ns.route("/<int:accessory_id>")
class Accessory(Resource):
    def get(self, accessory_id):
        """Get an accessory by ID"""
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accessories WHERE id = %s", (accessory_id,))
        accessory = cursor.fetchone()
        cursor.close()
        connection.close()
        if not accessory:
            abort(404, "Accessory not found")
        return accessory

    @accessory_ns.expect(accessory_model)
    def put(self, accessory_id):
        """Update an accessory"""
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = (
            "UPDATE accessories SET name = %s, type = %s, description = %s, price = %s WHERE id = %s"
        )
        cursor.execute(query, (
            data["name"], data["type"], data["description"], data["price"], accessory_id
        ))
        connection.commit()
        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            abort(404, "Accessory not found")
        cursor.close()
        connection.close()
        return {**data, "id": accessory_id}

    def delete(self, accessory_id):
        """Delete an accessory"""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accessories WHERE id = %s", (accessory_id,))
        connection.commit()
        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            abort(404, "Accessory not found")
        cursor.close()
        connection.close()
        return {"message": "Accessory deleted successfully"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
