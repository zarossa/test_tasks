from data import config
from data import columns
import mysql.connector
# from mysql.connector import cursor
from mysql.connector import Error


def db_connect():
    """Соединение с базой данных"""
    return mysql.connector.connect(**config)


def execute_read_query(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as er:
        print(f"The error '{er}' occurred")

table_name = 'crimean_fd'
criteria = [1990103427322000002]
new_data = set()
try:
    connection = db_connect()

    with connection.cursor() as cursor:
        select_users = f"SELECT * FROM `{table_name}` WHERE id = 189720329"
        info = execute_read_query(select_users)
    data = []
    mini = {}
    for i in info:
        for idx, line in enumerate(i):
            if line is None:
                continue
            if type(line) is not int:
                if ';:;' in line:
                    line = line.split(';:;')
            mini[columns[idx]] = line
        data.append(mini)
        # print(mini['id'])
        # new_data.add(mini['id'])
        # mini = {}
    # print(data)
    # for line in data:
    #     print(line['id'])
    # print(len(data))
    # print(len(new_data))
    # for line in new_data:
    #     print(line)
    with open('logs/data.txt', 'w') as log:
        for line in data:
            for i in line:
                log.write(f'{i}: {line[i]}\n')

    for line in data:

        for i in line:
            print(f'{i}: {line[i]}')
        print('\n\n')
except Error as e:
    print(f'The error {e} was occurred')
