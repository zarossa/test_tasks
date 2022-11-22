import datetime  # импорт стандартных библиотек
import os
import zipfile

import data  # импорт функций
import parser_xml
import sql
import ftp

"""Переменная для отслеживания прогресса загрузки из консоли
0 - отображается сокращенная информация
1 - отображается подробная информация
Для работы из консоли можно включить 1, но если в консоли работы не проводятся, то включаем 0, иначе логфайл захламится 
инфой из циклов, так как вывод инфы в файл не понимает возврат коретки (\r)"""
console_debug = 0

all_data = {}  # Массив для записи данных
data_contracts = []  # Массив для глобального хранения ID извещений
chank_size = 500  # Размера чанка
number_try = 0


def make_list_files(ftp_con, reg):
    """Функция создания списка скачиваемых файлов
    :param ftp_con: Соединение
    :param reg: Название региона
    :return: Возвращает список файлов для скачивания"""
    try:
        list_files = []

        # Переходим в папку с текущим регионом и получаем список архивов
        file_list_curr = ftp.ftp_cwd(ftp_con, '/fcs_regions/' + reg + '/contracts/currMonth')
        file_list_prev = ftp.ftp_cwd(ftp_con, '/fcs_regions/' + reg + '/contracts/prevMonth')
        file_list = ftp.ftp_cwd(ftp_con, '/fcs_regions/' + reg + '/contracts')
        for file in range(len(file_list_curr)):
            file_list_curr[file] = 'currMonth/' + file_list_curr[file]

        for file in range(len(file_list_prev)):
            if file_list_prev[file] in file_list:
                del file_list_prev[file]
            else:
                file_list_prev[file] = 'prevMonth/' + file_list_prev[file]

        file_list.remove('currMonth')
        file_list.remove('prevMonth')

        file_list += file_list_curr + file_list_prev
        del file_list_prev
        del file_list_curr
        for file in file_list:
            # Пропускаем все архивы, кроме 2021 года и более
            year = int(
                file.replace('prevMonth/', '').replace('currMonth/', '').replace('contract_', '').replace(
                    'control99doc_', '').replace(reg + '_', '').split('_')[0][:4])
            if year != 2022:
                continue
            list_files.append(file)
        return list_files
    except Exception as error:
        print(f'Archive error\n{error}')


def archive_downloading(ftp_con, list_of_files, reg, direction='tmp/'):
    """Функция скачивания архивов на локальный сервер
    :param ftp_con: Соединение
    :param list_of_files: Список файлов для скачивания
    :param reg: Имя региона
    :param direction: Директория скачивания"""
    try:
        print(f'Start to download data from {reg}')
        for archive in list_of_files:
            ftp.ftp_download(ftp_con, archive, direction)
    except Exception as error:
        print(f'Неудачная попытка загрузки\n{error}')


def archive_reading(archive_file, reg, len_list_files):
    """Функция чтения архивов
    :param reg: Номер региона
    :param archive_file: Архив
    :param len_list_files: Количество архивов"""
    arch_start = 1
    xml_start = 1
    global all_files
    global false_files
    global true_files
    global error_files
    global all_data
    global chank
    global chank_size
    with zipfile.ZipFile(archive_file, 'r') as f:
        all_files += len(f.namelist())

        # Перебор файлов в архиве
        for arch_file in f.namelist():
            # Отсеиваем лишние файлы
            if 'sig' in arch_file or 'Available' in arch_file or 'Cancel' in arch_file:
                false_files += 1
                continue
            true_files += 1

            try:
                # Получаем содержимое файла в байтовом виде и отправляем в парсер на обработку
                one_object = parser_xml.read_xml(f.read(arch_file))
                id_file = list(one_object.keys())[0]
                all_data.update(one_object)
                # if console_debug == 1:
                # print('Parsing xml ' + str(round(
                #     xml_start * (arch_start * 100 / len_list_files) / len(f.namelist()))) + '%',
                #       end='\n')
                xml_start += 1
                chank += 1

                if chank > chank_size - 1:
                    sql.parse_sql(all_data, reg)
                    all_data = {}
                    chank = 0
            except Exception as error:
                with open(f'logs/_log.txt', 'a') as log:
                    log.write(f'{archive_file}\n{file}\n{error}\n\n')
                error_files += 1
                continue


