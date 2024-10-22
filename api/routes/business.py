# app/routes/business.py

from flask import Blueprint, jsonify, request
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from mongo.mongo_db_initialiser import mongo_crud

# Create the business blueprint
business_bp = Blueprint('business', __name__)

@business_bp.route('/register', methods=['POST'])
def register_business():
    try:
        business_data = request.json
        new_business = mongo_crud.register_business(business_data)
        return jsonify(new_business.dict()), 201
    except (ValueError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500

@business_bp.route('/<string:business_name>', methods=['GET'])
def get_business(business_name: str):
    try:
        # Retrieve the business by name
        business = mongo_crud.get_business_by_name(business_name)
        return jsonify(business.dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
