"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
#* Boilerplate libraries
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Character,Planet,FavoritePlanet,FavoriteCharacter
from werkzeug.security import safe_str_cmp

#* JWT libraries
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#* Custom made libraries
from initialLoad import initial_loader
from payload_handlers import get_merged_lists,update_favorites_lists

#*Generic Libraries
from datetime import timedelta
import requests

#*MAIN SETUP
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
jwt = JWTManager(app)
db.init_app(app)
CORS(app)
setup_admin(app)
#*end MAIN SETUP

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    
@app.route('/create-account', methods=['POST'])
def create_account():
    body=request.get_json()

    if body is None:
        return "The request body is null", 400
    if 'username' not in body:
        return "Empty username", 400
    if 'email' not in body:
        return "Empty email", 400
    if 'password' not in body:
        return "Empty password", 400

    user=User()
    user.username=body['username']
    user.email=body['email']
    user.password=body['password']
    user.is_active=True
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "Added user"
    }

    return jsonify(response_body), 200

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).one_or_none()
    
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401
    
    expiration=timedelta(hours=80)
    access_token = create_access_token(identity=user, expires_delta=expiration)

    return jsonify(access_token=access_token)

@app.route("/load_data", methods=["GET"])
def load_data():
    #todo filtro que revisa
    initial_loader()
    return jsonify("Succesfully added the Data"), 200

@app.route("/get-favorites" , methods=["GET"])
@jwt_required()
def get_favorites():
    merged_lists=get_merged_lists(current_user.id)
    return jsonify(merged_lists), 200

@app.route("/update-favorites" , methods=["POST"])
@jwt_required()
def update_favorites_sm():
    user_payload=request.get_json()
    updated_lists=update_favorites_lists(user_payload,current_user.id)
    return jsonify("Succesfully updated databases", updated_lists), 200
    

#Just use for debugging purposes
@app.route("/user_identity", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        full_name=current_user.email,
        username=current_user.username,
    )

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
