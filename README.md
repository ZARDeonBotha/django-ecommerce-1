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
- [Twitter API Integration](#twitter-api-integration)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [MariaDB Troubleshooting on Mac](#mariadb-troubleshooting-on-mac)
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
- Twitter API posting using OAuth 2.0 Bearer tokens (**required for posting; legacy keys supported for compatibility**)
- Responsive templates with Bootstrap

## Tech Stack

- Backend: Django 5.2 (Python 3.10+ recommended)
- Frontend: HTML5, Bootstrap, Django Templates
- Database: MySQL or MariaDB

## Setup Instructions

1. **Clone the repository**
    ```
    git clone https://github.com/ZARDeonBotha/django-ecommerce-1.git
    cd django-ecommerce-1
    ```

2. **Create and activate a Python virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate     # Linux/macOS
    venv\Scripts\activate        # Windows
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Create `.env` file at the project root**
   Example:
    ```
    SECRET_KEY=<your secret key>
    DEBUG=True
    EMAIL_HOST_USER=<your gmail address>
    EMAIL_HOST_PASSWORD=<your app/google password>
    # --- Twitter API v2 credentials ---
    TWITTER_BEARER_TOKEN=<your Twitter OAuth 2.0 Bearer token>        # REQUIRED for posting tweets/store announcements
    TWITTER_CLIENT_ID=<your Twitter Client ID>                        # For OAuth2 flows (optional)
    TWITTER_CLIENT_SECRET=<your Twitter Client Secret>                # For OAuth2 flows (optional)
    # --- Legacy keys (read-only endpoints/compatibility) ---
    TWITTER_CONSUMER_KEY=<your Twitter app key>
    TWITTER_CONSUMER_SECRET=<your Twitter app secret>
    TWITTER_ACCESS_TOKEN=<your Twitter access token>
    TWITTER_ACCESS_TOKEN_SECRET=<your Twitter access token secret>
    ```
    - All sensitive credentials are securely loaded from `.env` using python-dotenv.
    - Do **NOT** store this file in public repositories or version control.

## Environment Variables

Environment variables configured in the `.env` file provide secure authentication for email and Twitter API, preventing application errors and credential leaks.

**For Twitter API posting (write actions), you must use the OAuth 2.0 Bearer token. Twitter legacy keys are retained for compatibility with read-only endpoints.**

## Database Setup

- **Ensure MySQL/MariaDB is running.**

  On macOS (Homebrew):
    ```
    brew services start mariadb
    brew services list      # Confirm mariadb is 'started'
    ```
  On Windows (XAMPP/MAMP/etc.): Start MySQL from your control panel.

- **Create the database (if not already created)**
  Open a terminal and run:
    ```
    mysql -u admin -p -h 127.0.0.1 -P 3306
    # Then inside the MySQL prompt:
    CREATE DATABASE ecommerce_db;
    ```

- **Default configuration uses:**
    - database name: `ecommerce_db`
    - user: `admin`
    - password: `admin`  
      Update credentials in your `.env` or `settings.py` as needed.

- **Run Django migrations (from project folder)**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

- **Create an admin/superuser**
    ```
    python manage.py createsuperuser
    ```

## Running the Application

1. **Collect static files**
    ```
    python manage.py collectstatic
    ```

2. **Start the local server**
    ```
    python manage.py runserver
    ```

3. **Visit**
    ```
    http://localhost:8000/
    ```

## Twitter API Integration

- The application supports posting new store/products to Twitter/X using the official Twitter API v2.
- **For posting tweets (write actions), you MUST use the Bearer token (`TWITTER_BEARER_TOKEN`)—legacy OAuth 1.0A keys will not work for new apps.**
- Enable `tweet.write` scope and OAuth 2.0 for your Twitter app at https://developer.x.com/.
- For compatibility, legacy keys may be retained for read-only endpoints (getting user/profile data).
- If you encounter a 403 error, confirm you are using your Bearer token and have set correct permissions/scopes in your Twitter developer portal.

**References:**
- [Devcommunity Twitter OAuth Guide](https://devcommunity.x.com/t/cannot-set-permissions-and-enable-oauth-1-0-on-twitter-to-create-a-bot/175901/3)

## Common Issues & Troubleshooting

- **OAuth/Twitter errors:**
    - Ensure `.env` contains your Bearer token (`TWITTER_BEARER_TOKEN`) and you are using OAuth 2.0.
    - 403 errors on posting often mean you are using old OAuth credentials or missing `tweet.write` permissions.
    - For read-only API endpoints, legacy keys are still supported.

- **Email errors:**  
  Make sure your credentials (user/password) are valid and less secure apps are enabled if needed.

- **Database errors:**  
  Double-check the credentials, ensure your database service is running, and confirm the database exists.

- **Missing migrations:**  
  If you see model errors, run makemigrations/migrate again.

- **Static/media problems:**  
  Confirm you collected static files and your MEDIA_URL and MEDIA_ROOT are correct.

---

## MariaDB Troubleshooting on Mac

If you get errors such as "Can't connect to MySQL server" or "Access denied for user ...", follow these recovery steps:

### Fixing Startup and Password Issues

1. **Stop MariaDB completely:**
    ```
    brew services stop mariadb
    ps aux | grep mysql
    ps aux | grep mariadbd
    sudo kill -9 <PID>
    ```

2. **Remove stale lock and pid files:**
    ```
    sudo rm -f /usr/local/var/mysql/*.pid
    sudo rm -f /usr/local/var/mysql/aria_log_control*
    ```

3. **Start MariaDB in safe mode (skip grant tables):**
    ```
    sudo mysqld_safe --skip-grant-tables &
    ```
   *(Open a new terminal window for the next command)*

4. **Connect as root (no password needed):**
    ```
    mysql -u root
    ```
   *(if you get a socket error, try: `mysql -u root --socket=/usr/local/var/mysql/mysql.sock`)*

5. **At the MariaDB prompt, reset credentials and create the database:**
    ```
    FLUSH PRIVILEGES;
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
    CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
    GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
    CREATE DATABASE IF NOT EXISTS ecommerce_db;
    FLUSH PRIVILEGES;
    ```
   *(If `ALTER USER` fails, use: `SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root');`)*

6. **Exit MariaDB and kill the safe server process:**
    ```
    exit
    ps aux | grep mysqld
    sudo kill -9 <PID>
    ```

7. **Restart MariaDB normally:**
    ```
    brew services start mariadb
    ```

8. **Test login with the new password**
    ```
    mysql -u root -p
    # Enter password: root

    mysql -u admin -p
    # Enter password: admin
    ```
   You should see the `ecommerce_db` database.

---

## License

This project is for educational use only as part of the HyperionDev curriculum.

---