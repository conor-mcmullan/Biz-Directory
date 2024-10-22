from bson import ObjectId
from models.review import Review
from models.business import Business
from pymongo.errors import PyMongoError
from mongo.mongo_connection import MongoConnection
from utils.sanitise import sanitize_string

class MongoCRUD:
    def __init__(self, mongo_connection: MongoConnection = None):
        if mongo_connection:
            self.db = mongo_connection.get_db()
        else:
            self.db = MongoConnection().get_db()

    def calculate_overall_rating(self, reviews: list) -> float:
        """Calculate the overall rating from a list of Review objects."""
        if not reviews:
            return 0.0
        total_rating = sum(review.rating for review in reviews)
        return total_rating / len(reviews)

    def register_business(self, business_data: dict):
        # Check if the businessID is provided and valid, else generate a new ObjectId
        if "businessID" in business_data:
            try:
                business_data['businessID'] = ObjectId(business_data['businessID'])  # Convert to ObjectId
            except Exception:
                raise ValueError("Provided businessID is not a valid ObjectId.")
        else:
            business_data['businessID'] = ObjectId()  # Generate a new ObjectId

        # Use sanitized business name for the collection
        collection_name = f"business_{sanitize_string(business_data['name'])}"
        business_collection = self.db[collection_name]

        # Check if the business already has a collection
        existing_business = self.db.list_collection_names(filter={"name": collection_name})

        if existing_business:
            raise ValueError(f"Business with the name '{business_data['name']}' already exists.")

        # Handle the reviews in business_data
        reviews = []
        if "reviews" in business_data:
            for review in business_data["reviews"]:
                if "reviewID" in review:
                    try:
                        review["reviewID"] = ObjectId(review["reviewID"])  # Convert to ObjectId if valid
                    except Exception:
                        raise ValueError("Provided reviewID is not a valid ObjectId.")
                else:
                    review["reviewID"] = ObjectId()  # Generate a new reviewID

                review_model = Review(**review)
                reviews.append(review_model)

            business_data['reviews'] = reviews

        # Calculate the overall rating based on reviews
        business_data['overallRating'] = self.calculate_overall_rating(reviews)

        # Create a Business instance
        new_business = Business(**business_data)

        # Insert into the business-specific collection
        try:
            business_collection.insert_one(new_business.dict())
        except PyMongoError as e:
            raise PyMongoError(f"Database Insertion Error: {e}")

        return new_business

    def add_review_to_business(self, business_name: str, review_data: dict):
        """Add or update a review for the business and recalculate the overall rating."""
        collection_name = f"business_{sanitize_string(business_name)}"
        business_collection = self.db[collection_name]

        # Check if the business exists
        business_data = business_collection.find_one({"name": business_name})
        if not business_data:
            raise ValueError(f"Business with the name '{business_name}' does not exist.")

        # Initialize reviewID and check if it exists
        review_id = review_data.get("reviewID")
        
        if review_id:
            # Check if the reviewID exists in the current reviews
            existing_review = next((review for review in business_data.get("reviews", []) if review["reviewID"] == ObjectId(review_id)), None)
            
            if existing_review:
                # If the review already exists, update it with the new data
                existing_review.update(review_data)
            else:
                # If the review does not exist, generate a new ObjectId
                review_data["reviewID"] = ObjectId()
        else:
            # If no reviewID provided, generate a new ObjectId
            review_data["reviewID"] = ObjectId()

        # Create a Review instance
        review_model = Review(**review_data)

        # Append or update the review in the business's reviews list
        if "reviews" not in business_data:
            business_data["reviews"] = []
        
        # If the review was newly created, append it; otherwise, it's already updated
        if not existing_review:
            business_data["reviews"].append(review_model)

        # Calculate the new overall rating based on updated reviews
        business_data['overallRating'] = self.calculate_overall_rating(business_data["reviews"])

        # Update the business document
        try:
            business_collection.update_one({"name": business_name}, {"$set": business_data})
        except PyMongoError as e:
            raise PyMongoError(f"Database Update Error: {e}")

        return business_data


    def get_business_by_name(self, business_name: str):
        """ Retrieve a business by its name """
        # Sanitize the business name before using it as a collection name
        collection_name = f"business_{sanitize_string(business_name)}"
        
        # Access the business-specific collection
        business_collection = self.db[collection_name]

        # Find the business data (assuming you store some basic business information in the collection itself)
        business_data = business_collection.find_one()
        
        if not business_data:
            raise ValueError(f"Business with name '{business_name}' not found.")
        
        return Business(**business_data)
