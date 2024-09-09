from flask import Flask 
#from .routes import main
import db

def create_app():
    app = Flask('api')

    #app.register_blueprint(main)

    return app

db.add_record('item 1')
db.add_record('item 2')
db.add_record('item 3')

print(db.get_records())