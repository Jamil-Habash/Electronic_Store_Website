from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Employee,Customer
from flask_login import login_user, logout_user, login_required, current_user
from . import db
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = Employee.query.filter_by(Email=email).first()
        if user:
            if user.Pass == password:
                flash('Logged in successfully', 'success')
                login_user(user, remember=True)
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
        elif email.lower().startswith('emp'):
            flash('Email cannot start with "emp".', 'error')
        else:
            newCustomer = Customer(Full_Name=full_name,Address=address,Phone_Number=phone,Email=email,Pass=password)
            db.session.add( newCustomer)
            db.session.commit()
            flash('Successfully Registered', 'success')
            return redirect(url_for('views.home'),user=current_user)
    return render_template("signUp.html",user=current_user)



@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('auth.login'))
