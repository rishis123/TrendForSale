from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    #in_cart = 
    #bought = 

    def serialize(self):
        data = {
            "full_name" : self.full_name,
            "username" : self.username,
        }
        return data

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    product_name = db.Column(db.String(20), unique=True, nullable=False)
    image_link = db.Column(db.String(50), unique=True, nullable=False)

    def serialize(self):
        data = {
            "product_name" : self.product_name,
        }
        return data
