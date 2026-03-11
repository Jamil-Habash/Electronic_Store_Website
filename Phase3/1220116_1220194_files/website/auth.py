from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Employee
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
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', 'error')
        else:
            flash('Email does not exist.', 'error')
    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('auth.login'))
