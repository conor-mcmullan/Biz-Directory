# app/routes/reviews.py

from flask import Blueprint, jsonify, request
from pymongo.errors import PyMongoError
from pydantic import ValidationError
from mongo.mongo_db_initialiser import mongo_crud

# Create the review blueprint
review_bp = Blueprint('review', __name__)

@review_bp.route('/add/<string:business_name>', methods=['POST'])
def add_review(business_name: str):
    try:
        review_data = request.json
        updated_business = mongo_crud.add_review_to_business(business_name, review_data)
        return jsonify(updated_business.dict()), 201
    except (ValueError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    except PyMongoError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
