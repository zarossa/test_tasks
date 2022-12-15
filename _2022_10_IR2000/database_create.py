import mysql.connector as mysql
from mysql.connector import Error
from data import columns
from data import config
from data import ext_columns


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
        'ID', 'Номер_реестровой_записи', 'Дата_публикации', 'Печатная_форма_контракта', 'Номер_контракта')])
    create_db()
    connection = db_connect()
    with connection.cursor() as cursor:
        for table in tables:
            create_table = f'''CREATE TABLE {table} (
                    true_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    ID INT,
                    Номер_реестровой_записи BIGINT,
                    Дата_публикации TEXT,
                    Печатная_форма_контракта TEXT,
                    Номер_контракта TEXT
                ) ROW_FORMAT=DYNAMIC;'''
            execute_query(create_table)
            create_columns = f'ALTER TABLE {table} {columns}'
            execute_query(create_columns)
        for table in ext_columns:
            create_table = f'''CREATE TABLE {table} (
                    true_id INTEGER PRIMARY KEY AUTO_INCREMENT
                ) ROW_FORMAT=DYNAMIC;'''
            columns = ', '.join([f'ADD {i} MEDIUMTEXT' for i in ext_columns[table]])
            execute_query(create_table)
            create_columns = f'ALTER TABLE {table} {columns}'
            execute_query(create_columns)
    connection.close()
except Error as e:
    print(f'The error was occurred:\n{e}')
