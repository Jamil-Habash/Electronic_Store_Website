from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import db, Employee, Product, Orders, OrderDetails, Customer, Model, InventoryRecord,Purchase , PurchaseDetail
from sqlalchemy import func, desc,cast, String

control = Blueprint('control', __name__)


@control.route('/inventory')
@login_required
def inventory():
    query =(db.session.query(
        Product,
        Model.Model_Name,
        InventoryRecord.Quantity
    )
    .join(Model, Model.Model_ID == Product.Product_ID)
    .join(InventoryRecord, Model.Model_ID == InventoryRecord.Model_ID)
    )
    search_field = request.args.get('field')
    search_value = request.args.get('value')

    if search_field == "Model_Name":
        query = query.filter(Model.Model_Name.ilike(f"%{search_value}%"))

    elif search_field == "Product_Type":
        query = query.filter(Product.Product_Type.ilike(f"%{search_value}%"))

    results = query.all()
    if not results:
        flash('No products found', 'error')
    return render_template("inventory.html", user=current_user, products=  results)

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
        .filter(Employee.Emp_Name != "abdallah kokash")
        .filter(Orders.Employee_ID.isnot(None))
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
    # 8. Total Expenses
    total_expenses = db.session.query(func.sum(Purchase.Total_Cost)).scalar()

    # 9. Total profit
    total_profit = (total_revenue) - total_expenses

    # 10. Revenue by product
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


@control.route('/empManager')
@login_required
def employee_manager():
    search_field = request.args.get('field')
    search_value = request.args.get('value')

    filters = {
        "Employee_ID": Employee.Employee_ID,
        "Emp_Name": Employee.Emp_Name,
        "Date_Of_Birth": Employee.Date_Of_Birth,
        "Salary": Employee.Salary,
        "Email": Employee.Email,
        "Phone_Number": Employee.Phone_Number,
        "Address": Employee.Address
    }
    if search_field and search_value:
        column = filters.get(search_field)

        if column.type.python_type.__name__ == 'date':

            employees = Employee.query.filter(column == search_value).all()
        else:
            employees = Employee.query.filter(cast(column, String).ilike(f"%{search_value}%")).all()
    else:
        employees = Employee.query.all()
    if not employees:
        flash('No Employee Found', 'error')
    return render_template("employee.html", user=current_user, employees=employees)

@control.route('/add_employee', methods=['GET', 'POST'])
def addEmp():
    if request.method == "POST":
        empName = request.form.get('empName')
        empPhone = request.form.get('empPhoneNumber')
        empAddress = request.form.get('empAddress')
        empDateOfBirth = request.form.get('empDateOfBirth')
        empEmail = request.form.get('empEmail')
        empPass = request.form.get('empPass')
        empSalary = request.form.get('empSalary')
        if len(empName) < 3:
            flash('Incorrect Name', 'error')
        elif len(empPhone) != 10:
            flash('Incorrect Phone Number', 'error')
        elif len(empAddress) < 3:
            flash('Incorrect Address', 'error')
        elif len(empEmail) < 8:
            flash('Incorrect Email', 'error')
        elif len(empPass) < 3:
            flash('Incorrect Password', 'error')
        else:
            newEmp = Employee(Emp_Name=empName, Phone_Number=empPhone, Address=empAddress, Email=empEmail,
                              Pass=empPass, Date_Of_Birth=empDateOfBirth, Salary=empSalary)
            db.session.add(newEmp)
            db.session.commit()
            flash('Successfully Registered', 'success')
    employees = Employee.query.all()
    return render_template("employee.html", user=current_user, employees=employees)


@control.route('/update_employee', methods=['GET', 'POST'])
def updateEmp():
    if request.method == "POST":
        empID = request.form.get('employeeId')
        empName = request.form.get('empName')
        empPhone = request.form.get('empPhoneNumber')
        empAddress = request.form.get('empAddress')
        empDateOfBirth = request.form.get('empDateOfBirth')
        empEmail = request.form.get('empEmail')
        empPass = request.form.get('empPass')
        empSalary = request.form.get('empSalary')
        if len(empName) < 3:
            flash('Incorrect Name', 'error')
        elif len(empPhone) != 10:
            flash('Incorrect Phone Number', 'error')
        elif len(empAddress) < 3:
            flash('Incorrect Address', 'error')
        elif len(empEmail) < 8:
            flash('Incorrect Email', 'error')
        elif len(empPass) < 3:
            flash('Incorrect Password', 'error')
        else:
            employee = Employee.query.filter_by(Employee_ID=empID).first()
            employee.Emp_Name = empName
            employee.Phone_Number = empPhone
            employee.Address = empAddress
            employee.Email = empEmail
            employee.Pass = empPass
            employee.Date_Of_Birth = empDateOfBirth
            employee.Salary = empSalary
            db.session.commit()
            flash('Successfully Updated', 'success')
    employees = Employee.query.all()

    return render_template("employee.html", user=current_user, employees=employees)

@control.route('/delete_employee', methods=['GET', 'POST'])
def deleteEmp():
    if request.method == "POST":
        empID = request.form.get('employeeId')
        employee = Employee.query.filter_by(Employee_ID=empID).first()
        if not employee:
            flash('Employee Does Not Exist', 'error')
        else:
            db.session.delete(employee)
            db.session.commit()
            flash('Successfully Deleted', 'success')
    employees = Employee.query.all()
    return render_template("employee.html", user=current_user, employees=employees)
@control.route('/orders')
@login_required
def orders():
    search_field = request.args.get('field')
    search_value = request.args.get('value')
    filters = {
        "Order_ID": Orders.Order_ID,
        "Customer_ID": Orders.Customer_ID,
        "Employee_ID": Orders.Employee_ID,
        "Total_Price": Orders.Total_Price,
        "Date_Of_Order": Orders.Date_Of_Order,
    }
    if search_field and search_value:
        column = filters.get(search_field)
        if column.type.python_type.__name__ == 'date':
            orders = Orders.query.filter(Orders.Employee_ID.isnot(None),column == search_value).all()
        else:
            orders = Orders.query.filter(Orders.Employee_ID.isnot(None),cast(column, String).ilike(f"%{search_value}%")).all()
    else:
        orders = Orders.query.filter(Orders.Employee_ID.isnot(None)).order_by(Orders.Order_ID).all()
    pending_orders = Orders.query.filter(Orders.Employee_ID.is_(None)).all()
    return render_template('orders.html', orders=orders, pending_orders=pending_orders, user=current_user)

@control.route('/orders/approve/<int:order_id>', methods=['POST'])
@login_required
def approve_order(order_id):
    order = Orders.query.get(order_id)
    if not order:
        flash('Order not found.', 'warning')
        return redirect(url_for('control.orders'))

    order.Employee_ID = Employee.Employee_ID
    for detail in order.order_details:
        product = Product.query.get(detail.Product_ID)
        if product:
            inventory_record = InventoryRecord.query.filter_by(Model_ID=product.Product_ID).first()
            if inventory_record:
                inventory_record.Quantity -= detail.quantity
                if inventory_record.Quantity < 0:
                    inventory_record.Quantity = 0
    db.session.commit()
    flash(f'Order #{order_id} approved and inventory updated.', 'success')
    return redirect(url_for('control.orders'))

@control.route('/purchase_orders')
@login_required
def purchase_orders():
    search_field = request.args.get('field')
    search_value = request.args.get('value')
    filters = {
        "Purchase_ID": Purchase.Purchase_ID,
        "Employee_ID": Purchase.Employee_ID,
        "Date_Of_Purchase": Purchase.Date_Of_Purchase,
        "Total_Price": Purchase.Total_Cost,
    }

    if search_field and search_value:
        column = filters.get(search_field)
        if column.type.python_type.__name__ == 'date':
            purchases_order = Purchase.query.filter(column == search_value).all()
        else:
            purchases_order = Purchase.query.filter(cast(column, String).ilike(f"%{search_value}%")).all()
    else:
        purchases_order = Purchase.query.all()
    return render_template('purchase_orders.html', purchases_order=purchases_order, user=current_user)