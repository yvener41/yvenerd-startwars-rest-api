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
from models import db, Person, Planet, Users, FavoritePeople, FavoritePlanets


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

# add this function call for the commands
setup_commands(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# routes for people of starwars

@app.route('/people', methods=['GET'])
def get_people():
    response_body = Person.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def get_one_person(person_id):

    single_person = Person.query.get(person_id)
    if single_person is None:
        raise APIException(f'Person ID {person_id} not found.', status_code=404)
        
    return jsonify(single_person.serialize()), 200


# routes for planets of star wars

@app.route('/planets', methods=['GET'])
def get_planets():
    response_body = Planet.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):    
    single_planet = Planet.query.get(planet_id)
    if single_planet is None:
        raise APIException(f'Planet ID {planet_id} not found.', status_code=404)
        
    return jsonify(single_planet.serialize()), 200


# users and favorites

@app.route('/users', methods=['GET'])
def get_all_users():
    pass


@app.route('/users/<int:user_id>', methods=['GET'])
def get_one_user():
    pass


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_one_user_favorites():
    pass


@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def add_one_person_to_favorites():
    pass


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_one_planet_to_favorites():
    pass


@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_one_person_from_favorites():
    pass


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_one_planet_from_favorites():
    pass












# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)