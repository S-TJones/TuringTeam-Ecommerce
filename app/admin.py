from flask import Blueprint, jsonify, current_app, session

admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin.route('/status')
def status():
    return jsonify({ "message": "API Operational for admin" })