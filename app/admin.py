from flask import Blueprint, jsonify, current_app, session
from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin.route('/status')
@login_required
def status():
    return jsonify({ "message": "API Operational for admin" })

@admin.route('/users',method=['GET'])
@login_required
def view_users():
    pass

@admin.route('/users/<userID>',methods=['GET','POST'])
@login_required
def user_details(userID):
    pass

@admin.route('/product/',methods=['GET','POST'])
@login_required
def createProduct():
    pass


@admin.route('/product/<productID>',methods=['GET','POST'])
@login_required
def updateProductDetails(product):
    pass


@admin.route('/product/<productID>',method = ['DELETE'])
@login_required
def deleteProduct(productID):
    pass