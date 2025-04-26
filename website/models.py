from . import db
from flask_login import UserMixin


# Employee Table
class Employee(db.Model, UserMixin):
    __tablename__ = 'Employee'
    Employee_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    SSN = db.Column(db.String(32), unique=True, nullable=False)
    Emp_Name = db.Column(db.String(32))
    Phone_Number = db.Column(db.String(32))
    Address = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Pass = db.Column(db.String(100), nullable=False)
    Date_Of_Birth = db.Column(db.Date)
    Salary = db.Column(db.Float, nullable=False)

    def get_id(self):
        return str(self.Employee_ID)


# Company Table
class Company(db.Model):
    __tablename__ = 'Company'
    Company_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Company_Name = db.Column(db.String(50))
    Address = db.Column(db.String(100))
    mail = db.Column(db.String(100))


# Model Table
class Model(db.Model):
    __tablename__ = 'Model'
    Model_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Model_Name = db.Column(db.String(50))
    Manufacture_Date = db.Column(db.Date)
    Company_ID = db.Column(db.Integer, db.ForeignKey('Company.Company_ID', onupdate='CASCADE'))
    company = db.relationship('Company', backref=db.backref('models'))


# Inventory_Record Table
class InventoryRecord(db.Model):
    __tablename__ = 'Inventory_Record'
    Record_ID = db.Column(db.Integer)
    Model_ID = db.Column(db.Integer, db.ForeignKey('Model.Model_ID', onupdate='CASCADE'), primary_key=True)
    Quantity = db.Column(db.Integer)
    model = db.relationship('Model', backref=db.backref('inventory_records', uselist=False))


# Product Table
class Product(db.Model):
    __tablename__ = 'Product'
    Product_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Price = db.Column(db.Float)
    Product_Type = db.Column(db.String(50))
    Warranty = db.Column(db.Integer)
    Model_ID = db.Column(db.Integer, db.ForeignKey('Model.Model_ID', onupdate='CASCADE'))
    model = db.relationship('Model', backref=db.backref('products'))


# Customer Table
class Customer(db.Model):
    __tablename__ = 'Customer'
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Phone_Number = db.Column(db.String(15))
    Address = db.Column(db.String(100))
    Full_Name = db.Column(db.String(100))


# Orders Table
class Orders(db.Model):
    __tablename__ = 'Orders'
    Order_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID', onupdate='CASCADE'))
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employee.Employee_ID', onupdate='CASCADE'))
    Total_Price = db.Column(db.Float)
    Payment_Method = db.Column(db.String(50))
    Date_Of_Order = db.Column(db.Date)
    customer = db.relationship('Customer', backref=db.backref('orders'))
    employee = db.relationship('Employee', backref=db.backref('orders'))


# Order_Details Table
class OrderDetails(db.Model):
    __tablename__ = 'Order_Details'
    Order_ID = db.Column(db.Integer, db.ForeignKey('Orders.Order_ID', ondelete='CASCADE'), primary_key=True)
    Product_ID = db.Column(db.Integer, db.ForeignKey('Product.Product_ID', ondelete='CASCADE'), primary_key=True)
    Discount = db.Column(db.DECIMAL(5, 2))
    order = db.relationship('Orders', backref=db.backref('order_details'))
    product = db.relationship('Product', backref=db.backref('order_details', uselist=False))


# Purchase Table
class Purchase(db.Model):
    __tablename__ = 'Purchase'
    Purchase_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employee.Employee_ID', onupdate='CASCADE'))
    Date_Of_Purchase = db.Column(db.Date)
    Total_Cost = db.Column(db.Float)
    Payment_Method = db.Column(db.String(50))
    Tax = db.Column(db.DECIMAL(5, 2))
    employee = db.relationship('Employee', backref=db.backref('purchases'))


# Purchase_Detail Table
class PurchaseDetail(db.Model):
    __tablename__ = 'Purchase_Detail'
    Purchase_ID = db.Column(db.Integer, db.ForeignKey('Purchase.Purchase_ID', ondelete='CASCADE'), primary_key=True)
    Model_ID = db.Column(db.Integer, db.ForeignKey('Model.Model_ID', ondelete='CASCADE'), primary_key=True)
    Quantity = db.Column(db.Integer)
    Cost_Per_Unit = db.Column(db.Float)
    purchase = db.relationship('Purchase', backref=db.backref('purchase_details'))
    model = db.relationship('Model', backref=db.backref('purchase_details'))
