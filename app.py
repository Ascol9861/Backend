from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import OperationalError
from flask_cors import CORS

# PostgreSQL database credentials
DB_HOST = '34.30.91.14'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'root'

app = Flask(__name__)
CORS(app)

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"Unable to connect to PostgreSQL: {e}")
    return connection

def create_user(name, email):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error inserting user: {e}")
            return False
    else:
        return False

def get_users():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return users
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
    else:
        return []

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    email = request.form.get('email')
    if name and email:
        if create_user(name, email):
            return jsonify({'message': 'User added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to add user'}), 500
    else:
        return jsonify({'error': 'Name and email are required'}), 400

@app.route('/users', methods=['GET'])
def get_all_users():
    users = get_users()
    return jsonify({'users': users})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
