import json
import os
from flask import Flask, request, session, redirect, jsonify
# from db import db
from flask_sqlalchemy import SQLAlchemy
from random import choice
from flask_cors import CORS #allow frontend to communicate
from flask_session import Session #Store session data 
from db import db, User, Order
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

# define db filename
api = Flask(__name__)
origins = os.environ.get("ORIGINS")

CORS(api)

# CORS(api, resources={r"/*": {"origins": origins, "supports_credentials": True}})  # Allow requests from frontned server

# setup config
api.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI", 'sqlite:///site.db') #default if not otherwise provided
api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api.config["SQLALCHEMY_ECHO"] = True

api.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY") #securely store information, prevent hacker from passing in token and accessing content they shouldn't.

jwt = JWTManager(api)

db.init_app(api)

"""
Creating all necessary tables before request
"""
@api.before_first_request
def create_tables():
     db.create_all()


"""
Login Request. If valid user-name and password combination, then logs in user by creating an access token.
"""
@api.route('/login', methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user_value = User.query.filter_by(username=username).first()
    if not user_value:
        return failure_response("No such user"), 401
    if user_value.password != password:
        return failure_response("Wrong password"), 401
    print('made it here')

    access_token = create_access_token(identity={"username": username})
    response = {"access_token":access_token}
    return success_response(response)

"""
Accesses profile of logged-in user (requirement -- hence jwt_required tag). Returns username, email, and fullname.
"""
@api.route('/profile', methods=["GET"])
@jwt_required() #If not logged-in accessing this will give 401 error
def access_profile():
    current_user = get_jwt_identity() #returns JSON web token or None
    if not current_user:
        return failure_response("No JSON Web token here"), 401
    username = current_user.get("username")
    if not username:
        return failure_response("Bad JSON web token"), 401
    user_value = User.query.filter_by(username=username).first()
    if not user_value:
        return failure_response("No such user")
    return success_response(user_value.serialize())

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# your routes here

"""
Test route for postman
"""
@api.route("/metadata")
def hello_world():
    return success_response("Hello, World!")

# run the app
if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8000, debug=True)