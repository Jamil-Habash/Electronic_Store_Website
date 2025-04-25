from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Employee
from . import db
from flask_login import login_user, logout_user, login_required, current_user

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
            else:
                flash('Incorrect password', 'error')
        else:
            flash('Email does not exist.', 'error')
    return render_template("login.html", user=current_user)


@auth.route('/add_employee', methods=['GET', 'POST'])
def hire():
    if request.method == "POST":
        ssn = request.form.get('SSN')
        empName = request.form.get('empName')
        empPhone = request.form.get('empPhoneNumber')
        empAddress = request.form.get('empAddress')
        empDateOfBirth = request.form.get('empDateOfBirth')
        empEmail = request.form.get('empEmail')
        empPass = request.form.get('empPass')
        if len(ssn) != 9:
            flash('Incorrect SSN', 'error')
        elif len(empName) < 3:
            flash('Incorrect Name', 'error')
        elif len(empPhone) != 10:
            flash('Incorrect Phone Number', 'error')
        elif len(empAddress) < 5:
            flash('Incorrect Address', 'error')
        elif len(empEmail) < 8:
            flash('Incorrect Email', 'error')
        elif len(empPass) < 3:
            flash('Incorrect Password', 'error')
        else:
            newEmp = Employee(SSN=ssn, Emp_Name=empName, Phone_Number=empPhone, Address=empAddress, Email=empEmail, Pass=empPass, Date_Of_Birth=empDateOfBirth)
            db.session.add(newEmp)
            db.session.commit()
            flash('Successfully Registered', 'success')

    return render_template("hire.html", user=current_user)


@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('auth.login'))
