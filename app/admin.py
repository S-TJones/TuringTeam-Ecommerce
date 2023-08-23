import os
from flask import Blueprint, Config, jsonify, current_app, redirect, request, session, url_for
from flask_login import login_required,current_user
from app.forms import ProductForm, RegistrationForm, UserUpdate
from app.models import Order, ProductStatus, Users,Product
from app.extensions import db
from werkzeug.utils import secure_filename


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

        user.first_name = firstName.strip().lower()
        user.last_name = lastName.strip().lower()
        user.email = email.strip().lower()
        user.role = role.strip().lower()

        try:
            db.session.commit()
            return jsonify({
                'result':'Successfully updated User'
                }),200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error":e}),500       

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
    invalidUser = Users.query.get(userID)
    if invalidUser is not None:
        fname,lname = invalidUser.first_name,invalidUser.last_name
        try:
            db.session.delete(invalidUser)
            db.session.commit()
            return jsonify({
                'result':f'Successfully removed {fname} {lname}'
                }),200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error":e}),500
        
    else:
        return jsonify({'result':"No user exists with that id"}),204


@admin.route('/product/', methods=['GET','POST'])
@login_required
def createProduct():
    adminOnly()

    form = ProductForm()
    form.status_options.choices = [(option.value,option.name) for option in ProductStatus]
    
    if request.method =='POST' and form.validate_on_submit():
        name = form.name.data.strip().lower()
        description = form.description.data.strip().lower()
        price = form.price.data.strip().lower()
        image = form.image.data.strip().lower()
        status = form.status_options.data

        if image.filename == '':
            return jsonify({'error':'file name required'}),422
        
        imageName = secure_filename(image.filename.rstrip())

        image.save(str(os.path.join(Config.UPLOAD_FOLDER,imageName)))

        new_product = Product(
            name,
            description,
            price,
            image,
            ProductStatus(str(status))
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            return jsonify({
                'result':f'Successfully added Product'
                }),200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error":e}),500
        
    return redirect(url_for('main.products'))
    
    


@admin.route('/product/<productID>', methods=['GET','POST'])
@login_required
def updateProductDetails(productID):
    adminOnly()
    
    prodToEdit = Product.query.get(productID)
    form = ProductForm()

    if request.method == "POST" and form.validate_on_submit():
        name= form.name.data.strip().lower()
        description= form.description.data.strip().lower()
        price= form.price.data.strip().lower()
        image= form.image.data.strip().lower()
        status_options = form.status_options.data

        prodToEdit.name = name
        prodToEdit.description = description
        prodToEdit.price = price
        prodToEdit.image = image
        prodToEdit.status = ProductStatus(str(status_options))

        try:
            db.session.commit()
            return jsonify({
                'result':f'Successfully Edited Product'
                }),200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error":e}),500
        

    if request.method == "GET":
        if prodToEdit is not None:
            result = {
                'name': prodToEdit.name,
                'description': prodToEdit.description,
                'price': prodToEdit.price,
                'image': prodToEdit.image,
                'status': prodToEdit.status,
                'statusOPtions': [(option.value,option.name) for option in  ProductStatus] 
            }

            return jsonify(result),200
        else:
            return jsonify({'result':'No products by that identifier'}),404


@admin.route('/product/<productID>', methods=['DELETE'])
@login_required
def deleteProduct(productID):
    adminOnly()
    if request.method == 'DELETE':
        prodToDelete = Product.query.get(productID)
        if prodToDelete is not None:
            try:
                db.session.delete(prodToDelete)
                db.session.commit()
                return jsonify({
                    'result':f'Successfully Deleted Product'
                    }),200
            except Exception as e:
                db.session.rollback()
                return jsonify({"error":e}),500

        

@admin.route('/orders/', methods=['GET'])
@login_required
def viewOrders():
    adminOnly()
    orders = Order.query.all()
    orderList = []
    if len(orders) != 0:
        for order in orders:
            result = {
                
            }


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
    if current_user.role != 'admin':
        return jsonify({
            "error":"Unauthorised Access, Administrator role required"
        }),401