from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.email = kwargs['email']
        self.password = kwargs['password']
    
    @classmethod
    def create(cls, **kwargs):
        new_user = cls(**kwargs)
        db.session.add(new_user) # INSERT INTO

        try:
            db.session.commit() # Se ejecuta el INSERT INTO
            return new_user
        except Exception as error:
            raise Exception(error.args[0],400)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.gender = kwargs['gender']
        self.hair_color = kwargs['hair_color']
        self.eye_color = kwargs['eye_color']
    
    @classmethod
    def create(cls, **kwargs):
        new_character = cls(**kwargs)
        db.session.add(new_character) # INSERT INTO

        try:
            db.session.commit() # Se ejecuta el INSERT INTO
            return new_character
        except Exception as error:
            raise Exception(error.args[0],400)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    population = db.Column(db.String(120))
    terrain = db.Column(db.String(120))

    def __init__(self, **kwargs):
        self.name = kwargs['name'],
        self.population = kwargs['population']
        self.terrain = kwargs['terrain']

    @classmethod
    def create(cls, **kwargs):
        new_planet = cls(**kwargs)
        db.session.add(new_planet) # INSERT INTO

        try:
            db.session.commit() # Se ejecuta el INSERT INTO
            return new_planet
        except Exception as error:
            raise Exception(error.args[0],400)

    def serialize(self):
        return {
            "id" : self.id, 
            "name" : self.name,
            "population" : self.population,
            "terrain" : self.terrain
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120))
    passengers = db.Column(db.String(120))
    cost = db.Column(db.String(120))

    def __init__(self, **kwargs):
        self.name = kwargs['name'],
        self.model = kwargs['model']
        self.passengers = kwargs['passengers']
        self.cost = kwargs['cost']
    
    @classmethod
    def create(cls, **kwargs):
        new_vehicle = cls(**kwargs)
        db.session.add(new_vehicle ) # INSERT INTO

        try:
            db.session.commit() # Se ejecuta el INSERT INTO
            return new_vehicle 
        except Exception as error:
            raise Exception(error.args[0],400)

    def serialize(self):
        return {
            "id" : self.id, 
            "name" : self.name,
            "model" : self.model,
            "passengers" : self.passengers, 
            "cost" : self.cost
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"))

    def __init__(self, **kwargs):
        self.name = kwargs['name'],
        self.user_id = kwargs['user_id']
        self.character_id = kwargs['character_id'] if 'character_id' in kwargs else None
        self.planet_id = kwargs['planet_id'] if 'planet_id' in kwargs else None
        self.vehicle_id = kwargs['vehicle_id'] if 'vehicle_id' in kwargs else None

    @classmethod
    def create_fav(cls,**kwargs):
        new_favorite = cls(**kwargs)
        db.session.add(new_favorite)
        try:
            db.session.commit()
            return new_favorite 
        except Exception as error:
            raise Exception(error.args[0],400)
    
    @classmethod
    def delete_fav(cls, kwargs):
        db.session.delete(kwargs)
        try:
            db.session.commit()
            return {"message": "successfully deleted"}
        except Exception as error:
            raise Exception(error.args[0],400)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }