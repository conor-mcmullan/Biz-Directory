from flask import Flask, jsonify, request
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from mongo_crud import MongoCRUD
from mongo_connection import MongoConnection

app = Flask(__name__)

@app.before_first_request
def initialize_db():
    try:
        # Establish the connection once when the app starts
        mongo_conn = MongoConnection().connect(uri="mongodb://localhost:27017/biz_directory")
        # Initialize CRUD operations class with the connected database
        global mongo_crud
        mongo_crud = MongoCRUD(mongo_conn)  # Pass the connection object into MongoCRUD
    except ConnectionError as e:
        print(f"Database connection failed: {str(e)}")

@app.route('/register_business', methods=['POST'])
def register_business():
    try:
        business_data = request.json
        new_business = mongo_crud.register_business(business_data)
        return jsonify(new_business.dict()), 201
    except (ValueError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

@app.route('/get_business/<string:business_name>', methods=['GET'])
def get_business(business_name: str):
    try:
        # Retrieve the business by name
        business = mongo_crud.get_business_by_name(business_name)
        return jsonify(business.dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
