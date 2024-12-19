
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')
    restaurantPizza = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan', overlaps="pizzas,restaurants")

    # add serialization rules
    serialize_only = ('address', 'id', 'name')

    def to_dict(self):
        return {
            'address': self.address,
            'id': self.id,
            'name': self.name
            
        } 
        
    

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurantPizza = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan', overlaps="pizzas,restaurants")
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')
    # add serialization rules
    serialize_only = ('id', 'ingredients', 'name')
    def to_dict(self):
        return {
            'id': self.id,
            'ingredients': self.ingredients,
            'name': self.name
        }

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    pizza = db.relationship('Pizza', back_populates='restaurantPizza', overlaps="pizzas,restaurants")
    # add relationships
    restaurant = db.relationship('Restaurant', back_populates='restaurantPizza', overlaps="pizzas,restaurants")
    # add relationships

    # add serialization rules
    # serialize_only = ('price', 'pizza_id', 'restaurant_id' )
    # def to_dict(self):
    #     return {
    #         'price': self.price,
    #         'pizza_id': self.pizza_id,
    #         'restaurant_id': self.restaurant_id,
    #     }
    
    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0 or price >= 31:
            raise ValueError ('Price mist be between 1 and 30 inclusive.')
        return price





    def __repr__(self):

        return f"<RestaurantPizza ${self.price}>"























# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(
#     naming_convention={
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     }
# )

# db = SQLAlchemy(metadata=metadata)


# class Restaurant(db.Model, SerializerMixin):
#     __tablename__ = "restaurants"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     address = db.Column(db.String)

#     # add relationship

#     # add serialization rules

#     def __repr__(self):
#         return f"<Restaurant {self.name}>"


# class Pizza(db.Model, SerializerMixin):
#     __tablename__ = "pizzas"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     ingredients = db.Column(db.String)

#     # add relationship

#     # add serialization rules

#     def __repr__(self):
#         return f"<Pizza {self.name}, {self.ingredients}>"


# class RestaurantPizza(db.Model, SerializerMixin):
#     __tablename__ = "restaurant_pizzas"

#     id = db.Column(db.Integer, primary_key=True)
#     price = db.Column(db.Integer, nullable=False)

#     # add relationships

#     # add serialization rules

#     # add validation

#     def __repr__(self):
#         return f"<RestaurantPizza ${self.price}>"
