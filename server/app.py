
#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, session
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_all_restaurants():

    restaurants = Restaurant.query.all()

    dict = [restaurant.to_dict() for restaurant in restaurants]
    return make_response(jsonify(dict)), 200

@app.route('/restaurants/<int:id>', methods=['GET'])

def get(id):
    restaurant_by_id = Restaurant.query.filter(Restaurant.id==id).first()
    if not restaurant_by_id:
        return {'error': 'Restaurant not found'}, 404
    
    restaurant_to_dict = restaurant_by_id.to_dict()

    restaurant_to_dict['restaurant_pizzas'] = [{
        'id': rp.id,
        'price': rp.price,
        'pizza_id': rp.pizza_id,
        'restaurant_id': rp.restaurant_id,
        'pizza': {
            'id': rp.pizza.id,
            'ingredients': rp.pizza.ingredients,
            'name': rp.pizza.name  
        }
        

    }for rp in restaurant_by_id.restaurantPizza]

    return jsonify(restaurant_to_dict), 200


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_by_id(id):
    selected_restaurant = Restaurant.query.filter(Restaurant.id==id).first()
    if not selected_restaurant:
        return {'error', 'Restaurant not found'}, 404
    
    db.session.delete(selected_restaurant)
    db.session.commit()

    return {}, 204

@app.route('/pizzas')
def get_pizzas():

    return [pizza.to_dict() for pizza in Pizza.query.all() ]


    
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

   
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    
    errors = []

    if not price or  not pizza_id or not restaurant_id:
    
        errors.append('Missing required fields: price, pizza_id, restaurant_id.')

    if not isinstance(price, int) or price < 1 or price > 30:
        errors.append('Price must be anumber between 1 and 30.')
    
    if not isinstance(pizza_id, int):
        errors.append('Pizza ID must be an integer.')
    if not isinstance(restaurant_id, int):
        errors.append('Restaurant ID must be an integer.')

    
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)
    if not pizza:
        errors.append(f'Pizza with id {pizza_id} does not exist.')
    if not restaurant:
        errors.append(f'Restaurant with id {restaurant_id} does not exist.')

    if errors:
        return {'errors': ['validation errors']}, 400

    try:
        
        restaurant_pizza = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(restaurant_pizza)
        db.session.commit()

        
        response = {
            "id": restaurant_pizza.id,
            "pizza": {
                "id": pizza.id,
                "ingredients": pizza.ingredients,
                "name": pizza.name
            },
            "pizza_id": pizza_id,
            "price": price,
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            },
            "restaurant_id": restaurant_id
        }

        return jsonify(response), 201

    except Exception as e:
        db.session.rollback()
        return {'errors': ['validation errors']}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)

































# #!/usr/bin/env python3
# from models import db, Restaurant, RestaurantPizza, Pizza
# from flask_migrate import Migrate
# from flask import Flask, request, make_response
# from flask_restful import Api, Resource
# import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# api = Api(app)


# @app.route("/")
# def index():
#     return "<h1>Code challenge</h1>"


# if __name__ == "__main__":
#     app.run(port=5555, debug=True)
