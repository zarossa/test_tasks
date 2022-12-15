import mysql.connector as mysql
from mysql.connector import Error
import re
from data import columns as table_columns
from data import ext_columns
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
            query = f"SELECT ID, Номер_реестровой_записи, Дата_публикации, Архив FROM {table} WHERE Регион = '{region_name}'"
            cursor.execute(query)
            ids = cursor.fetchall()
        connection.close()
        result = {}
        for i in ids:
            result[i[0]] = {'id': i[0], 'regNum': i[1], 'publish_date': i[2], 'Архив': i[3]}
        return result
    except Exception as e:
        with open(direction + 'logs/error.txt', 'a') as log:
            log.write(f'The error was occurred at the function get_contracts_numbers:\n{table}\n{e}\n\n')


def get_others_numbers(table):
    """Функция получения списка данных
    :param table: Имя таблицы
    :return: Список данных"""
    try:
        connection = db_connect()
        with connection.cursor() as cursor:
            query = f"SELECT Внешняя_ссылка FROM {table}"
            cursor.execute(query)
            result = cursor.fetchall()
        connection.close()
        result = [i[0] for i in result]
        return result
    except Exception as e:
        with open(direction + 'logs/error.txt', 'a') as log:
            log.write(f'The error was occurred at the function get_others_numbers:\n{table}\n{e}\n\n')


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


def parse_sql(data, region, region_name, table_name, type_data, hard_mode=False):
    """Функция парсера БД"""
    if hard_mode:
        if not data:
            return
        pass
    else:
        if len(data) < 2000:
            return
    preval = {}
    values = []
    for notif in data:
        value = {}
        if type_data != 'main':
            value['Внешняя_ссылка'] = notif
        for column in data[notif]:
            value[column] = data[notif][column]
        preval[notif] = value

    if type_data == 'main':
        contract_numbers = get_contracts_numbers(table_name, region_name)
        table_column = table_columns
        for notif in preval:
            if int(notif) not in contract_numbers:
                value = []
                for it in table_column:
                    if it in preval[notif]:
                        value.append(preval[notif][it])
                    elif it == 'region':
                        value.append(region)
                    else:
                        value.append(None)
                values.append(tuple(value))
        pass
    else:
        table_name = '_' + type_data
        contract_numbers = get_others_numbers(table_name)
        table_column = ext_columns['_' + type_data]
        for notif in preval:
            if notif not in contract_numbers:
                value = []
                for it in table_column:
                    if it in preval[notif]:
                        value.append(preval[notif][it])
                    else:
                        value.append(None)
                values.append(tuple(value))
        pass

    if len(values) > 0:
        insert_values(table_name, table_column, values)
    return type_data
