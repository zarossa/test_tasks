import mysql.connector as mysql
from mysql.connector import Error
from data import columns
from data import config


def db_connect():
    """Connection to database"""
    return mysql.connect(**config)


def create_db():
    """Function of creating a database"""
    try:
        connection = mysql.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            # port=config['port']
        )
        with connection.cursor() as cursor:
            query = f'''SET GLOBAL innodb_file_format=Barracuda;
                    SET GLOBAL innodb_file_per_table=1;
                    SET GLOBAL innodb_large_prefix=1;
                    CREATE DATABASE {config["database"]} COLLATE utf8_general_ci'''
            cursor.execute(query)
        connection.close()
        return True
    except Error as er:
        print(f'The error was occurred at the function create_db:\n{er}')


def execute_query(query):
    try:
        cursor.execute(query)
        connection.commit()
    except Error as er:
        print(f"The error was occurred with query\n{er}")


try:
    tables = ['northwestern_fd',
              'central_fd',
              'volga_fd',
              'southern_fd',
              'north_caucasian_fd',
              'ural_fd',
              'siberian_fd',
              'far_eastern_fd',
              'moscow_and_moscow_region',
              'crimean_fd']
    columns = ', '.join([f'ADD {i} MEDIUMTEXT' for i in columns if i not in (
        'id', 'regNum', 'publish_date', 'Печатная_форма_кнтркта', 'Номер_кнтркта')])
    create_db()
    connection = db_connect()
    with connection.cursor() as cursor:
        for table in tables:
            create_table = f'''CREATE TABLE {table} (
                    true_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    id INT,
                    regNum BIGINT,
                    publish_date TEXT,
                    Печатная_форма_кнтркта TEXT,
                    Номер_кнтркта TEXT
                ) ROW_FORMAT=DYNAMIC;'''
            execute_query(create_table)
            create_columns = f'ALTER TABLE {table} {columns}'
            execute_query(create_columns)
    connection.close()
except Error as e:
    print(f'The error was occurred:\n{e}')
