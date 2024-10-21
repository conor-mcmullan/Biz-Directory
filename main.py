# main.py

from datetime import datetime
from pprint import pprint

def main():
    # Example of registering a new business with reviews
    new_business_json = {
        "businessID": "60c72b2f4f1a2c001f8e4d2a",  # Optional: Use if you have a specific ID
        "name": "Best Coffee Shop",
        "address": "123 Coffee Lane, Brew City",
        "contactEmail": "info@bestcoffeeshop.com",
        "contactPhone": "+1234567890",
        "businessType": "Cafe",  # New field for business type
        "reviews": [
            {
                "reviewID": "60c72b2f4f1a2c001f8e4d3a",  # Optional: Use if you have a specific review ID
                "rating": 4.5,
                "description": "Great coffee and friendly service!",
                "reviewerEmail": "john@example.com",
                "reviewerName": "John Doe",
                "review_ts": datetime.now()  # This should be a valid datetime
            },
            {
                "rating": 5.0,
                "description": "Best coffee I’ve ever had!",
                "reviewerEmail": "jane@example.com",
                "reviewerName": "Jane Smith",
                "review_ts": datetime.now()  # This should be a valid datetime
            }
        ]
    }
    pprint(new_business_json)

if __name__ == "__main__":
    main()
