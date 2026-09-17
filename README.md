# Electronic Store — Flask Web Application

A full-stack web application for an electronics store built with Flask and MySQL. It supports two separate user roles — customers and employees — each with their own interface and functionality.

## How It Was Made

Built with Flask using the Blueprint pattern to separate customer-facing views, authentication, and employee control into distinct modules. SQLAlchemy is used as the ORM with a MySQL backend. Flask-Login handles session management with role-aware user loading (customer vs. employee). The frontend uses Jinja2 templates with separate base layouts for customers and the employee dashboard.

## Features

**Customer side**
- Browse products with search, product detail pages, and best-selling/new arrivals sections on the home page
- Add to cart with stock validation, checkout, and payment
- Order history and profile management

**Employee side**
- Dashboard with store analytics
- Inventory management
- Purchase orders (restocking)
- Order approval and management
- Employee management (add, update, delete)

## Tech Stack

- Python / Flask
- MySQL with SQLAlchemy ORM
- Flask-Login for authentication
- Jinja2 templates
