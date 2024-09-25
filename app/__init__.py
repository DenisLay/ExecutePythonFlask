from flask import Flask
from flask_jwt_extended import JWTManager

from .routes import main

def create_app():
    app = Flask('api')

    app.register_blueprint(main)

    app.config['JWT_SECRET_KEY'] = '1234567890'

    jwt = JWTManager(app)

    return app