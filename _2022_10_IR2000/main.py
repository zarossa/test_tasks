import datetime  # импорт стандартных библиотек
import os
import zipfile
import sys
import errno

import data  # импорт функций
import parser_xml
import sql
import ftp
from data import direction

"""Переменная для отслеживания прогресса загрузки из консоли
0 - отображается сокращенная информация
1 - отображается подробная информация
Для работы из консоли можно включить 1, но если в консоли работы не проводятся, то включаем 0, иначе логфайл захламится 
инфой из циклов, так как вывод инфы в файл не понимает возврат коретки (\r)"""
console_debug = 0

all_data = {}  # Массив для записи данных
all_long_data = {}
chank_size = 500  # Размера чанка
number_try = 0


def archive_downloading(ftp_con, list_of_files, reg, dir=direction + 'tmp/'):
    """Функция скачивания архивов на локальный сервер
    :param ftp_con: Соединение
    :param list_of_files: Список файлов для скачивания
    :param reg: Имя региона
    :param dir: Директория скачивания"""
    try:
        text = f'Start to download data from {reg}'
        print(text)
        with open(direction + 'logs/log.txt', 'a') as reg:
            reg.write(f'{text}\n')
        for archive in list_of_files:
            ftp.ftp_download(ftp_con, archive, dir)
    except Exception as error:
        print(f'Неудачная попытка загрузки\n{error}')
        with open(direction + 'logs/error.txt', 'a') as log:
            log.write(f'Неудачная попытка загрузки {reg}\n{error}\n\n')


def archive_reading(archive_file, reg, table_name, len_list_files):
    """Функция чтения архивов
    :param archive_file: Архив
    :param reg: Номер региона
    :param table_name: Название SQL таблицы
    :param len_list_files: Количество архивов"""
    arch_start = 1
    xml_start = 1
    global all_files
    global all_long_data
    global false_files
    global true_files
    global error_files
    global all_data
    global chank
    global chank_long
    global chank_size
    region_name = data.regions(reg)
    # print(f'read {archive_file}')
    with zipfile.ZipFile(archive_file, 'r') as f:
        all_files += len(f.namelist())

        # Перебор файлов в архиве
        for arch_file in f.namelist():
            # Отсеиваем лишние файлы
            if 'sig' in arch_file or 'Available' in arch_file or 'Cancel' in arch_file:
                false_files += 1
                continue
            true_files += 1
            len_files = 0

            try:
                # Получаем содержимое файла в байтовом виде и отправляем в парсер на обработку
                one_object = parser_xml.read_xml(f.read(arch_file), region_name, archive_file)
                id_file = list(one_object.keys())[0]
                # for i in one_object[id_file]:
                #     len_files += len(one_object[id_file][i])
                # if len_files < 8000:
                all_data.update(one_object)
                chank += 1
                # else:
                #     all_long_data.update(one_object)
                #     chank_long += 1
                # if console_debug == 1:
                # print('Parsing xml ' + str(round(
                #     xml_start * (arch_start * 100 / len_list_files) / len(f.namelist()))) + '%',
                #       end='\n')
                xml_start += 1

                if chank > chank_size - 1:
                    sql.parse_sql(all_data, reg, region_name, table_name)
                    all_data = {}
                    chank = 0
                # if chank_long > 0:  #chank_size // 10 - 1:
                #     sql.parse_sql(all_long_data, reg, region_name, table_name, True)
                #     all_long_data = {}
                #     chank_long = 0
            except Exception as error:
                with open(direction + 'logs/error.txt', 'a') as log:
                    log.write(f'Ошибка чтения\n{archive_file}\n{arch_file}\n{error}\n\n')
                error_files += 1
                continue


