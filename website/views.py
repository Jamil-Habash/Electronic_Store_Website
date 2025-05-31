from flask import Blueprint, render_template
from flask import send_file
import io
from .models import Product,OrderDetails,Model
from . import db
from sqlalchemy import func
from flask_login import current_user

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