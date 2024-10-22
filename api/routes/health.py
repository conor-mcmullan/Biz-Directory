# app/routes/health.py

from flask import Blueprint, jsonify

# Create the business blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def register_business():
    return jsonify({'message': 'I am Healthy !'}), 200
