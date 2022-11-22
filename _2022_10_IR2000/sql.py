import mysql.connector as mysql
from mysql.connector import Error
import re
from data import field_links
from data import columns as table_columns
from data import config


def db_connect():
    """Соединение с базой данных"""
    return mysql.connect(**config)


def get_columns(table):
    """Функция получения списка столбцов таблицы
    :param table: Имя таблицы
    :return: Список столбцов"""
    try:
        connection = db_connect()
        with connection.cursor() as cursor:
            query = f"SHOW COLUMNS FROM {table}"
            cursor.execute(query)
            columns = cursor.fetchall()
        connection.close()
        result = [column[0] for column in columns]
        return result
    except Error as e:
        print(f'The error was occurred at the function get_columns:\n{e}')


def get_contracts_numbers(table):
    """Функция получения списка контрактов
    :param table: Имя таблицы
    :return: Список контрактов"""
    try:
        connection = db_connect()
        with connection.cursor() as cursor:
            query = f"SELECT id, regNum, publish_date FROM {table}"
            cursor.execute(query)
            ids = cursor.fetchall()
        connection.close()
        result = {}
        for i in ids:
            result[i[0]] = {'id': i[0], 'regNum': i[1], 'publish_date': i[2]}
        return result
    except Exception as e:
        print(f'The error was occurred at the function get_contracts_numbers:\n{e}')


def get_suppliers_info(table, region):
    """Функция получения информации о подрядчиках
    :param table: Имя таблицы
    :param region: Регион
    :return: Информация о подрядчиках"""
    try:
        connection = db_connect()
        query = f"""
SELECT 
  `t`.`suppliersINN`, 
  `t`.`suppliersKPP`, 
  `t`.`suppliersfullName`, 
  `t`.`suppliersaddress`, 
  `t`.`supplierscontactEMail`, 
  `t`.`supplierscontactPhone`, 
  `t`.`supplierslastName`, 
  `t`.`suppliersfirstName`, 
  `t`.`suppliersmiddleName` 
FROM 
  `{table}` AS `t` 
WHERE 
  `t`.`region` = '{region}' 
  AND `t`.`suppliersINN` IS NOT NULL"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            contracts = cursor.fetchall()
        connection.close()
        result = []
        for contract in contracts:
            inn = contract[0].split(';:;')
            kpp = None if contract[1] is None else contract[1].split(';:;')
            name = None if contract[2] is None else contract[2].split(';:;')
            address = None if contract[3] is None else contract[3].split(';:;')
            email = None if contract[4] is None else contract[4].split(';:;')
            phone = None if contract[5] is None else contract[5].split(';:;')
            last_name = None if contract[6] is None else contract[6].split(';:;')
            first_name = None if contract[7] is None else contract[7].split(';:;')
            middle_name = None if contract[8] is None else contract[8].split(';:;')
            k = 0

            for _ in inn:
                pres = {
                    'inn': inn[k],
                    'kpp': '' if kpp is None else (kpp[0] if k >= len(kpp) else kpp[k]),
                    'name': '' if name is None else (name[0] if k >= len(name) else name[k]),
                    'address': '' if address is None else (address[0] if k >= len(address) else address[k]),
                    'email': '' if email is None else (email[0] if k >= len(email) else email[k]),
                    'phone': '' if phone is None else (phone[0] if k >= len(phone) else phone[k]),
                    'fio': '' if last_name is None else (last_name[0] if k >= len(last_name) else last_name[k])}
                pres['fio'] += '' if first_name is None else ' ' + (
                    first_name[0] if k >= len(first_name) else first_name[k])
                pres['fio'] += '' if middle_name is None else ' ' + (
                    middle_name[0] if k >= len(middle_name) else middle_name[k])

                result.append(pres)
                k += 1
        return result
    except Error as e:
        print(f'The error was occurred at the function get_suppliers_info:\n{e}')


def update_values(table, columns, values):
    """Функция обновления записей в таблице
    :param table: Имя таблицы
    :param columns: Перечень имен столбцов в виде списка
    :param values: Данные для записи в виде списка кортежей"""
    try:
        connection = db_connect()
        columns = columns[3:]
        columns = [f"{column} = IFNULL(%s, DEFAULT({column}))" for column in columns]
        sets = ', '.join(columns)
        for idx, value in enumerate(values):
            values[idx] = tuple(list(value)[1:-1] + [value[0]])
        query = f"UPDATE {table} SET {sets} WHERE regNum = %s"
        with connection.cursor() as cursor:
            cursor.executemany(query, values)
            connection.commit()
        connection.close()
        return True
    except Error as e:
        print(f'The error was occurred at the function update_values:\n{e}')


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
        print(f'The error was occurred at the function insert_values:\n{e}')


def parse_for_update(columns, values):
    data = {}
    for idx, column in enumerate(columns):
        data[column] = {}
        for value in values:
            data[column][value[0]] = value[idx + 1]
    return data


def parse_sql(data, region):
    """Функция парсера БД"""
    # global data.fieldsLinks
    # columns_to_add = []
    preval = {}
    values = []
    # updates = []
    # В зависимости от региона, получаем таблицу для записи
    if region in ['78', '47', '53', '60', '10', '29', '11', '35', '51', '83', '39']:
        table_name = 'northwestern_fd'
    elif region in ['32', '33', '37', '40', '44', '57', '62', '67', '69', '71', '76', '31', '36', '46', '48', '68']:
        table_name = 'central_fd'
    elif region in ['52', '43', '12', '13', '21', '58', '73', '64', '63', '56', '02', '16', '18', '59']:
        table_name = 'volga_fd'
    elif region in ['08', '34', '30', '01', '61', '23']:
        table_name = 'southern_fd'
    elif region in ['26', '15', '09', '07', '20', '06', '05']:
        table_name = 'north_caucasian_fd'
    elif region in ['66', '74', '45', '72', '89', '86']:
        table_name = 'ural_fd'
    elif region in ['04', '22', '54', '70', '42', '55', '19', '17', '24', '38', '03', '75']:
        table_name = 'siberian_fd'
    elif region in ['14', '79', '87', '25', '27', '28', '41', '49', '65']:
        table_name = 'far_eastern_fd'
    elif region in ['77', '50']:
        table_name = 'moscow_and_moscow_region'
    else:
        table_name = 'crimean_fd'

    contract_numbers = get_contracts_numbers(table_name)
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


# contract_numbers = get_contracts_numbers('crimean_fd')
# print(contract_numbers[164013710])