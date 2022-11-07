"""
1. Подключиться к серверу
модуль ftp - DONE

2. Скачать необходимые файлы
модуль download, data

3. Собрать интересующую инфу с файлов
модуль parser

4. Обновить и добавить дату в БД
модуль sql
"""

import datetime  # импорт стандартных библиотек
import os
import zipfile

import data  # импорт функций
# import download
import parser_xml
import sql
import ftp

"""Переменная для отслеживания прогресса загрузки из консоли
0 - отображается сокращенная информация
1 - отображается подробная информация
Для работы из консоли можно включить 1, но если в консоли работы не проводятся, то включаем 0, иначе логфайл захламится 
инфой из циклов, так как вывод инфы в файл не понимает возврат коретки (\r)"""
console_debug = 1

all_data = {}  # Массив для записи данных
data_contracts = []  # Массив для глобального хранения ID извещений
chank_size = 500  # Размера чанка

try:
    # Перебор регионов
    for region in data.all_regions:
        # region = '13'
        region_name = data.regions(region)  # Получаем название региона по его индексу
        arch_start = 1

        # Проверка полученного региона на возможные ошибки
        if region_name == 0:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), f'Региона с кодом {region} не существует')
            continue

        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), region, region_name, 'START')
        tmp_files = []

        # Устанавливаем соединение и скачиваем архивы на локальный сервер
        ftp_connect = ftp.ftp_connect()

        if ftp_connect:
            # Переходим в папку с текущим регионом и получаем список архивов
            file_list_curr = ftp.ftp_cwd(ftp_connect, '/fcs_regions/' + region_name + '/contracts/currMonth')
            file_list_prev = ftp.ftp_cwd(ftp_connect, '/fcs_regions/' + region_name + '/contracts/prevMonth')
            file_list = ftp.ftp_cwd(ftp_connect, '/fcs_regions/' + region_name + '/contracts')
            # file_list = ftp.ftp_cwd(ftp_connect, '/fcs_regions/' + region_name + '/contracts/currMonth')

            # for file in file_list_curr:
            #     file = 'currMonth/' + file
            # for file in file_list:
            #     file = 'currMonth/' + file
            for file in range(len(file_list_curr)):
                file_list_curr[file] = 'currMonth/' + file_list[file]

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
                # if '_2021' not in fileName and '_2022' not in fileName:
                year = int(
                    file.replace('prevMonth/', '').replace('currMonth/', '').replace('contract_', '').replace(
                        'control99doc_', '').replace(region_name + '_', '').split('_')[0][:4])
                if year != 2022:
                    if console_debug == 1:
                        print(f'Download archives {str(round(arch_start * 100 / len(file_list)))}%', end='\n')

                    arch_start = arch_start + 1
                    continue

                # Закачаваем архив во временную папку tmp
                file_zip = ftp.ftp_download(ftp_connect, file)
                tmp_files.append(file_zip)

                if console_debug == 1:
                    print(f'Download archives {str(round(arch_start * 100 / len(file_list)))}%', end='\n')

                arch_start += 1
            ftp_connect.close()  # Закрываем соединение
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 'Не удалось установить связь с FTP-сервером')
            continue

        if console_debug == 1:
            print('')  # Перенос строки после вывода процента скачаных архивов (не удалять, нужно)
        print(f'Download complete: {len(tmp_files)} archives')

        chank = 0
        all_files = 0
        true_files = 0
        false_files = 0
        error_files = 0

        # Перебор архивов
        for idx, tmp_file in enumerate(tmp_files):
            # Пропуск нечитаемого/несуществующего файла (с этим возникали какие-то проблемы,
            # парсер ссылался на несуществующий файл, видимо где-то были дубли)
            try:
                arch_start = 1
                xml_start = 1
                file_zip_open = zipfile.ZipFile(tmp_file, 'r')  # Открытие zip-архива
                all_files += len(file_zip_open.namelist())

                # Перебор файлов в архиве
                for index, file in enumerate(file_zip_open.namelist()):
                    # Отсеиваем лишние файлы
                    if 'Procedure' in file or 'sig' in file or 'Available' in file or 'contract' not in file \
                            or 'Cancel' in file:
                        false_files += 1
                        continue

                    true_files += 1

                    try:
                        # Получаем содержимое файла в байтовом виде и отправляем в парсер на обработку
                        oneObject = parser_xml.read_xml(file_zip_open.read(file))
                        oneObjectID = list(oneObject.keys())[0]
                        if oneObjectID not in data_contracts:
                            data_contracts.append(oneObjectID)
                            all_data.update(oneObject)
                        elif oneObject[oneObjectID]['publishDate'] >= all_data[oneObjectID]['publishDate']:
                            all_data[oneObjectID] = oneObject[oneObjectID]
                        if console_debug == 1:
                            print('Parsing xml ' + str(round(
                                xml_start * (arch_start * 100 / len(tmp_files)) / len(file_zip_open.namelist()))) + '%',
                                  end='\n')
                        xml_start = xml_start + 1

                        chank += 1

                        if chank > chank_size - 1:
                            sql.parse_sql(all_data, region)
                            all_data = {}
                            chank = 0
                    except Exception as er:
                        print(er)
                        error_files = error_files + 1
                        continue
                file_zip_open.close()
            except Exception as ex:
                print(f'Archive error\n{ex}')
                continue

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
