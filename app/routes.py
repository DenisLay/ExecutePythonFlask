from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required

from .script_builder import execute_code
import json
from .db import bot

main = Blueprint('main', 'api')
cors = CORS(main, resources={r"/*": {"origins": "http://localhost:3000"}})

@main.route('/', methods=["GET"])
@cross_origin()
def index():
    return f'<h1>Index</h1>'

@main.route('/help', methods=["GET"])
@cross_origin()
def help():
    return f'<h1>Help</h1>'

@main.route('/register', methods=["POST"])
@cross_origin()
def register():
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Missing data"}), 400

        if data['password'] == '':
            return jsonify({"error": "Missing data"}), 400

        return bot.create_user(data['username'], data['email'], data['password'])
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/login', methods=["POST"])
@cross_origin()
def login():
    try:
        data = request.get_json()
        return bot.login_user(data["email"], data["password"])
    except Exception as e:
        return jsonify({"error": str(e)})

@main.route('/exec', methods=["POST"])
@jwt_required()
@cross_origin()
def req():
    try:
        data = request.json
        src = data.get('src')

        try:
            res = execute_code(src)

            return res
        except Exception as e:
            return json.dumps({ 'error-in': str(e) }, indent=1)

    except Exception as e:
        return json.dumps({ 'error-out': str(e) }, indent=1)

@main.route('/new_table', methods=["POST"])
@jwt_required()
@cross_origin()
def new_table():
    try:
        data = request.json
        src = json.loads(data.get('src'))

        try:
            status = bot.create_table(src)

            return status
        except Exception as e:
            return json.dumps({ 'error-in': str(e) }, indent=1)

    except Exception as e:
        return json.dumps({ 'error-out': str(e) }, indent=1)

@main.route('/fetch', methods=["POST"])
@cross_origin()
def fetch():
    try:
        data = request.json

        try:
            items = bot.fetch(data.get('src'))

            return items
        except Exception as e:
            return json.dumps({ 'error-in': str(e) }, indent=1)

    except Exception as e:
        return json.dumps({ 'error-out': str(e) }, indent=1)

@main.route('/check', methods=["GET"])
@cross_origin()
def check():
    return {
        'status' : 'ok'
    }