try:
    with open(direction + 'logs/log.txt', 'w') as f:
        f.write(f'Процесс\n')
    with open(direction + 'logs/regions.txt', 'w') as f:
        f.write(f'Обработанные регионы\n')
    with open(direction + 'logs/error.txt', 'w') as f:
        f.write(f'Запись ошибок\n')
    # Перебор регионов
    for region in data.all_regions:
        try:
            for file in os.listdir(direction + 'tmp'):
                os.remove(direction + 'tmp/' + file)
            region_name = data.regions(region)  # Получаем название региона по его индексу
            table_name = data.table_name(region)  # Получаем название SQL таблицы по индексу региона
            with open(direction + 'logs/regions.txt', 'a') as reg:
                reg.write(f'{region_name}\n')
            arch_start = 1

            # Проверка полученного региона на возможные ошибки
            if region_name == 0:
                text = f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} Региона с кодом {region} не существует'
                print(text)
                with open(direction + 'logs/log.txt', 'a') as reg:
                    reg.write(f'{text}\n')
                continue

            text = f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} {region} {region_name} START'
            print(text)
            with open(direction + 'logs/log.txt', 'a') as reg:
                reg.write(f'{text}\n')

            # Устанавливаем соединение и скачиваем архивы на локальный сервер
            ftp_connect = ftp.ftp_connect()
            if ftp_connect:
                list_files = ftp.ftp_make_list_files(ftp_connect, region_name)
                list_files = ftp.ftp_list_of_new(list_files, table_name, region_name)
                download_files = []
                number_try = 0
                while len(list_files) > len(download_files):
                    number_try += 1
                    list_files_local = dict()
                    for file in os.listdir(direction + 'tmp'):
                        list_files_local[file] = os.stat(f'{direction}tmp/{file}')[6]
                    list_of_files = ftp.ftp_list_of_download(ftp_connect, set(list_files), list_files_local)
                    archive_downloading(ftp_connect, list_of_files, region_name)
                    download_files = os.listdir(direction + 'tmp')
                    if number_try > 5:
                        break
                ftp_connect.close()  # Закрываем соединение
            else:
                text = f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} Не удалось установить связь с FTP-сервером'
                print(text)
                with open(direction + 'logs/log.txt', 'a') as reg:
                    reg.write(f'{text}\n')
                continue
            # if console_debug == 1:
            #     print('')  # Перенос строки после вывода процента скачаных архивов (не удалять, нужно)
            text = f'Download complete: {len(download_files)} archives'
            print(text)
            with open(direction + 'logs/log.txt', 'a') as reg:
                reg.write(f'{text}\n')
            list_files = os.listdir(direction + 'tmp')
            chank = 0
            chank_long = 0
            all_files = 0
            true_files = 0
            false_files = 0
            error_files = 0

            # Перебор архивов
            for tmp_file in list_files:
                try:
                    archive_reading(direction + 'tmp/' + tmp_file, region, table_name, len(list_files))
                except Exception as error:
                    with open(direction + 'logs/error.txt', 'a') as log:
                        log.write(f'Archive error\n{tmp_file}\n{error}\n\n')

            if console_debug == 1:
                print('')  # Перенос строки после вывода процента скачаных архивов (не удалять, нужно)

            # Добавляем оставшиеся записи в БД после обработки региона
            sql.parse_sql(all_data, region, region_name, table_name)
            # sql.parse_sql(all_long_data, region, region_name, table_name, True)
            all_data = {}
            all_long_data = {}

            chank = 0
            chank_long = 0

            # Получаем список файлов временной папки и удаляем их
            for file in os.listdir(direction + 'tmp'):
                os.remove(direction + 'tmp/' + file)

            text = f'''All: {all_files} status: {all_files == true_files + false_files}
            True: {true_files} False: {false_files}\nErrors: {error_files} files\n{region} {region_name} STOP'''
            print(text)
            with open(direction + 'logs/log.txt', 'a') as reg:
                reg.write(f'{text}\n')
        except IOError as ioe:
            text = f'Ошибка ввода/вывода!\n{ioe}'
            with open(direction + 'logs/log.txt', 'a') as reg:
                reg.write(text)
            with open(direction + 'logs/error.txt', 'a') as log:
                log.write(text)
            if ioe.errno == errno.EPIPE:
                pass

    text = 'Скрипт закончил работу\n'
    print(text)
    with open(direction + 'logs/log.txt', 'a') as reg:
        reg.write(text)
except Exception as e:
    text = f'!!! Ошибка в выполнении скрипта !!!\n{e}'
    print(text)
    with open(direction + 'logs/log.txt', 'a') as reg:
        reg.write(text)
    with open(direction + 'logs/error.txt', 'a') as log:
        log.write(text)
