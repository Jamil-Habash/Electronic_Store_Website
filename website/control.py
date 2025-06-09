from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import db, Employee, Product, Orders, OrderDetails, Customer, Model, InventoryRecord, Purchase,PurchaseDetail
from sqlalchemy import func, desc, cast, String
from datetime import date
import os

control = Blueprint('control', __name__)


@control.route('/purchase')
@login_required
def purchase():
    products = [
        {
            "Model_Name": "Inspiron 15",
            "price": 500,
            "warranty": "12 month",
            "type": "Laptop",
            "image": "Inspiron 15.jpg",
            "description": "Dell Inspiron 15 is a dependable all-rounder designed for daily productivity. Equipped with an Intel Core i5, 8GB RAM,"
                           "and 256GB SSD, it delivers smooth multitasking performance. Its 15.6\" Full HD display provides vibrant visuals, and the full-size keyboard enhances typing comfort. "
                           "Ideal for students and professionals who need a reliable, budget-friendly machine with strong battery life and solid connectivity options."
        },
        {
            "Model_Name": "XPS 13",
            "price": 1000,
            "warranty": "24 month",
            "type": "Laptop",
            "image": "XPS 13.jpg",
            "description": "Dell XPS 13 blends power with elegance. Featuring a sleek aluminum chassis, it houses an Intel Core i7, 16GB RAM, and 512GB SSD. "
                           "The 13.3\" InfinityEdge display offers near-borderless viewing with rich colors. Great for professionals on the move, its portability, long battery life, "
                           "and premium build make it perfect for presentations, video calls, and creative workflows."
        },
        {
            "Model_Name": "Pavilion 14",
            "price": 600,
            "warranty": "12 month",
            "type": "Laptop",
            "image": "Pavilion 14.jpg",
            "description": "HP Pavilion 14 offers a refined computing experience with an AMD Ryzen 5, 8GB RAM, and 512GB SSD. "
                           "Its compact and stylish design makes it perfect for students or casual users. The 14\" FHD display, fast boot time, and responsive performance make everyday tasks—from streaming to document editing—efficient and enjoyable."
        },
        {
            "Model_Name": "Envy 13",
            "price": 1300,
            "warranty": "24 month",
            "type": "Laptop",
            "image": "Envy 13.jpg",
            "description": "HP Envy 13 combines power, portability, and aesthetics. Equipped with an Intel Core i7, 16GB RAM, and 512GB SSD, it easily handles demanding apps. "
                           "The 13.3\" FHD touchscreen is sharp and responsive, while the all-metal chassis adds a premium feel. Bang & Olufsen speakers, fingerprint sensor, and long battery life make it perfect for creatives and professionals alike."
        },
        {
            "Model_Name": "ThinkPad X1 Carbon",
            "price": 1200,
            "warranty": "36 month",
            "type": "Laptop",
            "image": "ThinkPad X1 Carbon.jpg",
            "description": "Lenovo ThinkPad X1 Carbon is a business-class ultrabook known for its military-grade durability and world-class keyboard. With an Intel Core i7, 16GB RAM, 1TB SSD, "
                           "and a stunning 14\" UHD display, it's built for serious multitaskers. Features include a fingerprint reader, rapid charging, and a featherlight carbon fiber body—ideal for professionals who demand both power and portability."
        },
        {
            "Model_Name": "IdeaPad 5",
            "price": 600,
            "warranty": "12 month",
            "type": "Laptop",
            "image": "IdeaPad 5.jpg",
            "description": "Lenovo IdeaPad 5 is a well-rounded laptop for home and office use. It features an AMD Ryzen 7 processor, 8GB RAM, and 512GB SSD, delivering excellent speed and responsiveness. "
                           "Its 15.6\" Full HD display with narrow bezels ensures immersive viewing, while Dolby Audio speakers enhance entertainment. Perfect for those who need solid performance without breaking the bank."
        },
        {
            "Model_Name": "MacBook Air M2",
            "price": 1100,
            "warranty": "24 month",
            "type": "Laptop",
            "image": "MacBook Air M2.jpg",
            "description": "The new MacBook Air with M2 chip sets a new standard for ultraportables. With 8GB RAM, 256GB SSD, and a brilliant 13.6\" Liquid Retina display, it offers impressive power in a thin, silent design. "
                           "Ideal for students, developers, and everyday creatives, it supports seamless multitasking, powerful graphics, and over 18 hours of battery life—all in a fanless, ultra-light enclosure."
        },
        {
            "Model_Name": "MacBook Pro 14",
            "price": 1900,
            "warranty": "36 month",
            "type": "Laptop",
            "image": "MacBook Pro 14.jpg",
            "description": "Apple MacBook Pro 14 is engineered for performance-hungry professionals. Featuring the Apple M2 Pro chip, 16GB RAM, and 512GB SSD, it handles intensive tasks like video editing, 3D rendering, and music production with ease. "
                           "Its 14.2\" Liquid Retina XDR display offers stunning brightness and contrast, while studio-quality microphones and powerful speakers enhance creative workflows. Built for professionals who demand excellence."
        },
        {
            "Model_Name": "Asus ROG",
            "price": 1800,
            "warranty": "32 month",
            "type": "Laptop",
            "image": "Asus ROG.jpg",
            "description": "Asus ROG series is built for gamers and power users. With high-end AMD Ryzen or Intel Core i9 CPUs, NVIDIA RTX GPUs, RGB keyboards, and superior thermal cooling, it delivers elite gaming performance and multitasking capabilities for streamers and creators."
        },
        {
            "Model_Name": "Lenovo Ideapad 3",
            "price": 600,
            "warranty": "24 month",
            "type": "Laptop",
            "image": "lenovo ideapad 3.jpg",
            "description": "Lenovo Ideapad 3 is a budget-friendly laptop offering solid performance for everyday tasks. With Intel i3 or Ryzen 3, a 15.6\" display, and Dolby Audio, it’s great for students, families, and casual browsing or media consumption."
        },
        {
            "Model_Name": "Samsung 15 AI Book 4",
            "price": 950,
            "warranty": "12 month",
            "type": "Laptop",
            "image": "Samsung 15 AI Book 4.jpg",
            "description": "Samsung Galaxy Book 4 combines premium design with AI-enhanced performance. Featuring Intel AI chips, Super AMOLED display, and seamless Galaxy ecosystem integration, it’s a stylish and powerful laptop for multitasking professionals and creatives alike."
        },
        {
            "Model_Name": "Asus Tuf F15",
            "price": 1200,
            "warranty": "12 month",
            "type": "Laptop",
            "image": "Asus Tuf F15.jpg",
            "description": "Asus TUF F15 is a durable gaming laptop designed for performance under pressure. Equipped with 12th Gen Intel Core processors, NVIDIA GeForce RTX graphics, and military-grade construction, it handles AAA gaming and multitasking with ease."
        }
    ]

    return render_template("purchase.html", user=current_user, products=products)
