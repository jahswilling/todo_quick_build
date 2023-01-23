from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from .models import User, db
from flasgger import swag_from

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/signup", methods=["POST"])
@swag_from.docs.operation(
    summary="Sign up for the application",
    description="Provides a JSON web token after successful sign up",
    parameters=[
        {
            "name": "username",
            "description": "The desired username",
            "required": True,
            "in": "formData",
            "type": "string"
        },
        {
            "name": "password",
            "description": "The desired password",
            "required": True,
            "in": "formData",
            "type": "string"
        }
    ],
    responses={
        "201": {
            "description": "A JSON web token",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string"
                    },
                    "refresh_token": {
                        "type": "string"
                    }
                }
            }
        },
        "400": {
            "description": "Missing JSON in request or username already exists"
        }
    }
)
def signup():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    ), 201



@auth_blueprint.route("/login", methods=["POST"])
@swag_from.docs.operation(
    summary="Login to the application",
    description="Provides a JSON web token after successful login",
    parameters=[
        {
            "name": "username",
            "description": "The username of the user",
            "required": True,
            "in": "formData",
            "type": "string"
        },
        {
            "name": "password",
            "description": "The password of the user",
            "required": True,
            "in": "formData",
            "type": "string"
        }
    ],
    responses={
        "200": {
            "description": "A JSON web token",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string"
                    },
                    "refresh_token": {
                        "type": "string"
                    }
                }
            }
        },
        "401": {
            "description": "Invalid username or password"
        }
    }
)
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    ), 200

