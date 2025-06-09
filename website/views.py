from datetime import date
from flask import Blueprint, render_template,send_file,request,flash, redirect, url_for,session,g
from flask_login import login_required, current_user
import io
from .models import Product,Orders,OrderDetails,Model,Customer, Payment, InventoryRecord
from . import db
from sqlalchemy import func,or_

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Top 6 best-selling products by quantity
    best_selling = (
        db.session.query(Product)
        .join(OrderDetails)
        .group_by(Product.Product_ID)
        .order_by(func.sum(OrderDetails.quantity).desc())
        .limit(6)
        .all()
    )

    # Top 6 latest products by model date
    new_products = (
        Product.query
        .join(Product.model)
        .order_by(Model.Manufacture_Date.desc())
        .limit(6)
        .all()
    )
    return render_template("home.html", best_selling_products=best_selling, new_products=new_products,user=current_user)
@views.route('/products')
def products():
    search_query = request.args.get('search', '')
    if search_query:
        products = Product.query.join(Product.model).filter(Model.Model_Name.ilike(f"%{search_query}%")).all()
    else:
        products = Product.query.all()
    return render_template('products.html', products=products, user=current_user)

@views.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product, user=current_user)

@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    product = Product.query.get(product_id)
    inventory = InventoryRecord.query.filter_by(Model_ID=product.Product_ID).first()
    stock = inventory.Quantity
    cart = session.get('cart', {})
    current_quantity_in_cart = cart.get(str(product_id), 0)

    if current_quantity_in_cart + quantity > stock:
        remaining = stock - current_quantity_in_cart
        flash(f"Only {remaining} left in stock. Cannot add more.", category='error')
        return redirect(url_for('views.products'))
    cart[str(product_id)] = current_quantity_in_cart + quantity
    session['cart'] = cart

    flash(f"Added {quantity} of {product.model.Model_Name} to cart!", category='success')
    return redirect(url_for('views.products'))


@views.before_request
def cart_count():
    cart = session.get('cart', {})
    g.cart_count = len(cart) if cart else 0

@views.route('/cart')
def cart():
    cart = session.get('cart', {})
    products = []
    total = 0
    total_after_discount = 0
    def calculate_discount(price, quantity):
        if price < 100:
            return 0.0
        discount = 0.1 * (quantity - 1)
        if discount > 0.5:
            discount = 0.5
        if quantity < 1:
            discount = 0.0
        return discount
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            discount = calculate_discount(product.Price, quantity)
            discounted_price = product.Price * quantity * (1 - discount)
            total_after_discount += discounted_price
            item_total = quantity * product.Price
            products.append({
                'productID': product.Product_ID,
                'productName': product.model.Model_Name,
                'quantity': quantity,
                'unitPrice': product.Price,
                'total': item_total
            })
            total += item_total
    return render_template('cart.html', products=products, total=total,total_after_discount=total_after_discount , user=current_user)

@views.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = str(request.form.get('product_id'))
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        flash("Item removed from cart", "success")
    else:
        flash("Item not found in cart", "error")
    return redirect(url_for('views.cart'))

@views.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    payment_method = request.form.get('payment_method')
    payment_identifier = request.form.get('payment_identifier')
    payment_key = request.form.get('payment_key')

    if payment_method == "Credit Card":
        if not  payment_identifier :
            flash("Credit Card Number is required", "error")
            return redirect(url_for('views.cart'))
        elif any(c.isalpha() for c in  payment_identifier ):
            flash("Credit Card Number should contain only numbers", "error")
            return redirect(url_for('views.cart'))
        if not payment_key:
            flash("CVC is required", "error")
            return redirect(url_for('views.cart'))
        elif any(c.isalpha() for c in payment_key):
            flash("CVC should contain only numbers", "error")
            return redirect(url_for('views.cart'))
    if payment_method == "PayPal":
        if not payment_identifier:
            flash("Paypal Email Is Required", "error")
            return redirect(url_for('views.cart'))
        if not payment_key:
            flash("Paypal Password Is Required", "error")
            return redirect(url_for('views.cart'))
    def calculate_discount(price, quantity):
        if price < 100:
            return 0.0
        discount = 0.1 * (quantity - 1)
        if discount > 0.5:
            discount = 0.5
        if quantity < 1:
            discount = 0.0
        return discount

    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            discount = calculate_discount(product.Price, quantity)
            discounted_price = product.Price * quantity * (1 - discount)
            total_price += discounted_price
    # Create Order
    new_order = Orders(
        Customer_ID=current_user.Customer_ID,
        Total_Price=total_price,
        Date_Of_Order=date.today()
    )
    db.session.add(new_order)
    db.session.commit()
    # Add OrderDetails with calculated discounts
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            discount_rate = calculate_discount(product.Price, quantity)
            order_detail = OrderDetails(
                Order_ID=new_order.Order_ID,
                Product_ID=product.Product_ID,
                Discount=discount_rate*100,
                quantity=quantity
            )
            db.session.add(order_detail)
    # Add Payment
    new_payment = Payment(
        Order_ID=new_order.Order_ID,
        Payment_Method=payment_method,
        Payment_Identifier=payment_identifier,
        Payment_Key=payment_key
    )
    db.session.add(new_payment)
    db.session.commit()
    # Clear cart
    session['cart'] = {}
    flash("Order placed and payment recorded!", category='success')
    return redirect(url_for('views.home'))

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    customer = Customer.query.get(current_user.Customer_ID)
    if request.method == 'POST':
        customer.Full_Name = request.form['Full_Name']
        customer.Email = request.form['Email']
        customer.Phone_Number = request.form['Phone_Number']
        customer.Address = request.form['Address']
        customer.Pass = request.form['Pass']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('views.profile'))

    return render_template("profile.html", customer=customer,user=current_user)
@views.route('/product/image/<int:product_id>')
def product_image(product_id):
    product = Product.query.get_or_404(product_id)
    if product.Picture:
        return send_file(
            io.BytesIO(product.Picture),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name=f"product_{product_id}.jpg"
        )
    return "Image not found", 404