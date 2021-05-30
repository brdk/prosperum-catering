Pre-requirements
================
1. install `docker-compose`
2. python 3.7+ is required

Setup
=====
1. run `docker-compose up` to up PostgreSQL and RabbitMQ services  
2. create python virtual environment
3. run `pip install -r requirements.txt` to install all requirements 
4. run `./manage.py migrate` to apply migrations
5. run `./manage.py loaddata data.json` to load initial data from fixtures
6. run `./manage.py runserver` to start server
7. run `./manage.py createsuperuser` to create a super user (optionally)

API Endpoints
=============
1. `http://127.0.0.1:8000/api/cities/` - list of cities (CRUD)
2. `http://127.0.0.1:8000/api/restaurant-types/` - types of restaurants (CRUD)
3. `http://127.0.0.1:8000/api/ingredients/` - ingredients to cook dishes and make different beverages (CRUD)
4. `http://127.0.0.1:8000/api/portions/` - dishes and beverages (CRUD)
   `http://127.0.0.1:8000/api/portions/top/<N>` - top dishes and beverages based on how many times they were ordered
   Available filters:
   - `restaurant` - name of restaurant where dishes/beverages were ordered
   - `name` - name of dish/beverage
   - `date` - a date when dishes/beverages were ordered
   - `price_min` - filter out dishes/beverages with price lower than defined
   - `price_max` - filter out dishes/beverages with price higher than defined
   - `dish_type` - one of: Beef, Chicken, Pork, Vegetarian, Vegan
5. `http://127.0.0.1:8000/api/restaurants/` - restaurants
   `http://127.0.0.1:8000/api/restaurants/<ID>/guests/` - get all guests visited a restaurant 
   `http://127.0.0.1:8000/api/restaurants/<ID>/guests/notify/<DATE>/` - GET request. Notifies all guests who visited a restaurant on a selected date. Date format: yyyy-mm-dd 
   `http://127.0.0.1:8000/api/restaurants/<ID>/menu/` - get available dishes/beverages in a restaurant. The same filters as for `/api/portions/` might be applied
6. `http://127.0.0.1:8000/api/guests/` - list of all guest (beware: no pagination)
7. `http://127.0.0.1:8000/api/orders/` - list of all orders
   `http://127.0.0.1:8000/api/orders/total/` - total amount of all orders
    Available filters:
   - `restaurant` - name of restaurant where dishes/beverages were ordered
   - `name` - name of dish/beverage
   - `date` - a date when dishes/beverages were ordered
   - `price_min` - filter out dishes/beverages with price lower than defined
   - `price_max` - filter out dishes/beverages with price higher than defined
   - `dish_type` - one of: Beef, Chicken, Pork, Vegetarian, Vegan
    
How to create a new order
=========================
1. create a guest using a POST request to `http://127.0.0.1:8000/api/guests/`.  
   Required fields are: first name, last name, email, address
2. do a POST request to `http://127.0.0.1:8000/api/orders/`.  
   Required fields are:  
   - ordered_portions  
   - guest (guest id from the step 1)
   - restaurant (restaurant id)