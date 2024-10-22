# app/__init__.py

from flask import Flask
from mongo.mongo_db_initialiser import initialize

# Initialize Flask app
app = Flask(__name__)

# Call to initialize the database connection
initialize()

# Import and register blueprints after DB initialization
from api.routes.business import business_bp
from api.routes.reviews import review_bp

# Register blueprints with the Flask app
app.register_blueprint(business_bp, url_prefix="/business")
app.register_blueprint(review_bp, url_prefix="/review")

