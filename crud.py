# crud.py

from pymongo import MongoClient
from bson import ObjectId
from models import BusinessModel, ReviewModel


# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
businesses_collection = db['businesses']

def register_business(business_data: dict):
    # Check if the business name already exists
    existing_business = businesses_collection.find_one({"name": business_data["name"]})

    if existing_business:
        raise ValueError(f"Business with the name '{business_data['name']}' already exists.")

    # Check if businessID is provided and valid, else generate a new ObjectId
    if "businessID" in business_data:
        try:
            business_data['businessID'] = ObjectId(business_data['businessID'])  # Convert to ObjectId
        except Exception:
            raise ValueError("Provided businessID is not a valid ObjectId.")
    else:
        business_data['businessID'] = ObjectId()  # Generate a new ObjectId

    # Handle the reviews in business_data
    if "reviews" in business_data:
        reviews = []
        for review in business_data["reviews"]:
            if "reviewID" in review:
                try:
                    review["reviewID"] = ObjectId(review["reviewID"])  # Convert to ObjectId if valid
                except Exception:
                    raise ValueError("Provided reviewID is not a valid ObjectId.")
            else:
                review["reviewID"] = ObjectId()  # Generate a new reviewID

            review_model = ReviewModel(**review)
            reviews.append(review_model)

        business_data['reviews'] = reviews

    new_business = BusinessModel(**business_data)
    businesses_collection.insert_one(new_business.dict())

    return new_business
