import psycopg2
from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token


class DBBot:
    def __init__(self, dbname, user, password, host):
        self.connection = psycopg2.connect(
            dbname = dbname,
            user = user,
            password = password,
            host = host
        )

        self.cursor = self.connection.cursor()

    def execScript(self, script):
        self.cursor.execute(script)
        self.connection.commit()

    def fetch(self, script):
        self.cursor.execute(script)
        items = self.cursor.fetchall()

        return items

    def create_table(self, src):
        try:
            table_name = src.get('table')
            columns = src.get('columns')

            columns_script = ''

            for index, column in enumerate(columns):
                if index < len(columns) - 1:
                    sym = ','
                else:
                    sym = ''
                column_script = f'{column["name"]} {column["attrs"]}{sym}'
                columns_script += column_script

            script = f'CREATE TABLE {table_name} ({columns_script});'

            self.cursor.execute(script)
            self.connection.commit()

            return 'ok'
        except Exception as e:
            self.connection.rollback()
            return f'error: {str(e)}'

    def create_user(self, username, email, password):
        try:
            self.cursor.execute(f'SELECT * FROM users WHERE email = \'{email}\'')
            user_exists = self.cursor.fetchone()

            if user_exists:
                return jsonify({"message": "User already exists"}), 400
        except Exception as e:
            return jsonify({"message-1": str(e)}), 400

        try:
            self.cursor.execute(f'INSERT INTO users (username, email, password) values(\'{username}\', \'{email}\', \'{password}\')')
            self.connection.commit()
        except Exception as e:
            return jsonify({"message-2": str(e)}), 400

        return jsonify({"message": "User registered succesfully"}), 201

    def login_user(self, email, password):
        self.cursor.execute(f'SELECT * FROM users WHERE email = \'{email}\'')
        user = self.cursor.fetchone()

        if user and Bcrypt.check_password_hash(user[3], password):
            access_token = create_access_token(identity={'username': user[1], 'email': user[2]})
            return jsonify(access_token=access_token), 200

        return jsonify({"message": "Invalid credentials"}), 401

# {

#     "table": "users",
#     "columns": [
#         {
#             "id": "0",
#             "na   me": "id",
#             "attrs": "SERIAL PRIMARY KEY"
#         },
#         {
#             "id": "1",
#             "name": "username",
#             "attrs": "VARCHAR(50) UNIQUE NOT NULL"
#         },
#         {
#             "id": "2",
#             "name": "email",
#             "attrs": "VARCHAR(100) UNIQUE NOT NULL"
#         },
#         {
#             "id": "3",
#             "name": "created_at",
#             "attrs": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
#         }
#     ]
# }

bot = DBBot('maindb_d1pv', 'user', '67Xh91AN1squhUUMse0ckLo965OFiLKo', 'dpg-crjvuel2ng1s73fm1p10-a.oregon-postgres.render.com')