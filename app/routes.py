from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .db import add_record, get_records, clear_records
from .script_builder import execute_code
import json
import psycopg2

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
        'status' : 'ok'
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

@main.route('/db', methods=['GET'])
@cross_origin()
def db():
    try:
        connection = psycopg2.connect(database="example-db",
                                        host="postgresql://user:67Xh91AN1squhUUMse0ckLo965OFiLKo@dpg-crjvuel2ng1s73fm1p10-a.oregon-postgres.render.com/maindb_d1pv",
                                        user="user",
                                        password="PGPASSWORD=67Xh91AN1squhUUMse0ckLo965OFiLKo psql -h dpg-crjvuel2ng1s73fm1p10-a.oregon-postgres.render.com -U user maindb_d1pv")
        cursor = connection.cursor()

        return {
            'status': str(cursor)
        }
    except Exception as e:
        return {
            'status': str(e)
        }

@main.route('/check', methods=["GET"])
@cross_origin()
def check():
    return {
        'status' : 'ok'
    }