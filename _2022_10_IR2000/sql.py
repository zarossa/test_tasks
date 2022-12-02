import mysql.connector as mysql
from mysql.connector import Error
import re
from data import field_links
from data import columns as table_columns
from data import config
from data import direction


def db_connect():
    """Соединение с базой данных"""
    return mysql.connect(**config)


def get_contracts_numbers(table, region_name):
    """Функция получения списка контрактов
    :param table: Имя таблицы
    :param region_name: Имя региона
    :return: Список контрактов"""
    try:
        connection = db_connect()
        with connection.cursor() as cursor:
            query = f"SELECT id, regNum, publish_date, Название_архива FROM {table} WHERE Регион = '{region_name}'"
            cursor.execute(query)
            ids = cursor.fetchall()
        connection.close()
        result = {}
        for i in ids:
            result[i[0]] = {'id': i[0], 'regNum': i[1], 'publish_date': i[2], 'Название_архива': i[3]}
        return result
    except Exception as e:
        with open(direction + 'logs/error.txt', 'a') as log:
            log.write(f'The error was occurred at the function get_contracts_numbers:\n{table}\n{e}\n\n')


def insert_values(table, columns, values):
    """Функция добавления записей в таблицу
    :param table: Имя таблицы
    :param columns: Перечень имен столбцов в виде списка
    :param values: Данные для записи в виде списка кортежей"""
    try:
        connection = db_connect()
        val = re.sub(r'\$s', '%s', ', '.join(['IFNULL($s, DEFAULT(`%s`))'] * len(columns)) % tuple(columns))
        columns = ', '.join(columns)
        query = f"INSERT INTO {table} ({columns}) VALUES ({val})"
        with connection.cursor() as cursor:
            cursor.executemany(query, values)
            connection.commit()
        connection.close()
        return True
    except Error as e:
        with open(direction + 'logs/error.txt', 'a') as log:
            log.write(f'The error was occurred at the function insert_values:\n{table}\n{e}\n\n')
        with open(direction + 'logs/broken.txt', 'r') as log:
            log.write(f'{table}\n{e}\n{columns}\n{values}\n\n')


# def insert_big_values(table, columns, values, values2, values3, values4):
#     """Функция добавления записей в таблицу
#     :param table: Имя таблицы
#     :param columns: Перечень имен столбцов в виде списка
#     :param values: Данные для записи в виде списка кортежей
#     :param values2: Данные для записи в виде списка кортежей
#     :param values3: Данные для записи в виде списка кортежей
#     :param values4: Данные для записи в виде списка кортежей"""
#     try:
#         columns1 = columns[:50]
#         columns2 = columns[50:100]
#         columns3 = columns[100:150]
#         columns4 = columns[150:]
#         connection = db_connect()
#         val1 = re.sub(r'\$s', '%s', ', '.join(['IFNULL($s, DEFAULT(`%s`))'] * len(columns1)) % tuple(columns1))
#         columns1 = ', '.join(columns1)
#         query1 = f"INSERT INTO {table} ({columns1}) VALUES ({val1})"
#
#         columns2 = [f"`{column}` = IFNULL(%s, DEFAULT(`{column}`))" for column in columns2]
#         columns2 = ', '.join(columns2)
#         query2 = f"UPDATE {table} SET {columns2} WHERE `id` = %s"
#
#         columns3 = [f"`{column}` = IFNULL(%s, DEFAULT(`{column}`))" for column in columns3]
#         columns3 = ', '.join(columns3)
#         query3 = f"UPDATE {table} SET {columns3} WHERE `id` = %s"
#
#         columns4 = [f"`{column}` = IFNULL(%s, DEFAULT(`{column}`))" for column in columns4]
#         columns4 = ', '.join(columns4)
#         query4 = f"UPDATE {table} SET {columns4} WHERE `id` = %s"
#         with connection.cursor() as cursor:
#             cursor.executemany(query1, values)
#             connection.commit()
#             cursor.executemany(query2, values2)
#             connection.commit()
#             cursor.executemany(query3, values3)
#             connection.commit()
#             cursor.executemany(query4, values4)
#             connection.commit()
#         connection.close()
#         return True
#     except Error as e:
#         with open(direction + 'logs/error.txt', 'a') as log:
#             log.write(f'The error was occurred at the function insert_big_values:\n{table}\n{e}\n\n')


def parse_sql(data, region, region_name, table_name):
    """Функция парсера БД"""
    # global data.fieldsLinks
    # columns_to_add = []
    preval = {}
    values = []

    contract_numbers = get_contracts_numbers(table_name, region_name)
    # Формируем столбцы для добавления в БД
    # !!!Внимание!!! Проверка столбцов чувствительна к регистру. EndDate не равно endDate.
    for notif in data:
        value = {}
        for column in data[notif]:
            if column in field_links:
                col = field_links[column]
                value[col] = data[notif][column]
        preval[notif] = value

    # Формируем данные для записи/обновления в БД
    for notif in preval:
        if int(notif) not in contract_numbers:
            value = []
            for it in table_columns:
                if it in preval[notif]:
                    value.append(preval[notif][it])
                elif it == 'region':
                    value.append(region)
                else:
                    value.append(None)
            values.append(tuple(value))

    # Добавление новых записей в БД
    if len(values) > 0:
        insert_values(table_name, table_columns, values)
