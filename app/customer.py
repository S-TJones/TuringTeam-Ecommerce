from flask import Blueprint, jsonify, current_app, request, session
from flask_login import LoginManager, current_user, login_required
from sqlalchemy import and_
from app import login_manager
# from app.extensions import db
from . import db

from datetime import datetime
from app.models import LineItems, Order, Product, ShoppingCart, Users


customer = Blueprint('customer', __name__, url_prefix='/api/v1/customer')

@customer.route('/status')
def status():
    return jsonify({ "message": "API Operational for  cx" })

@customer.route('/orders/', methods=['GET'])
@login_required
def viewOrders():
    orders = Order.query.filter(Order.customer_id == current_user.get_id()).all()
    orderList =[]
    if len(orders) !=0:
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
                    'status':order.status,
                    'items':itemList
                }
            )
        
        return jsonify({'result':orderList}),200
    return jsonify({"result": "No orders available"}),204
    

@customer.route('/orders/<orderID>', methods=['GET'])
@login_required
def order_details(orderID):
    order = Order.query.filter(and_(Order.id == orderID, Order.user_id == current_user.get_id())).first()
    
    if order is not None:
        itemList = []
        items = LineItems.query.filter_by(order_id = order.id)
        customer =  Users.query.filter_buy(id = current_user.get_id())
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



@customer.route('/cart', methods=['GET'])
@login_required
def view_cart():
    #load All line items for the customer
    if request.method == 'GET':
        cartList =[]
        cartItems  = ShoppingCart.query.filter(ShoppingCart.user_id == current_user.get_id()).all()
        
        if len(cartItems) !=0:
            for item in cartItems:
                cartList.append(
                    {
                        'item_id': item.id,
                        'product_name': Product.query.filter(Product.id == item.product_id).first().name,
                        'price': Product.query.filter(Product.id == item.product_id).first().price,
                        'quantity': item.quantity
                    }
                )
            return jsonify({'result':cartList}),200
        else:
            return jsonify({"result": "Your shopping cart is empty"}),204 

@customer.route('/cart/',methods=['POST'])
def addToCart():
    if request.method == 'POST':
        prod_id = request.form['id']

        #commits the item to the shopping cart
        c_uid = current_user.get_id()
        cartItem = ShoppingCart.query.filter(ShoppingCart.product_id == prod_id).filter(ShoppingCart.user_id == c_uid).first()

        # increment the quantity of the item in the cart if present 
        # else put item in cart
        if cartItem is not None:
            cartItem.quantity +=1
            try:
                db.session.commit()
                return jsonify({
                    'result':'Successfully added Item to the cart'
                    }),201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error":e}),500 
        else:
            newCartItem = ShoppingCart(c_uid,prod_id,1)
            try:
                db.session.add(newCartItem)
                db.session.commit()
                return jsonify({
                    'result':'Successfully added Item to the cart'
                    }),201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error":e}),500
            



@customer.route('/cart/<cartItemID>', methods=['DELETE'])
@login_required
def remove_from_cart(cartItemID):
     if request.method == 'DELETE':
        cartItem = ShoppingCart.query.get(cartItemID)
        if cartItem is not None:
            try:
                db.session.delete(cartItem)
                db.session.commit()
                return jsonify({
                    'result':f'Successfully Deleted cart Item'
                    }),200
            except Exception as e:
                db.session.rollback()
                return jsonify({"error":e}),500
        return jsonify({'result':'No such cart Item exists'}),404


@customer.route('/check-out',methods=['GET','POST'])
@login_required
def checkout():
    #------------IMPLEMENTATION OF STRIPE HERE-------------------
    pass

@customer.after_request
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
