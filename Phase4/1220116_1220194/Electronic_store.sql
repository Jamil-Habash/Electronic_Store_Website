create database electronic_store;
use electronic_store;
drop database electronic_store;

CREATE TABLE Employee(
    Employee_ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone_Number VARCHAR(15) UNIQUE,
    Address VARCHAR(100),
	Pass VARCHAR(100) NOT NULL,
    Emp_Name VARCHAR(32),
    Date_Of_Birth DATE,
    Salary FLOAT NOT NULL
);
 CREATE TABLE Customer(
    Customer_ID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Full_Name VARCHAR(100),
	Email VARCHAR(50) UNIQUE,
    Phone_Number VARCHAR(15) UNIQUE,
    Address VARCHAR(100),
	Pass VARCHAR(50)
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
Model_ID INT primary key,
Quantity INT,
FOREIGN KEY (Model_ID) REFERENCES Model(Model_ID) ON UPDATE CASCADE on delete cascade
);

CREATE TABLE Product (
Product_ID INT PRIMARY KEY not Null,
Price FLOAT,
Product_Type VARCHAR(50),
Warranty INT,
Picture longblob,
Descriptions varchar(1000),
FOREIGN KEY (Product_ID) REFERENCES Model(Model_ID) ON UPDATE CASCADE on delete cascade
);
CREATE TABLE PAYMENT(
Order_ID int PRIMARY KEY not Null,
Payment_Method VARCHAR(50),
Payment_Identifier VARCHAR(50),
Payment_Key VARCHAR(50),
FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID ) ON UPDATE CASCADE on delete cascade
);
CREATE TABLE Orders(
Order_ID INT PRIMARY KEY auto_increment not Null,
Customer_ID INT,
Employee_ID INT,
Total_Price FLOAT,
Date_Of_Order DATE,
FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON UPDATE CASCADE,
FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID) ON UPDATE CASCADE
);
 
CREATE TABLE Order_Details (
Order_ID INT,
Product_ID INT,
Discount DECIMAL(5, 2),
quantity int,
PRIMARY KEY (Order_ID, Product_ID),
FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID) ON DELETE CASCADE,
FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID) ON DELETE CASCADE
);

