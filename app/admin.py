import os
from flask import Blueprint, Config, jsonify, current_app, redirect, request, session, url_for
from flask_login import LoginManager, login_required,current_user
from app.forms import ProductForm, RegistrationForm, UpdateOrder, UserUpdate
from app.models import LineItems, Order, ProductStatus, Users,Product
from app import login_manager, app
# from app.extensions import db
from . import db
import os


from datetime import datetime
from werkzeug.utils import secure_filename


admin = Blueprint('admin', __name__, url_prefix='/api/v1/admin')
root_path = os.getcwd()
@admin.route('/status',methods=['GET'])
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

    if request.method == 'GET':
        if user is not None:
                result = {
                    'firstName': user.first_name,
                    'lastName' : user.last_name,
                    'email': user.email,
                    'id':user.id,
                    'role': user.role 
                }  
                #pre-populate the form
                form = UserUpdate(data = result)
                form_fields = []
                for field in form:
                    form_fields.append({
                        'label': field.label.text,
                        'type': field.widget.input_type,
                        'name': field.name,
                        'required': field.flags.required,
                        'value': field.data  # Include the prepopulated value
                    })
                return jsonify(form_fields),200  
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
def   createProduct():
    adminOnly()

    form = ProductForm()
    form.status_options.choices = [(option.value,option.name) for option in ProductStatus]
    
    if request.method =='POST':
        if form.validate_on_submit():
            name = form.name.data.strip()
            description = form.description.data.strip()
            price = form.price.data.strip()
            image = form.image.data
            status = form.status_options.data


            if image.filename == '':
                return jsonify({'error':'file name required'}),422

            imageName = secure_filename(image.filename.rstrip())

            # print(f'TIS IS THE OS PATH: {root_path}')
            # print(f'IMAGE NAME: {imageName}')
            upload_path = root_path+app.config['UPLOAD_FOLDER']

            image.save(upload_path +  imageName)
            # image.save(str(os.path.join(app.config.UPLOAD_FOLDER,imageName)))

            new_product = Product(
                name,
                description,
                price,
                imageName,
                ProductStatus(str(status)),
                current_user.get_id()
            )
            print("prod created")
            try:
                db.session.add(new_product)
                db.session.commit()
                return jsonify({
                    'result':f'Successfully added Product'
                    }),201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error":e}),500
        else:
            error={
                    "error": form_errors(form)
                }
            return jsonify(error),400
        


    if request.method == 'GET':
        form_fields = []
        for field in form:
            form_fields.append({
                'label': field.label.text,
                'name': field.name,
                'required': field.flags.required,
            })
        print(form_fields)
        return jsonify(form_fields),200
        
    
    


@admin.route('/product/<productID>', methods=['GET','POST'])
@login_required
def updateProductDetails(productID):
    adminOnly()
    
    prodToEdit = Product.query.get(productID)
    form = ProductForm()

    if request.method == "POST" and form.validate_on_submit():
        name= form.name.data.strip()
        description= form.description.data.strip()
        price= form.price.data.strip()
        image= form.image.data.strip().lower()
        status_options = form.status_options.data
        
        if image.filename == '':
            return jsonify({'error':'file name required'}),422

        new_image_name = secure_filename(image.filename.rstrip())

        # if a different Image is present, save it to the uploads folder, else continue
        if new_image_name == prodToEdit.image:
            prodToEdit.name = name
            prodToEdit.description = description
            prodToEdit.price = price
            prodToEdit.status = ProductStatus(str(status_options))
            
        else:
            prodToEdit.name = name
            prodToEdit.description = description
            prodToEdit.price = price
            prodToEdit.image = image
            prodToEdit.status = ProductStatus(str(status_options))

            image.save(str(os.path.join(Config.UPLOAD_FOLDER,new_image_name)))



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

            #Pre-populate form
            form = ProductForm(data = result) 

            form_fields = []
            for field in form:
                form_fields.append({
                    'label': field.label.text,
                    'type': field.widget.input_type,
                    'name': field.name,
                    'required': field.flags.required,
                    'value': field.data  # Include the prepopulated value
                })
            return jsonify(form_fields),200 

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
            items = LineItems.query.filter_by(order_id = order.id).all()
            itemList = []
            for item in items:
                itemList.append({
                    'product_name': Product.query.filter_by(id = item.product_id).first().name,
                    'quantity': item.quantity
                })
            orderList.append(
                {
                    "id": order.id,
                    'address':order.billing_address,
                    'total':order.total_amount,
                    'status':order.get_status(),
                    'items':itemList
                }
            )
        return jsonify({'result':orderList}),200
    else:
         return jsonify({"result": "No orders available"}),204


@admin.route('/orders/<orderID>', methods=['GET','POST'])
@login_required
def order_details(orderID):
    adminOnly()

    order = Order.query.filter(Order.id == orderID).first()
    form = UpdateOrder(status_options = order.status.value) # pre-selects the status for the drop down option
    
    if request.method == 'POST':
        #---------The implementation of Stripe here --------
        pass
    
    if request.method == 'GET':
        if order is not None:

            items = LineItems.query.filter_by(order_id = order.id)
            customer =  Users.query.filter_by(id = order.user_id).first()
            itemList = []
            for item in items:
                itemList.append({
                    'product_name': Product.query.filter_by(id = item.product_id).first().name,
                    'quantity': item.quantity
                })


            orderDetails = {
            "id": order.id,
            "customer_name": f"{customer.first_name} {customer.last_name}".title(),
            "customer_email": f'{customer.email}',
            'billing_address': order.billing_address,
            'total_amount': order.total_amount,
            'status':order.get_status(),
            'items':itemList
            }
            
            return jsonify({'result':orderDetails}),200
        else:
            return jsonify({"result": "No orders available"}),204








#------------------------------------------------------
# Helper functions

def adminOnly():
    if current_user.role != 'admin':
        return jsonify({
            "error":"Unauthorised Access, Administrator role required"
        }),401
    

@admin.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
