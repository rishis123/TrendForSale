import json
from flask import Flask, request
# from db import db
from flask_sqlalchemy import SQLAlchemy
from random import choice
from flask_cors import CORS #allow frontend to communicate

# define db filename
db_filename = "todo.db"
app = Flask(__name__)
CORS(app)

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# initialize app
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# your routes here

@app.route("/metadata")
def hello_world():
    return success_response("Hello, World!")

# run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
  