@control.route('/commit_purchase', methods=['POST'])
@login_required
def commit_purchase():
    product_names = request.form.getlist('model_name')
    quantities = request.form.getlist('quantity')
    prices = request.form.getlist('unit_price')
    product_types = request.form.getlist('product_type')
    warranties = request.form.getlist('warranty')
    descriptions = request.form.getlist('description')

    if not product_names:
        return redirect(url_for('control.purchase'))

    total_cost = 0
    purchase_items = []
    for name, qty_str, price_str, ptype, warranty_str, desc in zip(
            product_names, quantities, prices, product_types, warranties, descriptions):
        qty = int(qty_str)
        price = float(price_str) +200
        warranty = int(warranty_str.split(" ")[0])
        total_cost += qty * price
        purchase_items.append((name, qty, price, ptype, warranty, desc))

    purchase = Purchase(
        Employee_ID=current_user.Employee_ID,
        Date_Of_Purchase=date.today(),
        Total_Cost=total_cost
    )
    db.session.add(purchase)
    db.session.flush()

    for name, qty, price, ptype, warranty, desc in purchase_items:
        model = Model.query.filter_by(Model_Name=name).first()
        detail = PurchaseDetail(
            Purchase_ID=purchase.Purchase_ID,
            Model_ID=model.Model_ID,
            Quantity=qty,
            Cost_Per_Unit=price
        )
        db.session.add(detail)

        product = Product.query.filter_by(Product_ID=model.Model_ID).first()
        if not product:
            image_path = os.path.join("website", "static", name + ".jpg")
            with open(image_path, "rb") as f:
                image_data = f.read()
            product = Product(
                Product_ID=model.Model_ID,
                Price=price,
                Product_Type=ptype,
                Warranty=warranty,
                Picture=image_data,
                Descriptions=desc
            )
            db.session.add(product)

            inventory_record = InventoryRecord(
                Model_ID=model.Model_ID,
                Quantity=qty
            )
            db.session.add(inventory_record)
        else:
            inventory_record = InventoryRecord.query.filter_by(Model_ID=model.Model_ID).first()
            if inventory_record:
                inventory_record.Quantity += qty

    db.session.commit()
    flash("Purchase committed successfully!", "success")
    return redirect(url_for('control.purchase'))
