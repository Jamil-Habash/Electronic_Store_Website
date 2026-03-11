create database electronic_store;
use electronic_store;
drop database electronic_store;

create table Employee(
SSN varchar(32) unique not Null, 
Employee_ID Int PRIMARY KEY auto_increment not Null,
Emp_Name varchar(32),
Phone_Number varchar(15),
Address varchar(100),
Email varchar(100) unique not null,
Date_Of_Birth date,
Pass varchar(100) not NUll,
Salary float not NUll
 );
 
CREATE TABLE Company (
Company_ID INT PRIMARY KEY auto_increment not Null,
Company_Name VARCHAR(50),
Address VARCHAR(100),
mail VARCHAR(100)
);

CREATE TABLE Model (
Model_ID INT PRIMARY KEY auto_increment not Null,
Model_Name VARCHAR(50),
Manufacture_Date DATE,
Company_ID INT,
FOREIGN KEY (Company_ID) REFERENCES Company(Company_ID) ON UPDATE CASCADE
);

CREATE TABLE Inventory_Record (
Record_ID INT,
Model_ID INT,
Quantity INT,
primary key(Model_ID, Record_ID),
FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID) ON UPDATE CASCADE
);

CREATE TABLE Product (
Product_ID INT PRIMARY KEY auto_increment not Null,
Price FLOAT,
Product_Type VARCHAR(50),
Warranty INT,
Model_ID INT,
FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID) ON UPDATE CASCADE
);

CREATE TABLE Customer (
Customer_ID INT PRIMARY KEY auto_increment not Null, 
Phone_Number VARCHAR(15),
Address VARCHAR(100),
Full_Name VARCHAR(100)
);

CREATE TABLE Orders(
Order_ID INT PRIMARY KEY auto_increment not Null,
Customer_ID INT,
Employee_ID INT,
Total_Price FLOAT,
Payment_Method VARCHAR(50),
Date_Of_Order DATE,
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON UPDATE CASCADE,
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON UPDATE CASCADE
);
 
CREATE TABLE Order_Details (
Order_ID INT,
Product_ID INT,
Discount DECIMAL(5, 2),
PRIMARY KEY (Order_ID, Product_ID),
FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID) ON DELETE CASCADE,
FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID) ON DELETE CASCADE
);

CREATE TABLE Purchase (
Purchase_ID INT PRIMARY KEY auto_increment not Null,
Employee_ID INT,
Date_Of_Purchase DATE,
Total_Cost FLOAT,
Payment_Method VARCHAR(50),
Tax DECIMAL(5, 2),
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON UPDATE CASCADE
);

CREATE TABLE Purchase_Detail (
Purchase_ID INT,
Model_ID INT,
Quantity INT,
Cost_Per_Unit FLOAT,
PRIMARY KEY (Purchase_ID, Model_ID),
FOREIGN KEY (Purchase_ID) REFERENCES Purchase(Purchase_ID) ON DELETE CASCADE,
FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID) ON DELETE CASCADE
);

insert into Employee (SSN, Emp_Name, Phone_Number, Address, Email, Date_Of_Birth, Pass, Salary) 
values
("913123131", "jamil", "0593421232", "al tirah","manager@outlook.com","2004-10-1","123","4000"),
("913856722", "hanna", "0597129371", "3en minged","emp1@outlook.com","2004-1-1","567","5000"),
("123456789", "John Doe", "0501122334", "New York, NY", "john.doe@example.com", "1990-05-15", "password123", 4500),
("987654321", "Jane Smith", "0502233445", "Los Angeles, CA", "jane.smith@example.com", "1985-08-22", "password456", 5200),
("112233445", "Michael Brown", "0503344556", "Chicago, IL", "michael.brown@example.com", "1992-12-10", "password789", 4800),
("556677889", "Emily White", "0504455667", "Miami, FL", "emily.white@example.com", "1991-03-25", "password101", 5100),
("998877665", "David Green", "0505566778", "Houston, TX", "david.green@example.com", "1988-06-30", "password202", 4700);
select * from employee;
ALTER TABLE Employee AUTO_INCREMENT = 0;
delete from employee
where employee_id = 3;
