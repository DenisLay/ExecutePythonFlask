from flask import Blueprint, request
from flask_cors import CORS, cross_origin
import requests

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

        exec(src)
        return f'<i>{src}</i>'
    except Exception as e:
        return str(e)

@main.route("/check", methods=["GET"])
@cross_origin()
def check():
    return {
        "status":"ok"
    }