@control.route('/inventory')
@login_required
def inventory():
    query = (db.session.query(
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
    return render_template("inventory.html", user=current_user, products=results)


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
        .join(Orders, Orders.Order_ID == OrderDetails.Order_ID)
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
        .filter(Employee.Email != "manager@outlook.com")
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
    range_min = request.args.get('range_min')
    range_max = request.args.get('range_max')

    filters = {
        "Employee_ID": Employee.Employee_ID,
        "Emp_Name": Employee.Emp_Name,
        "Date_Of_Birth": Employee.Date_Of_Birth,
        "Salary": Employee.Salary,
        "Email": Employee.Email,
        "Phone_Number": Employee.Phone_Number,
        "Address": Employee.Address
    }
    if (search_field and search_value) or (range_min and range_min) :
        column = filters.get(search_field)

        if column.type.python_type.__name__ == 'date' and range_min and range_max:
            employees = Employee.query.filter(column.between(range_min, range_max))
        elif column.type.python_type.__name__ in ['int', 'float'] and range_min and range_max:
            employees = Employee.query.filter(column.between(float(range_min), float(range_max)))
        elif search_value:
            employees = Employee.query.filter(cast(column, String).ilike(f"%{search_value}%"))
    else:
        employees = Employee.query.all()
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
    range_min = request.args.get('range_min')
    range_max = request.args.get('range_max')
    filters = {
        "Order_ID": Orders.Order_ID,
        "Customer_ID": Orders.Customer_ID,
        "Employee_ID": Orders.Employee_ID,
        "Total_Price": Orders.Total_Price,
        "Date_Of_Order": Orders.Date_Of_Order,
    }
    if (search_field and search_value) or (range_min and range_min):
        column = filters.get(search_field)
        if column.type.python_type.__name__ == 'date' and range_min and range_max:
            orders = Orders.query.filter(Orders.Employee_ID.isnot(None), column.between(range_min, range_max))
        elif column.type.python_type.__name__ in ['int', 'float'] and range_min and range_max:
            orders = Orders.query.filter(Orders.Employee_ID.isnot(None), column.between(float(range_min), float(range_max)))
        else:
            orders = Orders.query.filter(Orders.Employee_ID.isnot(None),
                                         cast(column, String).ilike(f"%{search_value}%")).all()
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

    order.Employee_ID = current_user.Employee_ID
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
    range_min = request.args.get('range_min')
    range_max = request.args.get('range_max')
    filters = {
        "Purchase_ID": Purchase.Purchase_ID,
        "Date_Of_Purchase": Purchase.Date_Of_Purchase,
        "Total_Price": Purchase.Total_Cost,
    }
    if (search_field and search_value) or(range_min and range_min):
        column = filters.get(search_field)
        if column.type.python_type.__name__ == 'date' and range_min and range_max:
            purchases_order = Purchase.query.filter(column.between(range_min, range_max))
        elif column.type.python_type.__name__ in ['int', 'float'] and range_min and range_max:
            purchases_order = Purchase.query.filter(column.between(float(range_min), float(range_max)))
        else:
            purchases_order = Purchase.query.filter(cast(column, String).ilike(f"%{search_value}%"))
    else:
        purchases_order = Purchase.query.all()
    return render_template('purchase_orders.html', purchases_order=purchases_order, user=current_user)