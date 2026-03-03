# 🛒 Shopnow (E‑Kart) – Django E‑Commerce Web Application

![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Django Version](https://img.shields.io/badge/django-5.1.4-green)
![Database](https://img.shields.io/badge/database-MySQL-orange)
![Payment Gateway](https://img.shields.io/badge/payments-Razorpay-blueviolet)

**Shopnow (E‑Kart)** is a full‑stack, production-ready e‑commerce web application built using the **Django** framework. It provides a complete shopping experience, allowing users to register, log in, browse products by category, manage their shopping cart, and securely place orders using the Razorpay payment gateway. 

The project strictly adheres to Django’s **MTV (Model‑Template‑View)** architecture and uses Bootstrap 5 and Axios to deliver a responsive, dynamic frontend.

---


## 🚀 Key Features

### 👤 User Management
- Secure user registration, login, and logout.
- Forgot Password functionality.
- Dedicated user profile to view order history.

### 🛍️ Product Catalog
- Dynamic product listing with clear pricing and unit details.
- Categorized browsing (Fruits, Vegetables, Groceries, etc.).
- Image handling via Django Media.
- Search functionality to quickly find products.

### 🛒 Dynamic Cart System
- AJAX-powered Add to Cart functionality (no page reloads).
- Real-time cart quantity updates (+/- controls).
- Automatic calculation of delivery and handling charges based on the cart total.

### 💳 Secure Payments & Checkout
- **Razorpay** payment gateway integration.
- Secure online transaction handling and verification.
- Order creation only upon successful payment verification.

### 📦 Order Tracking
- Detailed order history accessible to users.
- Order status tracking (Pending, Paid, Completed, etc.).
- Admin capabilities to view and manage all orders.


---

## 🧰 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.11, Django 5.1.4 |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript (Axios for AJAX) |
| **Database** | MySQL (configured via `django-environ`) |
| **Payment Gateway** | Razorpay API |
| **Authentication** | Django Auth System |

---

## 🧠 Architecture Used

- **MTV (Model-Template-View)**
- AJAX-based client–server communication using **Axios**
- REST-style Django views for cart & order actions
- Separation of concerns between UI, logic, and data
- Secure authentication & CSRF protection
 
---


# 📁 Project Structure

```
Shopnow/
│
├── apps/
│   └── shop/                  # Core application (Models, Views, URLs, Forms)
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       ├── views.py
│       │
│       ├── migrations/
│       │   └── __init__.py
│       │
│       └── templatetags/
│           └── custom_tags.py
│
├── config/                  # Django project configuration & settings
│   ├── __init__.py
│   ├── urls.py              # Project routing
│   ├── wsgi.py              # WSGI entrypoint
│   │
│   └── settings/            # Django settings module
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── media/
│   ├── images/
│   └── media/
│       └── images/
│
├── static/                  # CSS, JavaScript (Axios logic), and UI assets
│
├── template/                # Global HTML Templates (Bootstrap components)
│
├── .gitignore
├── README.md
├── manage.py                # Django project launcher
└── requirements.txt         # Dependencies list

```

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your machine:
- **Python 3.10+**
- **MySQL Server** (Running locally or remotely)
- **Git**

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone [https://github.com/Sairaj-25/django_shopnow.git](https://github.com/Sairaj-25/django_shopnow.git)
cd django_shopnow
```

### 2. Set up a Virtual Environment
- Isolate your project dependencies:

```bash
python -m venv venv
```
- Windows
```
venv\Scripts\activate
```

- macOS / Linux
```
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
- Create a .env file in the root directory (alongside manage.py) and add your database credentials and API keys:


```
# Django Settings
DJANGO_SECRET_KEY="your-super-secret-django-key"
DEBUG=True

# Database Configuration (MySQL)
DB_NAME="your_db_name"
DB_USER="root"
DB_PASSWORD="your_db_password"
DB_HOST="127.0.0.1"
DB_PORT="3306"

# Razorpay API Keys
RAZOR_KEY_ID="your_razorpay_key_id"
RAZOR_KEY_SECRET="your_razorpay_key_secret"
```

### 5. Create Database
- Make sure you create the corresponding MySQL database (DB_NAME) on your MySQL server before running migrations.
```
CREATE DATABASE your_db_name;
```

### 6. Apply Migrations
- Initialize the database and apply the schema:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### 7. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```
```
Open your browser and navigate to: http://127.0.0.1:8000/
```


## 🔐 Admin Panel
- Access the Django admin dashboard at:
```
http://127.0.0.1:8000/admin/
```

- From here, you can:

- Add and manage Products & Categories.

- Monitor incoming Orders and Payments.

- Manage Users and Customers.

---


## 🔁 Project Flow (Step‑by‑Step)

### 1️⃣ User Registration Flow

```
User → Register Page → Form Validation → User Created → Redirect to Home
```

### 2️⃣ User Login Flow

```
User → Login Page → Credentials Check → Session Created → Home Page
```

### 3️⃣ Browse Products Flow

```
User → Home Page → Product List → Product Card → Price & Unit Display
```

### 4️⃣ Add to Cart Flow

```
User → Click Add to Cart → Product ID Captured → Cart Updated → Quantity Control
```

### 5️⃣ Payment & Order Flow

```
User → Checkout → Razorpay Payment → Payment Verification → Order Created → Order History Updated (MySQL)
```

### 6️⃣ Logout Flow

```
User → Logout → Session Destroyed → Redirect to Home
```
---

## 📈 Future Enhancements

* Invoice generation (PDF)
* Order cancellation & refunds
* REST API for mobile app
* Docker & cloud deployment (AWS)
* Advanced sales analytics dashboard


---

## 👨‍💻 Author

**Sairaj Jadhav**

---
