from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    favorites_planets= db.relationship('FavoritePlanet', backref='user', lazy=True)
    favorites_characters= db.relationship('FavoriteCharacter', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def check_password(self, password):
        return safe_str_cmp(password, self.password)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_day = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    favorite_id = db.relationship('FavoriteCharacter', backref='character', lazy=True)
    
    def __repr__(self):
        return '<Character %s>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_day": self.birth_day,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    favorite_id = db.relationship('FavoritePlanet', backref='planet', lazy=True)
    
    def __repr__(self):
        return '<Character %s>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            # do not serialize the password, its a security breach
        }

class FavoritePlanet (db.Model): # favorite_planet
    id = db.Column(db.Integer, primary_key=True)
    planet_id= db.Column(db.Integer,db.ForeignKey('planet.id'),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class FavoriteCharacter (db.Model): ## favorite_character
    id = db.Column(db.Integer, primary_key=True)
    character_id= db.Column(db.Integer,db.ForeignKey('character.id'),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    