# Django E-Commerce Application

A robust Django-based e-commerce platform built for the HyperionDev practical assignment (Parts 1 & 2).

---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [License](#license)

---

## Project Description

This web application enables vendors to manage stores and products, while buyers can browse, add to cart, and order. It demonstrates modern Django best practices, secure credential handling, and enterprise-style project architecture.

## Features

- User registration and authentication for Vendors & Buyers
- Vendor: manage stores and products
- Buyer: manage cart and place orders
- Role-based navigation and security
- Database-backed using MySQL or MariaDB
- SMTP/Email integration for notifications
- (Optional) Twitter API posting using OAuth credentials
- Responsive templates with Bootstrap

## Tech Stack

- Backend: Django 5.2 (Python 3.10+ recommended)
- Frontend: HTML5, Bootstrap, Django Templates
- Database: MySQL or MariaDB

## Setup Instructions

1. **Clone the repository**
   git clone https://github.com/ZARDeonBotha/django-ecommerce-1.git

    cd django-ecommerce-1
3. **Python virtual environment**
   python -m venv venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate # Windows
3. **Install dependencies**
   pip install -r requirements.txt
4. **Create .env file**

At the project root, create a `.env` file with:
SECRET_KEY=<your secret key>
DEBUG=True
EMAIL_HOST_USER=<your gmail address>
EMAIL_HOST_PASSWORD=<your app/google password>
TWITTER_CONSUMER_KEY=<your Twitter app key>
TWITTER_CONSUMER_SECRET=<your Twitter app secret>
TWITTER_ACCESS_TOKEN=<your Twitter access token>
TWITTER_ACCESS_TOKEN_SECRET=<your Twitter access token secret>

- All sensitive credentials are securely loaded from `.env` using python-dotenv.
- Do **NOT** store this file in public repositories or version control.

## Environment Variables

Environment variables configured in the `.env` file provide secure authentication for email and Twitter API, preventing application errors and credential leaks.

## Database Setup

- Ensure MySQL/MariaDB is running.
- Default configuration uses:
- database name: `ecommerce_db`
- user: `admin`
- password: `admin`
- Update credentials as needed in your `.env` or `settings.py`.
- Run migrations:
  python manage.py makemigrations
  python manage.py migrate

- Create an admin/superuser:
  python manage.py createsuperuser

## Running the Application

1. **Collect static files**
   python manage.py collectstatic

2. **Start the local server**
   python manage.py runserver

3. **Visit**
   http://localhost:8000/

## Common Issues & Troubleshooting

- **OAuth/Email errors:**  
  Make sure the `.env` file is created and all required keys have valid values (not empty or None).
- **Database issues:**  
  Double-check the credentials and ensure your database service is running properly.
- **Missing migrations:**  
  If you see model errors, run makemigrations/migrate again.
- **Static/media problems:**  
  Confirm you collected static files and your MEDIA_URL and MEDIA_ROOT are correct.

## License

This project is for educational use only as part of the HyperionDev curriculum.

---
