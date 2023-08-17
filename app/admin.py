from flask import Blueprint, jsonify, current_app, session
from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin.route('/status')
@login_required
def status():
    return jsonify({ "message": "API Operational for admin" })

@admin.route('/users', methods=['GET'])
@login_required
def view_users():
    pass

@admin.route('/users/<userID>', methods=['GET'])
@login_required
def view_user_details(userID):
    pass

@admin.route('/users/<userID>', methods=['GET','POST'])
@login_required
def edit_user_details(userID):
    """_summary_
    This includes the functionality to change the user from a 
    regular user to an admin
    Args:
        userID (_type_): _description_
    """
    pass

@admin.route('/users/<userID>', methods=['DELETE'])
@login_required
def delete_user(userID):
    """_summary_
        This could be nested in the edit view
        This to ensure that it is difficult to remove a user by accident
    Args:
        userID (_type_): _description_
    """
    pass



@admin.route('/product/', methods=['GET','POST'])
@login_required
def createProduct():
    pass


@admin.route('/product/<productID>', methods=['GET','POST'])
@login_required
def updateProductDetails(product):
    pass


@admin.route('/product/<productID>', methods=['DELETE'])
@login_required
def deleteProduct(productID):
    pass

@admin.route('/orders/', methods=['GET'])
@login_required
def viewOrders():
    pass

@admin.route('/orders/<orderID>', methods=['GET'])
@login_required
def order_details(orderID):
    pass

@admin.route('/orders/<orderID>', methods=['GET','POST'])
@login_required
def edit_order(orderID):
    pass
