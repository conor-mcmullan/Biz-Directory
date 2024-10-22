# app/__init__.py

from flask import Flask
from mongo.mongo_db_initialiser import initialize, DatabaseConnectionError
import sys

# Initialize Flask app
app = Flask(__name__)

try:
    # Call to initialize the database connection
    initialize()
except DatabaseConnectionError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Import and register blueprints after DB initialization
from api.routes.health import health_bp
from api.routes.business import business_bp
from api.routes.reviews import review_bp

# Register blueprints with the Flask app
app.register_blueprint(health_bp, url_prefix="/health")
app.register_blueprint(business_bp, url_prefix="/business")
app.register_blueprint(review_bp, url_prefix="/review")