try:
    # Перебор регионов
    for region in data.all_regions:
        # Проверка на наличие файлов в скачанном
        if os.listdir('tmp') and number_try < 5:
            number_try += 1
            try:
                region_name = os.listdir('tmp')[0].split('_')[1]
                for name in data.region_names:
                    if region_name in name:
                        region_name = name
                        break
                region_temp = data.region_names.get(region_name, 0)
                print(f'Дополнительная попытка №{number_try}')
                print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), region_temp, region_name, 'START')
                list_files_local = dict()
                for file in os.listdir('tmp'):
                    list_files_local[file] = os.stat(f'tmp/{file}')[6]
                ftp_connect = ftp.ftp_connect()
                if ftp_connect:
                    file_list = ftp.ftp_cwd(ftp_connect, '/fcs_regions/' + region_name + '/contracts')
                    list_files_server = set(make_list_files(ftp_connect, region_name))
                    list_of_ftp_files = ftp.ftp_list_of_download(ftp_connect, list_files_server, list_files_local)
                    try:
                        archive_downloading(ftp_connect, list_of_ftp_files, region_name)
                    except Exception as error:
                        print(f'Archive error\n{error}')
                    ftp_connect.close()
                    list_files = os.listdir('tmp')
                    print(f'Download complete: {len(list_files)} archives')
                    chank = 0
                    all_files = 0
                    true_files = 0
                    false_files = 0
                    error_files = 0
                    # Перебор архивов
                    for tmp_file in list_files:
                        archive_reading('tmp/' + tmp_file, region_temp, len(list_files))

                    # Добавляем оставшиеся записи в БД после обработки региона
                    sql.parse_sql(all_data, region_temp)
                    all_data = {}
                    data_contracts = []
                    chank = 0

                    # Получаем список файлов временной папки и удаляем их
                    for file in os.listdir('tmp'):
                        os.remove('tmp/' + file)

                    print(f'All: {all_files} status: {all_files == true_files + false_files} True: {true_files} '
                          f'False: {false_files}')
                    print(f'Errors: {error_files} files')
                    print(f'{region_temp} {region_name} STOP')
            except Exception as error:
                print(error)
        else:
            for file in os.listdir('tmp'):
                os.remove('tmp/' + file)
        region_name = data.regions(region)  # Получаем название региона по его индексу
        with open(f'logs/reg.txt', 'a') as reg:
            reg.write(region_name)  # Чтение архивов и сбор по папочкам-контрактам
        arch_start = 1

        # Проверка полученного региона на возможные ошибки
        if region_name == 0:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), f'Региона с кодом {region} не существует')
            continue

        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), region, region_name, 'START')
        # tmp_files = []

        # Устанавливаем соединение и скачиваем архивы на локальный сервер
        ftp_connect = ftp.ftp_connect()
        if ftp_connect:
            list_files = make_list_files(ftp_connect, region_name)
            archive_downloading(ftp_connect, list_files, region_name)
            ftp_connect.close()  # Закрываем соединение
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 'Не удалось установить связь с FTP-сервером')
            continue
        # if console_debug == 1:
        #     print('')  # Перенос строки после вывода процента скачаных архивов (не удалять, нужно)
        print(f'Download complete: {len(list_files)} archives')
        list_files = os.listdir('tmp')
        chank = 0
        all_files = 0
        true_files = 0
        false_files = 0
        error_files = 0

        # Перебор архивов
        for tmp_file in list_files:
            # Пропуск нечитаемого/несуществующего файла (с этим возникали какие-то проблемы,
            # парсер ссылался на несуществующий файл, видимо где-то были дубли)
            try:
                archive_reading('tmp/' + tmp_file, region, len(list_files))
            except Exception as error:
                print(f'Archive error\n{error}')

        if console_debug == 1:
            print('')  # Перенос строки после вывода процента скачаных архивов (не удалять, нужно)

        # Добавляем оставшиеся записи в БД после обработки региона
        sql.parse_sql(all_data, region)
        all_data = {}
        data_contracts = []
        chank = 0

        # Получаем список файлов временной папки и удаляем их
        for file in os.listdir('tmp'):
            os.remove('tmp/' + file)

        print(f'All: {all_files} status: {all_files == true_files + false_files} True: {true_files} '
              f'False: {false_files}')
        print(f'Errors: {error_files} files')
        print(f'{region} {region_name} STOP')
except Exception as e:
    print(f'!!! Ошибка в выполнении скрипта !!!\n{e}')
