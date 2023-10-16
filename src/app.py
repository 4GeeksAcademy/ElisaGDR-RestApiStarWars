"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


@app.route('/user/favorite-characters', methods=['GET'])
def show_fav_characters():
    favorite_characters = {
        "msg": "Hello, this is your GET /favorite_characters response "
    }
    return jsonify(favorite_characters), 200


@app.route('/user/favorite-planets', methods=['GET'])
def show_fav_planets():
    favorite_planets = {
        "msg": "Hello, this is your GET /favorite_planets response "
    }
    return jsonify(favorite_planets), 200


@app.route('/characters', methods=['GET'])
def show_characters():
    characters = {
        "msg": "Hello, this is your GET /characters response "
    }
    return jsonify(characters), 200


@app.route('/planets', methods=['GET'])
def show_planets():
    planets = {
        "msg": "Hello, this is your GET /planets response "
    }
    return jsonify(planets), 200


@app.route('/characters/ind:character_id', methods=['GET'])
def show_favorite_characters():
    characters = {
        "msg": "Hello, this is your GET /character_id response "
    }
    return jsonify(characters), 200


@app.route('/planets/ind:planets_id', methods=['GET'])
def show_favorite_planets():
    planets = {
        "msg": "Hello, this is your GET /planet_id response "
    }
    return jsonify(planets), 200


@app.route('/favorite-character/<int:character_id>', methods=['POST'])
def add_fav_character():
    request_body = request.get_json(force=True)
    favorite_characters.append(request_body)
    response_body = jsonify(favorite_characters)
    print("Incoming request with the following body", request_body)
    return response_body


@app.route('/favorite-planets/<int:planets_id>', methods=['POST'])
def add_fav_planet():
    request_body = request.get_json(force=True)
    favorite_planets.append(request_body)
    response_body = jsonify(favorite_planets)
    print("Incoming request with the following body", request_body)
    return response_body


@app.route('/favorite-character/<int:character_id>', methods=['DELETE'])
def delete_fav_character(position):
    if len(favorite_characters) < position : 
        response_body = {"message": "Not found"}
        return response_body, 416
    del favorite_characters[position - 1]
    response_body = {"message": "Deleted character", 
                         "result": favorite_characters}
    print("This is the position to delete: ",position)
    return jsonify(favorite_characters), 200


@app.route('/favorite-planets/<int:planets_id>', methods=['DELETE'])
def delete_fav_planet(position):
    if len(favorite_planets) < position : 
        response_body = {"message": "Not found"}
        return response_body, 416
    del favorite_planets[position - 1]
    response_body = {"message": "Deleted planet", 
                         "result": favorite_planets}
    print("This is the position to delete: ",position)
    return jsonify(favorite_planets), 200

characters = []
planets = []
favorite_planets = []
favorite_characters = []


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
