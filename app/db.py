import psycopg2

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