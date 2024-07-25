# MedeeKart [LIVE](https://medeekart-i87e.onrender.com)

This project is an online medicine store developed using Django. Users can register, login, view a list of featured and categorized medicines, add medicines to their cart, and make purchases using the PayU payment gateway.

## Deployment


  -The project is deployed on the  [here](https://medeekart-i87e.onrender.com) using render.
  -The database postgresql is connected at the deployment.
  
## Features

- User registration and authentication
- View and search for medicines categorized as Fever, Diabetes, Wellness & Fitness, Skincare, Babycare, etc.
- Add medicines to the cart
- Checkout and make payments using PayU

## Installation

### Prerequisites

- Python 3.x
- Django 3.x or higher
- paywix
- Virtualenv (optional but recommended)
- PayU account for payment gateway integration

### Setup

1. **Clone the repository**

    ```sh
    git clone https://github.com/yourusername/django-medicine-store.git
    cd medeekart
    cd iwt
    ```

2. **Create and activate a virtual environment**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**

    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**

    ```sh
    python manage.py runserver
    ```

## Usage

1. **Access the application**

   Open your web browser and go to `http://127.0.0.1:8000/`.

2. **Register and log in**

   Create a new account or log in with your existing credentials.

3. **Browse medicines**

   Browse through the list of featured and categorized medicines.

4. **Add to cart**

   Add desired medicines to your cart.

5. **Checkout**

   Proceed to checkout and complete the payment using PayU.
6. **Test cards for Payments**

    The Payment testing credentials can be used from [here](https://docs.payu.in/docs/test-cards-upi-id-and-wallets)

## Project Structure

    .
    ├── manage.py
    ├── iwt(medicine_store medee)
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── requirements.txt
    ── app(app_name)
       ├── migrations
       ├── static
       ├── templates
       ├── __init__.py
       ├── admin.py
       ├── apps.py
       ├── models.py
       ├── tests.py
       ├── views.py
       └── urls.py
  

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.



