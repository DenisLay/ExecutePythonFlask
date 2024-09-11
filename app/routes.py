from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .db import add_record, get_records, clear_records
from .script_builder import execute_code
import json

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

@main.route('/push_doc', methods=["GET"])
@cross_origin()
def push_doc():
    add_record('doc X')
    return '<p>added "doc X"</p>'

@main.route('/last_doc', methods=["GET"])
@cross_origin()
def last_doc():
    return get_records()

@main.route('/clear', methods=["GET"])
@cross_origin()
def clear():
    clear_records()
    return {
        "status":"ok"
    }

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

@main.route('/check', methods=["GET"])
@cross_origin()
def check():
    return {
        'status' : 'ok'
    }