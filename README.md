# Book Store – Online Book Selling System

Book Store is an e-commerce web project for selling books, developed with Django. The system allows users to browse books, place orders, and pay online.

---

## Technologies Used

- **Backend:** Django 5.1.2
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** MySQL
- **Payment:** Stripe API
- **Authentication:** Django Authentication System
- **Live Chat:** Tawk.to Chat API
- **Translation Management:** Django Rosetta

---

## Project Structure

```
Team-Book-Deh-New/
├── accounts/         # User management (registration, login, profile)
├── carts/            # Shopping cart management
├── category/         # Book categories
├── orders/           # Order processing and payment
├── store/            # Product and store interface
├── templates/        # HTML templates
├── static/           # Static resources (CSS, JS, images)
├── media/            # Uploaded product images
├── locale/           # Translation files for multi-language support
├── backup/           # Database backup files
├── manage.py         # Django management script
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (API keys, secrets)
├── README.md         # Project documentation
└── .vscode/          # VS Code settings
```

---

## Main Features

- **User Management:** Register, login, logout, profile, shipping addresses, password reset
- **Product Management:** Browse/search books, categories, product details, ratings, reviews
- **Shopping Cart:** Add/update/remove products, total calculation
- **Orders & Payment:** Shipping info, Stripe payment, secure processing, order tracking
- **Additional:** Wishlist, order history, user dashboard, featured carousel, responsive design

---

## Shopping Process

1. User registers/logs in
2. Browses products and adds to cart
3. Views cart and proceeds to checkout
4. Enters shipping information
5. Selects payment method (Stripe)
6. Completes payment
7. Receives order confirmation
8. Tracks order status

---

## Setup & Run

1. **Clone the repository**
    ```sh
    git clone <repository-url>
    cd Book-Store-DH
    ```

2. **Create virtual environment & install dependencies**
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux

    pip install -r requirements.txt
    ```

3. **Setup the database**
    ```sh
    python manage.py migrate
    ```

4. **Create admin account**
    ```sh
    python manage.py createsuperuser
    ```

5. **Run the server**
    ```sh
    python manage.py runserver
    ```

6. **Access the system**
    - Home: http://127.0.0.1:8000/
    - Admin: http://127.0.0.1:8000/admin/

---

## Stripe Payment Configuration

- Register at: https://stripe.com
- Get your API keys from the Stripe Dashboard
- Add the keys to your `.env` file or `settings.py`:
    ```
    STRIPE_PUBLISHABLE_KEY = 'your-publishable-key'
    STRIPE_SECRET_KEY = 'your-secret-key'
    ```

---

## Multi-language Support

This project supports English and Japanese. Users can switch languages using the language selector in the navigation bar. All translations are managed with Django’s internationalization framework.

---

**Contact:**  
- Email: cskh@bookstore.com.vn  
- Address: 43 Luu Huu Phuoc, Nam Tu Liem, Hanoi, Vietnam

---

> Copyright © Vietnam Japan University.
