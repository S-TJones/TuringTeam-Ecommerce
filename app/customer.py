from flask import Blueprint, jsonify, current_app, session
from flask_login import login_required


customer = Blueprint('customer', __name__, url_prefix='/api/v1/customer')

@customer.route('/status')
def status():
    return jsonify({ "message": "API Operational for  cx" })

@customer.route('/orders/', methods=['GET'])
@login_required
def viewOrders():
    pass

@customer.route('/orders/<orderID>', methods=['GET'])
@login_required
def order_details(orderID):
    pass

@customer.route('/orders/<orderID>', methods=['GET','POST'])
@login_required
def edit_order(orderID):
    pass


@customer.route('/cart', methods=['GET'])
@login_required
def view_cart():
    # use c_uid = current_user.get_id() to get the user ID
    pass


@customer.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    pass