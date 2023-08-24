import enum
from datetime import datetime
from flask_login import UserMixin
# from app.extensions import db
from . import db


# User Class
class Users(UserMixin, db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    # Instead of full name, first and last
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, first_name, last_name, email,password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return f"<User: {self.email}, id: {self.id} >"

#----------------------------------------------------------------------
#Note The class below is not a DB model, but Enumerate. Note parameter of the class definition.
# See https://docs.python.org/3/library/functions.html#enumerate
class ProductStatus(enum.Enum):
    # Status (e.g. pending, published)
    pending = 'pending'
    published = 'published'

# Product Class
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(2048))
    price = db.Column(db.Numeric(8,2), nullable = False)
    image = db.Column(db.String(256))
    status = db.Column(db.Enum(ProductStatus))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, description, price, image, status, user_id):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.status = status
        self.user_id = user_id

    def get_status(self):
        stat = str(self.status).split('.')
        return stat[1]
    
    # These methods to splice off the unwanted part of the Enum selected
    # They are called on the object in the respective views
    def __repr__(self):
        return f"<{self.id},{self.title},{self.type},{self.price}>"

#----------------------------------------------------------------------
#Note The class below is not a DB model, but Enumerate. Note parameter of the class definition.
# See https://docs.python.org/3/library/functions.html#enumerate

class OrderStatus(enum.Enum):
    # Status (e.g. pending, completed, canceled)
    pending = 'Pending'
    completed = 'Completed'
    cancelled = 'Cancelled'

# Order Class
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer,primary_key =True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    billing_address = db.Column(db.String(256))
    total_amount = db.Column(db.Numeric(8,2),nullable  = False)
    status = db.Column(db.Enum(OrderStatus))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,user_id, billing_address, total_amount, status):
        self.user_id = user_id
        self.billing_address = billing_address
        self.total_amount = total_amount
        self.status = status
    
    def get_status(self):
            stat = str(self.status).split('.')
            return stat[1]

    def __repr__(self):
        return f"< Order Id: {self.id}, Status: {self.status}>"

    def get_status(self):
       _ = str(self.status).split('.')
       return _[1]
    
#----------------------------------------------------------------------

class LineItems(db.Model):
    __tablename__ = 'line_items'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Numeric, nullable =False)

    def __init__(self,order_id, product_id, quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return f"<id: {self.id}, user_id: {self.user_id}>"

class ShoppingCart(db.Model):
    __tablename__='shopping_cart'

    id= db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('products.id'),nullable= False)
    quantity = db.Column(db.Numeric,nullable =False)

    def __init__(self,user_id,product_id,quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return f"<id: {self.id}, user_id: {self.user_id}>"