from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from .script_builder import execute_code
import json
from .db import bot

main = Blueprint('main', 'api')
cors = CORS(main, resources={r"/*": {"origins": "http://localhost:3000"}}) #Add your url of project here

@main.route('/', methods=["GET"])
@cross_origin()
def index():
    return f'<h1>Index</h1>'

@main.route('/help', methods=["GET"])
@cross_origin()
def help():
    return f'<h1>Help</h1>'

@main.route('/exec', methods=["POST"])
@cross_origin()
def req():
    try:
        data = request.json
        src = data.get('src')

        try:
            res = execute_code(src)

            return res
            #return json.dumps(res, indent=1)
        except Exception as e:
            return json.dumps({ 'error-in': str(e) }, indent=1)

    except Exception as e:
        return json.dumps({ 'error-out': str(e) }, indent=1)

@main.route('/new_table', methods=["POST"])
@cross_origin()
def new_table():
    try:
        data = request.json
        src = json.loads(data.get('src'))

        try:
            script = bot.create_table(src)

            return script
        except Exception as e:
            return json.dumps({ 'error-in': str(e) }, indent=1)

    except Exception as e:
        return json.dumps({ 'error-out': str(e) }, indent=1)

@main.route('/fetch', methods=["POST"])
@cross_origin()
def new_table():
    try:
        data = request.json

        try:
            items = bot.fetch(data.get('src'))

            return items
        except Exception as e:
            return json.dumps({ 'error-in': str(e) }, indent=1)

    except Exception as e:
        return json.dumps({ 'error-out': str(e) }, indent=1)

@main.route('/db', methods=['GET'])
@cross_origin()
def db():
    try:

        return {
            'status': f'ok: {str(bot.cursor)}'
        }
    except Exception as e:
        return {
            'status': f'error: {str(e)}'
        }

@main.route('/check', methods=["GET"])
@cross_origin()
def check():
    return {
        'status' : 'ok'
    }