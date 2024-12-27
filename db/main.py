class Database:
    def __init__(self):
        import mysql.connector
        from db import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT, MYSQL_HOST
        self.conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

    def store(self):
        # TODO: Implement
        pass

    def load(self):
        # TODO: Implement
        pass

    def __del__(self):
        self.conn.close()
