from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import db, Employee, Product, Orders, OrderDetails, Customer, Model, InventoryRecord,Purchase
from sqlalchemy import func, desc

control = Blueprint('control', __name__)

@control.route('/dashboard')
@login_required
def dashboard():
    # 1. Most Sold Products
    top_products = (
        db.session.query(
            Product.Product_ID,
            Model.Model_Name,
            Product.Product_Type,
            Product.Price,
            func.sum(OrderDetails.quantity).label('total_sold')
        )
        .join(OrderDetails, OrderDetails.Product_ID == Product.Product_ID)
        .join(Model, Product.Product_ID == Model.Model_ID)
        .group_by(Product.Product_ID)
        .join(Orders, Orders.Order_ID==OrderDetails.Order_ID )
        .order_by(desc('total_sold'))
        .filter(Orders.Employee_ID.isnot(None))
        .all()
    )

    # 2. Top Selling Employees
    top_employees = (
        db.session.query(
            Employee.Employee_ID,
            Employee.Emp_Name,
            func.count(Orders.Order_ID).label('orders_handled'),
            func.sum(OrderDetails.quantity).label('items_sold')
        )
        .join(Orders, Orders.Employee_ID == Employee.Employee_ID)
        .join(OrderDetails, OrderDetails.Order_ID == Orders.Order_ID)
        .group_by(Employee.Employee_ID)
        .order_by(desc('items_sold'))
        .filter(Employee.Emp_Name != "abdallah kokash" and Orders.Employee_ID.isnot(None))
        .all()
    )

    # 3. Total Revenue
    total_revenue = db.session.query(func.sum(Orders.Total_Price)).filter(Orders.Employee_ID.isnot(None)).scalar()

    # 4. Total Employees
    total_employees = db.session.query(func.count(Employee.Employee_ID)).scalar()

    # 5. Total Customers
    total_customers = db.session.query(func.count(Customer.Customer_ID)).scalar()

    # 6. Top 5 Customers by Spending
    customers_spend_most = (
        db.session.query(
            Customer.Customer_ID,
            Customer.Full_Name,
            Customer.Email,
            Customer.Phone_Number,
            func.sum(Orders.Total_Price).label("total_spent")
        )
        .join(Orders, Orders.Customer_ID == Customer.Customer_ID)
        .group_by(Customer.Customer_ID)
        .order_by(desc("total_spent"))
        .filter(Orders.Employee_ID.isnot(None))
        .limit(5)
        .all()
    )

    # 7. Low Stock Alerts
    low_stock_items = (
        db.session.query(
            Product.Product_ID,
            Product.Product_Type,
            Model.Model_Name,
            InventoryRecord.Quantity,
        )
        .join(Model, Product.Product_ID == Model.Model_ID)
        .join(InventoryRecord, InventoryRecord.Model_ID == Model.Model_ID)
        .filter(InventoryRecord.Quantity < 5)
        .all()
    )
    # 7. Total Expenses
    total_expenses = db.session.query(func.sum(Purchase.Total_Cost)).scalar()

    # 8. Total Expenses
    total_profit = (total_revenue) - total_expenses

    # 9. Revenue by product
    product_sales_data = (
        db.session.query(
            Product.Product_Type,
            Model.Model_Name,
            func.sum(OrderDetails.quantity).label("total_quantity"),
            func.sum(OrderDetails.quantity * Product.Price).label("revenue")
        )
        .join(OrderDetails, OrderDetails.Product_ID == Product.Product_ID)
        .join(Model, Product.Product_ID == Model.Model_ID)
        .join(Orders, Orders.Order_ID == OrderDetails.Order_ID)
        .group_by(Product.Product_ID)
        .filter(Orders.Employee_ID.isnot(None))
        .all()
    )
    return render_template("dashboard.html",
                           total_revenue=total_revenue,
                           total_employees=total_employees,
                           total_customers=total_customers,
                           total_expenses=total_expenses,
                           total_profit=total_profit,
                           top_products=top_products,
                           top_employees=top_employees,
                           top_customers=customers_spend_most,
                           low_stock_items=low_stock_items,
                           product_sales_data=product_sales_data)