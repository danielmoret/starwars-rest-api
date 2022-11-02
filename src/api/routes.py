"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Vehicle, Favorite
from api.utils import generate_sitemap, APIException
import requests

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/users', methods=['GET','POST'])
def get_users():
    if request.method == 'GET':
        users = User.query.all()
        users_dictionaries = []

        for user in users:
            users_dictionaries.append(user.serialize())

        return jsonify(users_dictionaries), 200
    
    new_user_data = request.json
    try:
        new_user = User.create(**new_user_data)
        return jsonify(new_user.serialize()),201
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/people', methods=['GET','POST'])
def get_characters():
    if request.method == 'GET':
        characters = Character.query.all()
        characters_dictionaries = []

        for character in characters:
            characters_dictionaries.append(character.serialize())

        return jsonify(characters_dictionaries)

    new_character_data = request.json
    try:
        new_character = Character.create(**new_character_data)
        return jsonify(new_character.serialize()),201
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/people/<int:people_id>')
def get_character(people_id):
    character = Character.query.filter_by(id = people_id)
    
    try:
        return jsonify(character[0].serialize())
    except Exception as error:
        return jsonify({"message": "the character does not exist"})


@api.route('/planets', methods=['GET','POST'])
def get_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        planets_dictionaries = []

        for planet in planets:
            planets_dictionaries.append(planet.serialize())
        
        return jsonify(planets_dictionaries)
    
    new_planet_data = request.json
    try:
        new_planet = Planet.create(**new_planet_data)
        return jsonify(new_planet.serialize()),201
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/planets/<int:planet_id>')
def get_planet(planet_id):
    planet = Planet.query.filter_by(id = planet_id)
    try:
        return jsonify(planet[0].serialize())
    except Exception as error:
        return jsonify({"message": "the planet does not exist"})

@api.route('/vehicles', methods=['GET','POST'])
def get_vehicles():
    if request.method == 'GET':
        vehicles = Vehicle.query.all()
        vehicles_dictionaries = []

        for vehicle in vehicles:
            vehicles_dictionaries.append(vehicle.serialize())
        
        return jsonify(vehicles_dictionaries)
    
    new_vehicle_data = request.json
    try:
        new_vehicle = Vehicle.create(**new_vehicle_data)
        return jsonify(new_vehicle.serialize()),201
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/vehicles/<int:vehicle_id>')
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id = vehicle_id)
    try:
        return jsonify(vehicle[0].serialize())
    except Exception as error:
        return jsonify({"message": "the vehicle does not exist"})

@api.route('/users/<int:user_id>/favorites')
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id = user_id)

    return jsonify(
            [fav.serialize() for fav in favorites]
        ),200

@api.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['POST'])
def add_character_to_favorite(people_id,user_id):
    new_favorite_data = request.json

    favorites = Favorite.query.filter_by(user_id = user_id, character_id = people_id).first()
    if favorites is not None:
        return jsonify({"msg": "The character is already in favorites"}), 401
    else:
        try:
            new_favorite = Favorite.create_fav(user_id = user_id, character_id = people_id, **new_favorite_data)
            return jsonify(new_favorite.serialize()),201
        except Exception as error:
            return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_planet_to_favorite(planet_id,user_id):
    new_favorite_data = request.json

    favorites = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if favorites is not None:
        return jsonify({"msg": "The planet is already in favorites"}), 401
    else:
        try:
            new_favorite = Favorite.create_fav(user_id = user_id, planet_id = planet_id, **new_favorite_data)
            return jsonify(new_favorite.serialize()),201
        except Exception as error:
            return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/favorite/vehicle/<int:user_id>/<int:vehicle_id>', methods=['POST'])
def add_vehicle_to_favorite(vehicle_id,user_id):
        new_favorite_data = request.json

        favorites = Favorite.query.filter_by(user_id = user_id, vehicle_id = vehicle_id).first()
        if favorites is not None:
            return jsonify({"msg": "The vehicle is already in favorites"}), 401
        else:
            try:
                new_favorite = Favorite.create_fav(user_id = user_id, vehicle_id = vehicle_id, **new_favorite_data)
                return jsonify(new_favorite.serialize()),201
            except Exception as error:
                return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500

