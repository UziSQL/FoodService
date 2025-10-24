FoodService

FoodService is a backend web application designed to minimize food waste by enabling users to buy unsold food from restaurants at discounted prices.
The system provides authentication, product management, order processing, and administrative functionality.
It is built with FastAPI, PostgreSQL, and Docker for scalability and reliability.

Overview

FoodService allows two types of users — buyers and sellers.
Sellers can list available food products, while buyers can purchase them using the integrated checkout flow.
The application includes an admin interface for managing users, products, and orders.

Features

User authentication and registration with JWT-based security

Role-based access control (buyer, seller, admin)

Product creation, editing, and deletion

Order creation and checkout system

Administrative panel for managing data

Full Docker containerization for deployment

Technology Stack
Component	Technology
Backend Framework	FastAPI (Python 3.12)
Database	PostgreSQL
ORM	SQLAlchemy
Templates	Jinja2
Authentication	OAuth2 with JWT
Password Hashing	Passlib (bcrypt)
Deployment	Docker and docker-compose