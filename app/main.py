from flask import Blueprint, current_app, jsonify, render_template
from passlib.hash import sha256_crypt
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from flask_wtf.csrf import generate_csrf
from datetime import datetime
from app.forms import LoginForm,RegistrationForm
from app.models import Users,Product
from app import login_manager
from pprint import pprint
# from app.extensions import db
from . import db

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash




main = Blueprint('main', __name__,url_prefix='/api/v1')

@main.route('/products',methods=["GET"])
def products():
    productList = []
    products = Product.query.all()
    if len(products) !=0:
        for product in products:
            if product.status == 'Published':
                productList.append({
                    "id":product.id,
                    "name":product.name,
                    "description":product.description,
                    "price":product.price,
                    "price":product.price,
                    "image":product.image
                })

        return jsonify({'result':productList}),200
    
    else:
        return jsonify({"result":"No Products Available"}),200




@main.route("/login", methods=["POST",'GET'])
def login():
    """Visitor uses this to Authorise and Authenticate themselves"""

    if current_user is not None and current_user.is_authenticated:
        return jsonify({"result":"Successful Login",'user_id':current_user.get_id()}),200
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            email = form.email.data.strip().lower()
            password = form.password.data.strip()
            
            user = Users.query.filter_by(email = email).first()
       

            if user is not None and check_password_hash(user.password,password):

                login_user(user)
                return jsonify({"result":"Successful Login",'user_id':user.id}),200

            else:
                return jsonify({"result":"Login unsuccessful. Check credentials"}),401
    else:
        form_fields = []
        for field in form:
            form_fields.append({
                'label': field.label.text,
                'type': field.widget.input_type,
                'name': field.name,
                'required': field.flags.required,
            })
        response = jsonify(form_fields)
        response.headers['X-CSRF-Token'] = generate_csrf()
        return response
            
@main.route('/sign-up',methods=['GET','POST'])
def signUp():
    """Registers Users"""
    form = RegistrationForm()
    if request.method == 'POST': 
        if form.validate_on_submit():
            firstName  = form.firstName.data.strip().lower()
            lastName = form.lastName.data.strip().lower()
            email = form.email.data.strip().lower()
            password = form.password.data.strip()
            retypePassword = form.retypePassword.data.strip()

            if password != retypePassword:
                return jsonify({'result':"passwords do not match"}),400

            if db.session.query(Users.id).filter(Users.email==email).first() is not None:
                return jsonify({"result": "User already has an account"}),400
            
            
            else:
             
                newUser = Users(
                    first_name = firstName,
                    last_name = lastName,
                    email = email,
                    password = generate_password_hash(password, method='pbkdf2:sha256'),
                    role = 'user'
                )
            
                try:
                    db.session.add(newUser)
                    db.session.commit()
                    return jsonify({"result":"Successfully Registered"}),201
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
                'type': field.widget.input_type,
                'name': field.name,
                'required': field.flags.required,
            })
        csrf_token = generate_csrf()
        response = jsonify(form_fields)
        response.headers['X-CSRF-Token'] = csrf_token
        return response

@main.route('/logout',methods=['GET'])
def logout():
    """Logout of the application"""
    logout_user()
    return jsonify({"result": "Logged out seccessfully"}),200



# Here we define a function to collect form errors
# which we can later use
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



@main.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@main.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))



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

