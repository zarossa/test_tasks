from data import config
from data import columns
import data
import mysql.connector
# from mysql.connector import cursor
from mysql.connector import Error

tables = [
    'northwestern_fd',
    'central_fd',
    'volga_fd',
    'southern_fd',
    'north_caucasian_fd',
    'ural_fd',
    'siberian_fd',
    'far_eastern_fd',
    'moscow_and_moscow_region',
    'crimean_fd',
    '_accountDetails',
    '_attachments',
    '_bankGuaranteePayment',
    '_bankGuaranteeTermination',
    '_counterpartiesInfo',
    '_delayWriteOffPenalties',
    '_enforcement',
    '_executionObligationGuarantee',
    '_executionPeriod',
    '_executions',
    '_finances',
    '_finance_stages',
    '_payments',
    '_foundation',
    '_holdCashEnforcement',
    '_modification',
    '_penalties',
    '_products',
    '_qualityGuaranteeInfo',
    '_guaranteeReturns',
    '_refundOverpaymentsInfo',
    '_subContractorsSum',
    '_suppliers',
    '_termination'
    ]


def db_connect():
    """Соединение с базой данных"""
    return mysql.connector.connect(**config)


def execute_query(query):
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as er:
        print(f"The error '{er}' occurred")


def execute_read_query(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as er:
        print(f"The error '{er}' occurred")

region = '91'
region_name = data.regions(region)
table_name = data.table_name(region)
print(table_name, region_name)
criteria = [1990103427322000002]
new_data = set()
try:
    connection = db_connect()
    print('success')
    for i in tables:
        with connection.cursor() as cursor:
            delete = f"DELETE FROM `{i}`"
            execute_query(delete)
            # select_users = f"SELECT id FROM `{table_name}` WHERE Регион = '{region_name}' and Заказчик_ИНН != 'NULL'"
            # info = execute_read_query(select_users)
            # query = f"SELECT Внешняя_ссылка FROM {i}"
            # print(query)
            # cursor.execute(query)
            result = cursor.fetchall()
    # result = [i[0] for i in result]
    # print(result)
    data = []
    mini = {}
    # print(len(info))
    # for i in info:
    #     for idx, line in enumerate(i):
    #         if line is None:
    #             continue
    #         if type(line) is not int:
    #             if ';:;' in line:
    #                 line = line.split(';:;')
    #         mini[columns[idx]] = line
    #     data.append(mini)
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
    # with open('logs/data.txt', 'w') as log:
    #     for line in data:
    #         for i in line:
    #             log.write(f'{i}: {line[i]}\n')
    #
    # for line in data:
    #
    #     for i in line:
    #         print(f'{i}: {line[i]}')
    #     print('\n\n')
except Error as e:
    print(f'The error {e} was occurred')
