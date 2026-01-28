
# Looping Marketplace

<p align="center">
  <img src="backend/static/images/suuuu5.png" alt="Looping Marketplace" width="600">
</p>



Looping Marketplace is a full web application designed for buying and selling products. It includes a complete CRUD system and is built using Django, PostgreSQL, Supabase, Python, and Bootstrap for the frontend. The platform also integrates Stripe as a payment gateway.

The application is fully functional for real use. Users can create an account and start browsing and purchasing products immediately. To become a seller, users must pay a one-time a fee, which unlocks the seller role and allows them to list and manage their own products.

## Current Features
- Full CRUD system for products
- User authentication and role management
- Buyer and seller account types
- Stripe payment integration
- PostgreSQL database with Supabase
- Responsive UI built with Bootstrap
- Marketplace ready for real transactions

## Future Enhancements
- Real-time chat between buyers and sellers
- Optional paid promotion for sellers to highlight products at the top of the marketplace
- Discount coupons for frequent buyers
- Automated notifications for:
  - Order updates
  - Chat messages
  - Low stock alerts
- Long-term goal: native mobile application

Looping Marketplace is designed to grow into a complete e-commerce ecosystem with advanced features for both buyers and sellers.



#### Comprehensive step-by-step instructions for installing and running the MarketPlace application.

## Requirements.
- Python 3.12+
- pip
- Docker Desktop
- Git

## Quick Start (Docker).

Repository.
[MarketPlace](https://github.com/Bootcamp-IA-P6/MarketPlace)

You do not need to clone the repository to run the application:
```bash
docker pull iruperth/looping:latest
docker run -d -p 8000:8000 iruperth/looping:latest
```

If you prefer to clone the repository and run it locally:

``` bash
git clone https://github.com/Bootcamp-IA-P6/MarketPlace.git
cd MarketPlace/backend
docker compose up --build
```

To run the containers in the background:

``` bash
docker compose up -d
```

# Run Locally.
## Create virtual environment.


### Mac / Linux
``` bash
cd backend
```

``` bash
python3 -m venv venv
```
``` bash
source venv/bin/activate
``` 
### Windows
``` bash
cd backend
```
``` bash
python -m venv venv
```
``` bash
venv\Scripts\activate
``` 
### Install dependencies.
``` bash
pip install -r requirements.txt
``` 
### Apply migrations.
``` bash
python manage.py migrate
``` 
### Run development server.
``` bash
python manage.py runserver
```

# Build and start containers with DOCKER.
``` bash
docker compose up --build
``` 
### Run in background.
``` bash
docker compose up -d
``` 
### Stop containers.
``` bash
docker compose down
``` 


<br>
<br>


## Contributing
We welcome contributions to improve Looping Marketplace.  
If you would like to collaborate, please create a pull request and our team will review it.

Thank you for your interest in the project.

<p align="center">
  <img src="backend/static/images/suuuu2.png" alt="Looping Marketplace" width="600">
</p>

