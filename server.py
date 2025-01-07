from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import mysql.connector
from decimal import Decimal
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder  
api = Api(app, version="1.0", title="Motor Shop API", description="API untuk mengelola motor dan aksesori")

motor_ns = api.namespace("motors", description="Operasi motor")
accessory_ns = api.namespace("accessories", description="Operasi aksesori")

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "motor_shop"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

motor_model = motor_ns.model("Motor", {
    "id": fields.Integer(readOnly=True),
    "name": fields.String(required=True),
    "brand": fields.String(required=True),
    "category": fields.String(required=True),
    "engine_capacity": fields.Integer(required=True),
    "year_of_production": fields.Integer(required=True),
    "price": fields.Float(required=True),
})

accessory_model = accessory_ns.model("Accessory", {
    "id": fields.Integer(readOnly=True),
    "name": fields.String(required=True),
    "type": fields.String(required=True),
    "description": fields.String(required=True),
    "price": fields.Float(required=True),
})

@motor_ns.route("/")
class MotorList(Resource):
    @motor_ns.response(200, "Berhasil")
    def get(self):
        """Mengambil semua data motor"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM motors")
            motors = cursor.fetchall()
            cursor.close()
            connection.close()


            for motor in motors:
                for key, value in motor.items():
                    if isinstance(value, Decimal):
                        motor[key] = float(value)

            return motors, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @motor_ns.expect(motor_model, validate=True)
    @motor_ns.response(201, "Dibuat")
    def post(self):
        """Menambahkan motor baru"""
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO motors (name, brand, category, engine_capacity, year_of_production, price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["name"], data["brand"], data["category"],
                data["engine_capacity"], data["year_of_production"], data["price"]
            ))
            connection.commit()
            motor_id = cursor.lastrowid
            cursor.close()
            connection.close()
            data["id"] = motor_id
            return data, 201
        except Exception as e:
            return {"error": str(e)}, 500

@motor_ns.route("/<int:motor_id>")
class Motor(Resource):
    @motor_ns.response(200, "Berhasil")
    @motor_ns.response(404, "Motor tidak ditemukan")
    def get(self, motor_id):
        """Mengambil motor berdasarkan ID"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM motors WHERE id = %s", (motor_id,))
            motor = cursor.fetchone()
            cursor.close()
            connection.close()

            if motor is None:
                return {"message": "Motor tidak ditemukan"}, 404

            # Mengonversi Decimal ke float
            for key, value in motor.items():
                if isinstance(value, Decimal):
                    motor[key] = float(value)

            return motor, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @motor_ns.expect(motor_model, validate=True)
    @motor_ns.response(200, "Diperbarui")
    def put(self, motor_id):
        """Memperbarui data motor"""
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = """
                UPDATE motors
                SET name = %s, brand = %s, category = %s,
                    engine_capacity = %s, year_of_production = %s, price = %s
                WHERE id = %s
            """
            cursor.execute(query, (
                data["name"], data["brand"], data["category"],
                data["engine_capacity"], data["year_of_production"], data["price"], motor_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return {"message": "Motor tidak ditemukan"}, 404
            cursor.close()
            connection.close()
            data["id"] = motor_id
            return data, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @motor_ns.response(200, "Dihapus")
    @motor_ns.response(404, "Motor tidak ditemukan")
    def delete(self, motor_id):
        """Menghapus motor"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "DELETE FROM motors WHERE id = %s"
            cursor.execute(query, (motor_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return {"message": "Motor tidak ditemukan"}, 404
            cursor.close()
            connection.close()
            return {"message": "Motor berhasil dihapus"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


@accessory_ns.route("/")
class AccessoryList(Resource):
    @accessory_ns.response(200, "Berhasil")
    def get(self):
        """Mengambil semua data aksesori"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM accessories")
            accessories = cursor.fetchall()
            cursor.close()
            connection.close()

   
            for accessory in accessories:
                for key, value in accessory.items():
                    if isinstance(value, Decimal):
                        accessory[key] = float(value)

            return accessories, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @accessory_ns.expect(accessory_model, validate=True)
    @accessory_ns.response(201, "Dibuat")
    def post(self):
        """Menambahkan aksesori baru"""
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO accessories (name, type, description, price)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["name"], data["type"], data["description"], data["price"]
            ))
            connection.commit()
            accessory_id = cursor.lastrowid
            cursor.close()
            connection.close()
            data["id"] = accessory_id
            return data, 201
        except Exception as e:
            return {"error": str(e)}, 500

@accessory_ns.route("/<int:accessory_id>")
class Accessory(Resource):
    @accessory_ns.response(200, "Berhasil")
    @accessory_ns.response(404, "Aksesori tidak ditemukan")
    def get(self, accessory_id):
        """Mengambil aksesori berdasarkan ID"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM accessories WHERE id = %s", (accessory_id,))
            accessory = cursor.fetchone()
            cursor.close()
            connection.close()

            if accessory is None:
                return {"message": "Aksesori tidak ditemukan"}, 404

            for key, value in accessory.items():
                if isinstance(value, Decimal):
                    accessory[key] = float(value)

            return accessory, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @accessory_ns.expect(accessory_model, validate=True)
    @accessory_ns.response(200, "Diperbarui")
    def put(self, accessory_id):
        """Memperbarui data aksesori"""
        data = request.json
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = """
                UPDATE accessories
                SET name = %s, type = %s, description = %s, price = %s
                WHERE id = %s
            """
            cursor.execute(query, (
                data["name"], data["type"], data["description"], data["price"], accessory_id
            ))
            connection.commit()
            if cursor.rowcount == 0:
                return {"message": "Aksesori tidak ditemukan"}, 404
            cursor.close()
            connection.close()
            data["id"] = accessory_id
            return data, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @accessory_ns.response(200, "Dihapus")
    @accessory_ns.response(404, "Aksesori tidak ditemukan")
    def delete(self, accessory_id):
        """Menghapus aksesori"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "DELETE FROM accessories WHERE id = %s"
            cursor.execute(query, (accessory_id,))
            connection.commit()
            if cursor.rowcount == 0:
                return {"message": "Aksesori tidak ditemukan"}, 404
            cursor.close()
            connection.close()
            return {"message": "Aksesori berhasil dihapus"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
