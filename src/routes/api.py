# routes/api.py

from flask import Blueprint, jsonify

# Create a Blueprint named 'api' with the URL prefix '/api'
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/data')
def get_data():
    """Returns a simple JSON response."""
    data = {'message': 'Hello from the API!', 'status': 'success'}
    return jsonify(data)

@api_blueprint.route('/status')
def get_status():
    """Returns the application status."""
    status = {'app_name': 'My Flask App', 'version': '1.0'}
    return jsonify(status)