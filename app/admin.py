from flask import Blueprint, jsonify, current_app, request, session
from flask_login import login_required,current_user
from app.forms import RegistrationForm, UserUpdate
from app.models import Users,Product
from app.extensions import db


admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin.route('/status')
@login_required
def status():
    return jsonify({ "message": "API Operational for admin" }),200

@admin.route('/users', methods=['GET'])
@login_required
def view_users():
    adminOnly()

    userList = []
    users = Users.query.all()
    if len(users) != 0:
        for user in users:
            userList.append(
                {
                    "id" : user.id,
                    "firstName" : user.first_name,
                    "lastName" : user.last_name,
                    "role" : user.role,
                    "joined" : user.created_at,
                    "updated" : user.updated_at
                }
            )
        return jsonify({'result':userList}),200
    else:
        return jsonify({"result": "No Users available"}),404


@admin.route('/users/<userID>', methods=['GET','POST'])
@login_required
def view_or_edit_user_details(userID):
    """_summary_
    Examine the details of a user, this includes the functionality to change the user from a 
    regular user to an admin
    Args:
        userID (_type_): _description_
    """

    adminOnly()
    form = UserUpdate()
    user = Users.query.filter_by(id = userID).first()
    if request.method =='POST' and form.validate_on_submit(): 
        firstName =  form.firstName.data
        lastName =  form.lastName.data
        email= form.email.data
        role = form.role.data

        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.role = role

        db.session.commit()
        return jsonify({
            'result':'Successfully updated User'
        }),200


    if user is not None:
            result = {
                'firstName': user.firstName,
                'lastName' : user.lastName,
                'email': user.email
            }    
            return jsonify(result),200
    else:
        return jsonify({"result":"User not found"}),404



@admin.route('/users/<userID>', methods=['DELETE'])
@login_required
def delete_user(userID):
    """_summary_
        This could be nested in the edit view
        This to ensure that it is difficult to remove a user by accident
    Args:
        userID (_type_): _description_
    """
    adminOnly()
    pass



@admin.route('/product/', methods=['GET','POST'])
@login_required
def createProduct():
    adminOnly()
    pass


@admin.route('/product/<productID>', methods=['GET','POST'])
@login_required
def updateProductDetails(product):
    adminOnly()
    pass


@admin.route('/product/<productID>', methods=['DELETE'])
@login_required
def deleteProduct(productID):
    adminOnly()
    pass

@admin.route('/orders/', methods=['GET'])
@login_required
def viewOrders():
    adminOnly()
    pass

@admin.route('/orders/<orderID>', methods=['GET'])
@login_required
def order_details(orderID):
    adminOnly()
    pass

@admin.route('/orders/<orderID>', methods=['GET','POST'])
@login_required
def edit_order(orderID):
    adminOnly()
    pass



#------------------------------------------------------
# Helper functions

def adminOnly():
    if current_user.role != 'Admin':
        return jsonify({
            "error":"Unauthorised Access, Administrator role required"
        }),401