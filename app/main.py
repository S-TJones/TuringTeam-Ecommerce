from flask import Blueprint, current_app, render_template

from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user

from app.forms import LoginForm
from app.models import Users
from app.extensions import db

from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # current_app.logger.debug("Hello World")
    return render_template('index.html')

@main.route('/home')
def home():
    """Render website's home page."""
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route("/login", methods=["GET", "POST"])
def login():
    """Visitor uses this to Authorise and Authenticate themselves"""

    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            
            user = Users.query.filter_by(email = email).first()

            if user is not None and check_password_hash(user.password, password):
                # Todo: Check for specific admin user
                login_user(user)
                flash("Logged In Sucessfully",'success')
                next = request.args.get('next')
                return redirect(next or url_for("main.home")) 
            else:
                flash("Incorrect credentials entered",'danger') 

    flash_errors(form)
    return render_template("login.html", form=form)

@main.route('/logout')
def logout():
    """Logout of the application"""
    logout_user() # from Flask-login
    session.clear() 
    flash('You were logged out', 'success')
    return redirect(url_for('main.index'))

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@main.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
