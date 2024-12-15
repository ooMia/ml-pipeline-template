def test_dir_exist():
    import os
    from db.tests import MYSQL_DATA_DIR
    assert os.path.exists(MYSQL_DATA_DIR)


def test_initial_connection():
    import mysql.connector
    from db.tests import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT, MYSQL_HOST
    with mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
    ) as conn:
        assert conn.is_connected()
