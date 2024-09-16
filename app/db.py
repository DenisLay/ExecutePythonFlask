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

    def create_table(self, table_name, ):
        pass

bot = DBBot('maindb_d1pv', 'user', '67Xh91AN1squhUUMse0ckLo965OFiLKo', 'dpg-crjvuel2ng1s73fm1p10-a.oregon-postgres.render.com')