from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Employee,Customer,CustomerContact,EmployeeContact
from flask_login import login_user, logout_user, login_required, current_user
from . import db
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        employee =EmployeeContact.query.filter_by(Email=email).first()
        customer =CustomerContact.query.filter_by(Email=email).first()
        if  employee:
            if  employee.Pass == password:
                flash('Logged in successfully', 'success')
                login_user( employee, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', 'error')
        elif customer:
            if customer.Pass == password:
                flash('Logged in successfully', 'success')
                login_user( customer, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', 'error')
        else:
            flash('Email does not exist.', 'error')
    return render_template("login.html", user=current_user)


@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == "POST":
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        phone = request.form.get('phone')
        if len(full_name) < 3:
            flash('Name must be at least 3 characters.', 'error')
        elif len(password) < 5:
            flash('Password must be at least 5 characters.', 'error')
        elif len(phone) < 10:
            flash('Phone must be at least 10 characters.', 'error')
        elif len(address) < 10:
            flash('Address must be at least 10 characters.', 'error')
        elif len(email) < 10:
            flash('Email must be at least 10 characters.', 'error')
        else:
            email_exists = (
                    CustomerContact.query.filter_by(Email=email).first() or
                    EmployeeContact.query.filter_by(Email=email).first()
            )
            phone_exists = (
                    CustomerContact.query.filter_by(Phone_Number=phone).first() or
                    EmployeeContact.query.filter_by(Phone_Number=phone).first()
            )

            if email_exists:
                flash('Email is already in use by another customer or employee.', 'error')
            elif phone_exists:
                flash('Phone number is already in use by another customer or employee.', 'error')
            else:
                # Step 1: Create Customer (only Full_Name)
                newCustomer = Customer(Full_Name=full_name)
                db.session.add(newCustomer)
                db.session.commit()

                # Step 2: Use generated Customer_ID to create CustomerContact
                customer_contact = CustomerContact(
                    Customer_ID=newCustomer.Customer_ID,
                    Email=email,
                    Phone_Number=phone,
                    Address=address,
                    Pass=password
                )
                db.session.add(customer_contact)
                db.session.commit()

                flash('Successfully Registered', 'success')
                return redirect(url_for('views.home', user=current_user))
    return render_template("signUp.html",user=current_user)



@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    session.pop('cart', None)
    return redirect(url_for('views.home'))