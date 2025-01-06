from flask import Flask, jsonify, request, abort
import mysql.connector

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "motor_shop"
}

# Initialize Flask app
app = Flask(__name__)

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/motors", methods=["POST"])
def create_motor():
    data = request.json
    required_fields = ["name", "brand", "category", "engine_capacity", "year_of_production", "price"]
    
    if not all(field in data for field in required_fields):
        abort(400, "Missing required fields")

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
    return jsonify({**data, "id": motor_id}), 201

@app.route("/motors", methods=["GET"])
def get_all_motors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM motors")
    motors = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(motors)

@app.route("/motors/<int:motor_id>", methods=["GET"])
def get_motor(motor_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM motors WHERE id = %s", (motor_id,))
    motor = cursor.fetchone()
    cursor.close()
    connection.close()
    if not motor:
        abort(404, "Motor not found")
    return jsonify(motor)

@app.route("/motors/<int:motor_id>", methods=["PUT"])
def update_motor(motor_id):
    data = request.json
    required_fields = ["name", "brand", "category", "engine_capacity", "year_of_production", "price"]
    
    if not all(field in data for field in required_fields):
        abort(400, "Missing required fields")

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
    return jsonify({**data, "id": motor_id})

@app.route("/motors/<int:motor_id>", methods=["DELETE"])
def delete_motor(motor_id):
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
    return jsonify({"message": "Motor deleted successfully"})

@app.route("/accessories", methods=["POST"])
def create_accessory():
    data = request.json
    required_fields = ["name", "type", "description", "price"]

    if not all(field in data for field in required_fields):
        abort(400, "Missing required fields")

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
    return jsonify({**data, "id": accessory_id}), 201

@app.route("/accessories", methods=["GET"])
def get_all_accessories():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accessories")
    accessories = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(accessories)

@app.route("/accessories/<int:accessory_id>", methods=["GET"])
def get_accessory(accessory_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM accessories WHERE id = %s", (accessory_id,))
    accessory = cursor.fetchone()
    cursor.close()
    connection.close()
    if not accessory:
        abort(404, "Accessory not found")
    return jsonify(accessory)

@app.route("/accessories/<int:accessory_id>", methods=["PUT"])
def update_accessory(accessory_id):
    data = request.json
    required_fields = ["name", "type", "description", "price"]

    if not all(field in data for field in required_fields):
        abort(400, "Missing required fields")

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
    return jsonify({**data, "id": accessory_id})

@app.route("/accessories/<int:accessory_id>", methods=["DELETE"])
def delete_accessory(accessory_id):
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
    return jsonify({"message": "Accessory deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
