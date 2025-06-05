from flask import Blueprint, render_template,send_file,request,flash, redirect, url_for,session
from flask_login import login_required, current_user
import io
from .models import Product,OrderDetails,Model,Customer
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
        products = Product.query.join(Product.model).filter(
            Model.Model_Name.ilike(f"%{search_query}%")
        ).all()
    else:
        products = Product.query.all()
    return render_template('products.html', products=products, user=current_user)

@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please log in to add products to cart.", category='error')
        return redirect(url_for('auth.login'))

    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash("Product added to cart!", category='success')
    return redirect(url_for('views.products'))

@views.route('/cart')
def cart():
    cart = session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            item_total = quantity * product.Price
            products.append({
                'productID': product.Product_ID,
                'productName': product.model.Model_Name,
                'quantity': quantity,
                'unitPrice': product.Price,
                'total': item_total
            })
            total += item_total
    return render_template('cart.html', products=products, total=total, user=current_user)

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