@api.route('/favorite/people/<int:user_id>/<int:people_id>', methods=['DELETE'])
def delete_character_to_favorite(people_id,user_id):
    favorite_to_delete = Favorite.query.filter_by(user_id = user_id, character_id = people_id).first()
    try:
        fav_delete = Favorite.delete_fav(favorite_to_delete)
        return jsonify(fav_delete),200
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500 

@api.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_planet_to_favorite(planet_id,user_id):
    favorite_to_delete = Favorite.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    try:
        fav_delete = Favorite.delete_fav(favorite_to_delete)
        return jsonify(fav_delete),200
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500 

@api.route('/favorite/vehicle/<int:user_id>/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_to_favorite(vehicle_id,user_id):
    favorite_to_delete = Favorite.query.filter_by(user_id = user_id, vehicle_id = vehicle_id)[0]
    try:
        fav_delete = Favorite.delete_fav(favorite_to_delete)
        return jsonify(fav_delete),200
    except Exception as error:
        return jsonify(error.args[0]),error.args[1] if len(error.args) > 1 else 500 

@api.route('/fill/planets')
def fill_planets():
    response = requests.get('https://swapi.dev/api/planets')
    data = response.json()
    planets = Planet.query.all()

    if len(planets) == data['count']:
        return jsonify("Los planetas ya existen"),400

    null = False
    count = 0
    for number in range(len(data['results'])):
        Planet.create(name = data['results'][number]['name'], population = data['results'][number]['population'], terrain = data['results'][number]['terrain'])
        count = count + 1
        print("creando...")
        
    while not null:
        response = requests.get(data['next'])
        data = response.json()

        for number in range(len(data['results'])):
            Planet.create(name = data['results'][number]['name'], population = data['results'][number]['population'], terrain = data['results'][number]['terrain'])
            count = count + 1
            print("creando...")
        null = data['next'] is None
    
    return jsonify(f"Cree {count} planets")

@api.route('/fill/people')
def fill_characters():
    response = requests.get('https://swapi.dev/api/people')
    data = response.json()
    characters = Character.query.all()

    if len(characters) == data['count']:
        return jsonify("Los personajes ya existen"),400

    null = False
    count = 0
    for number in range(len(data['results'])):
        Character.create(name = data['results'][number]['name'], gender = data['results'][number]['gender'], hair_color = data['results'][number]['hair_color'],eye_color = data['results'][number]['eye_color'])
        count = count + 1
        print("creando...")
        
    while not null:
        response = requests.get(data['next'])
        data = response.json()

        for number in range(len(data['results'])):
            Character.create(name = data['results'][number]['name'], gender = data['results'][number]['gender'], hair_color = data['results'][number]['hair_color'],eye_color = data['results'][number]['eye_color'])
            count = count + 1
            print("creando...")
        null = data['next'] is None
    
    return jsonify(f"Cree {count} personajes")

@api.route('/fill/vehicles')
def fill_vehicles():
    response = requests.get('https://swapi.dev/api/vehicles')
    data = response.json()
    vehicles = Vehicle.query.all()

    if len(vehicles) == data['count']:
        return jsonify("Los vehiculos ya existen"),400

    null = False
    count = 0
    for number in range(len(data['results'])):
        Vehicle.create(name = data['results'][number]['name'], model = data['results'][number]['model'], passengers = data['results'][number]['passengers'],cost = data['results'][number]['cost_in_credits'])
        count = count + 1
        print("creando...")
        
    while not null:
        response = requests.get(data['next'])
        data = response.json()

        for number in range(len(data['results'])):
            Vehicle.create(name = data['results'][number]['name'], model = data['results'][number]['model'], passengers = data['results'][number]['passengers'],cost = data['results'][number]['cost_in_credits'])
            count = count + 1
            print("creando...")
        null = data['next'] is None
    
    return jsonify(f"Cree {count} vehiculos")