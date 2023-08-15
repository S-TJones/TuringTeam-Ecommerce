from flask import Blueprint, jsonify, current_app, session

customer = Blueprint('customer', __name__, url_prefix='/api/v1/customer')

@customer.route('/status')
def status():
    return jsonify({ "message": "API Operational for  cx" })