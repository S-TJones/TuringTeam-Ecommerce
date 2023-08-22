from flask import Blueprint, current_app, jsonify, render_template

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user

from app.forms import LoginForm,RegistrationForm
from app.models import Users,Product
from app.extensions import db

from werkzeug.security import check_password_hash

main = Blueprint('main', __name__,url_prefix='/api/v1')

@main.route('/products')
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




@main.route("/login", methods=["POST"])
def login():
    """Visitor uses this to Authorise and Authenticate themselves"""

    if current_user is not None and current_user.is_authenticated:
        return jsonify({"result":"Successful Login",'user_id':current_user.get_id()}),200
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            
            user = Users.query.filter_by(email = email).first()

            if user is not None and check_password_hash(user.password, password):

                #will use current_user.role to access authorisation
                login_user(user)
                return jsonify({"result":"Successful Login",'user_id':user.id}),200

            else:
                return jsonify({"result":"Login unsuccessful. Check credentials"}),401
            
@main.route('/sign-up',methods=['GET','POST'])
def signUp():
    """Registers Users"""
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstName  = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data
        retypePassword = form.retypePassword.data

        if password != retypePassword:
            return jsonify({'result':"passwords do not match"}),400

        if db.session.query(Users.id).filter(Users.email==email).first() is not None:
            return jsonify({"result": "User already has an account"}),400
        
        else:
            newUser = Users(
                firstName = firstName,
                lastName = lastName,
                email = email,
                password = password,
                role = 'User'
            )

            db.session.add(newUser)
            db.session.commit()

        return jsonify({"result":"Successfully Registered"}),201
    else:        
        error={
                "error": form_errors(form)
            }
        return jsonify(error),400
    

@main.route('/logout')
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