CREATE TABLE Purchase (
Purchase_ID INT PRIMARY KEY auto_increment not Null,
Employee_ID INT,
Date_Of_Purchase DATE,
Total_Cost FLOAT,
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

INSERT INTO Employee (Email, Phone_Number, Address, Pass, Emp_Name, Date_Of_Birth, Salary) VALUES
('manager@outlook.com', '1234567890', '123 Elm Street', '123', 'abdallah-jamil', '1990-05-15', 5000.00),
('jane.smith@example.com', '2345678901', '456 Oak Avenue', 'securePass!', 'Jane Smith', '1985-09-20', 6200.00),
('michael.brown@example.com', '3456789012', '789 Pine Road', 'mikePass!', 'Michael Brown', '1992-03-10', 4700.00),
('emily.johnson@example.com', '4567890123', '321 Maple Lane', 'emily2024', 'Emily Johnson', '1988-07-25', 5300.00),
('william.lee@example.com', '5678901234', '654 Cedar Blvd', 'lee@123', 'William Lee', '1995-12-12', 5800.00);
INSERT INTO Customer (Full_Name, Email, Phone_Number, Address, Pass) VALUES
('Alice Walker', 'alice.walker@example.com', '9876543210', '12 Birch Street', 'alicePwd'),
('Bob Martin', 'bob.martin@example.com', '8765432109', '34 Spruce Ave', 'bobSecure'),
('Catherine Green', 'c.green@example.com', '7654321098', '56 Willow Dr', 'catPass'),
('Daniel White', 'daniel.white@example.com', '6543210987', '78 Aspen Blvd', 'daniel123'),
('Eva Black', 'eva.black@example.com', '5432109876', '90 Poplar Lane', 'evaSecure!');

INSERT INTO Company (Company_Name, Address, mail) VALUES
('Dell', '1 Dell Way, Round Rock, TX', 'support@dell.com'),
('HP', '1501 Page Mill Rd, Palo Alto, CA', 'support@hp.com'),
('Lenovo', '8001 Development Dr, Morrisville, NC', 'support@lenovo.com'),
('Apple', '1 Apple Park Way, Cupertino, CA', 'support@apple.com');

-- Insert models
INSERT INTO Model (Model_Name, Manufacture_Date, Company_ID) VALUES
('Inspiron 15', '2023-08-01', 1),
('XPS 13', '2024-01-15', 1),
('Pavilion 14', '2023-09-10', 2),
('Envy 13', '2024-02-25', 2),
('ThinkPad X1 Carbon', '2023-11-05', 3),
('IdeaPad 5', '2024-03-12', 3),
('MacBook Air M2', '2024-04-10', 4),
('MacBook Pro 14', '2024-01-20', 4);

INSERT INTO Model (Model_Name, Manufacture_Date, Company_ID) VALUES
('Asus ROG', '2023-08-01', 1),
('Lenovo Ideapad 3', '2024-08-01', 1),
('Samsung 15 AI Book 4', '2025-08-01', 2),
('Asus Tuf F15', '2022-08-01', 3);
INSERT INTO Orders (Customer_ID, Employee_ID, Total_Price, Date_Of_Order) VALUES
(1, 1, 7400, '2025-06-01'),
(2, 2, 14000, '2025-06-02'),
(3, 3, 4800, '2025-06-03'),
(4, 1, 800, '2025-06-03'),
(5, 4, 300, '2025-06-04');
INSERT INTO PAYMENT (Order_ID, Payment_Method, Payment_Identifier, Payment_Key) VALUES
(1, 'Credit Card', '1475874898374657', '987'),
(2, 'PayPal', 'henry@outlook.com', '12314214'),
(3, 'PayPal', 'emad@outlook.com', '123tf214'),
(4, 'Credit Card', '1475874898374657', '123'),
(5, 'Credit Card', '1475074898374657', '287');
INSERT INTO Order_Details (Order_ID, Product_ID, Quantity, Discount) VALUES
(1, 1, 2, 0.00),
(1, 2, 5, 30.00),
(2, 5, 10, 0.00),
(3, 2, 4, 40),
(4, 3, 1, 0.00),
(5, 4, 2, 0.00);
INSERT INTO Inventory_Record (Model_ID,Quantity) VALUES
(1,200),(2,400),(3,100),(4,100),(5,20),(6,4),(7,200),(8,50);
INSERT INTO Purchase_Detail (Purchase_ID, Model_ID, Quantity, Cost_Per_Unit) VALUES
(1, 1, 202, 500.00),
(1, 2, 409, 1000.00),
(2, 3, 301, 600),
(2, 4, 102, 1300),
(2, 5, 30, 1200),
(3, 6, 4, 600.00),
(3, 7, 200, 1100.00),
(3, 8, 50, 1900.00);
INSERT INTO Purchase (Employee_ID, Date_Of_Purchase, Total_Cost) VALUES
(1, '2024-06-01', 510000),
(2, '2024-06-02', 349200),
(3, '2024-06-03', 317400);

select * from customer;
select * from employee;
select * from product;
select * from  Order_Details;
select * from  Model;
select * from  orders;
select * from  PAYMENT;
select * from  Inventory_Record;
select * from Order_Details;
select * from Purchase;
select * from Purchase_Detail;




delete from Customer where Customer_ID > 0;
delete from orders where Order_ID > 0;
delete from Employee where Employee_ID>0;
delete from model where Model_ID>0;
delete from product where  Product_ID=9;
delete from Inventory_Record where Model_ID = 9;
delete from Order_Details where Order_ID > 0;
delete from Purchase where Purchase_ID = 7;

ALTER TABLE Employee DROP COLUMN SSN;
ALTER TABLE Order_Details add quantity int after Discount;
ALTER TABLE Customer add Email varchar(50) after Full_Name;
ALTER TABLE product add Descriptions varchar(1000) after Picture;
ALTER TABLE customer add pass varchar(50) after Email;
ALTER TABLE Product MODIFY Picture LONGBLOB;
ALTER TABLE Employee AUTO_INCREMENT = 0;
ALTER TABLE  Product AUTO_INCREMENT = 0;
ALTER TABLE  orders AUTO_INCREMENT = 0;
ALTER TABLE  customer AUTO_INCREMENT = 0;
ALTER TABLE  Model AUTO_INCREMENT = 0;
ALTER TABLE Inventory_Record AUTO_INCREMENT = 0;
DROP TABLE Purchase ;
