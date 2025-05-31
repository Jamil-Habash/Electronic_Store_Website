from flask import Blueprint, render_template, request, flash
from .models import Employee
from . import db
from flask_login import current_user

employee = Blueprint('employee', __name__)

@employee.route('/empManager')
def employee_manager():
    employees = Employee.query.all()
    return render_template("employee.html", user=current_user, employees=employees)


@employee.route('/add_employee', methods=['GET', 'POST'])
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


@employee.route('/update_employee', methods=['GET', 'POST'])
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

@employee.route('/delete_employee', methods=['GET', 'POST'])
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