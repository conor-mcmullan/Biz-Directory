from flask import Flask, jsonify, request
from app.models import BusinessModel, ReviewModel
from app.crud import create_review, update_review, check_review_exists
from pydantic import ValidationError
from bson.objectid import ObjectId

app = Flask(__name__)

# Replace with your actual MongoDB connection string if necessary
app.config["MONGO_URI"] = "mongodb://localhost:27017/bizdirectory"

mongo = PyMongo(app)


@app.route('/business', methods=['POST'])
def add_business():
    try:
        data = request.json
        business = BusinessModel(**data)
        mongo.db.business.insert_one(business.dict())
        return jsonify({"message": "Business created"}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@app.route('/business/<string:business_id>/review', methods=['POST'])
def add_review(business_id):
    try:
        data = request.json
        review = ReviewModel(**data)
        
        # Check if this user has already reviewed the business
        if check_review_exists(mongo.db, business_id, review.reviewerEmail):
            return jsonify({"error": "You have already reviewed this business"}), 400
        
        # Proceed to add the review
        result = create_review(mongo.db, business_id, review.dict())
        if result:
            return jsonify({"message": "Review added"}), 201
        return jsonify({"error": "Business not found"}), 404
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@app.route('/business/<string:business_id>/review/<string:reviewer_email>', methods=['PUT'])
def edit_review(business_id, reviewer_email):
    data = request.json
    result = update_review(mongo.db, business_id, reviewer_email, data)
    if result:
        return jsonify({"message": "Review updated"}), 200
    return jsonify({"error": "Review not found"}), 404
