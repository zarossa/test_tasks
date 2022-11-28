from ftplib import FTP
from data import direction
from sql import get_contracts_numbers


def ftp_connect():
    """Функция подключения к FTP госзакупок
    :return: Возвращает соединение"""
    ftp = False
    for i in range(0, 5):
        try:
            ftp = FTP(host='ftp.zakupki.gov.ru', user='free', passwd='free')  # Устанавливаем соединение
            break
        except Exception as e:
            text = f'Неудачная попытка соединения #{i+1}\n{e}'
            print(text)
            with open(direction + 'logs/log.txt', 'a') as reg:
                reg.write(text)
            continue
    return ftp


def ftp_cwd(ftp, dir):
    """Функция получения списка файлов и папок в директории на FTP
    :param ftp: FTP-соединение
    :param dir: Директория, из которой нужно получить список файлов и папок
    :return: Возвращает список файлов и папок"""
    ftp.cwd(dir)  # Переходим в нужную директорию
    return ftp.nlst()


def ftp_list_of_download(ftp, server_files, local_files):
    """Функция создания списка незагруженных файлов
    :param ftp: FTP-соединение
    :param server_files: Файлы на сервере
    :param local_files: Файлы скачанные
    :return: Возвращает список файлов для скачивания"""
    list_files = set()
    files = dict()
    for file in local_files:
        if f'currMonth/{file}' in server_files:
            files[f'currMonth/{file}'] = local_files[file]
        elif f'prevMonth/{file}' in server_files:
            files[f'prevMonth/{file}'] = local_files[file]
        elif file in server_files:
            files[file] = local_files[file]
    for file in files:
        try:
            size = ftp.size(file)
            if size == files[file]:
                list_files.add(file)
        except:
            continue
    return server_files - list_files


def ftp_list_of_new(server_files, table_name, region_name):
    """Функция создания списка новых файлов
    :param server_files: Файлы на сервере
    :param table_name: Название SQL таблицы
    :return: Возвращает список файлов для скачивания"""
    oldest_archive = ''
    new_list_files = []
    contract_numbers = get_contracts_numbers(table_name, region_name)
    for contract in contract_numbers:
        tmp_data = contract_numbers[contract]['Название_архива']
        if oldest_archive < tmp_data:
            oldest_archive = tmp_data
    if not oldest_archive:
        return server_files
    publish_date = oldest_archive.split('/')[-1]
    for archive in server_files:
        if publish_date < archive.replace('prevMonth/', '').replace('currMonth/', ''):
            new_list_files.append(archive)
    return new_list_files


def ftp_download(ftp, file, path_tmp=direction + 'tmp/'):
    """Функция скачивания файла с FTP
    :param ftp: FTP-соединение
    :param file: Путь до файла, относительно текущей директории (устонавливается перед запуском функции)
    :param path_tmp: Расположение временой папки
    :return: Возвращает путь до файла во временной папке"""
    # Дописываем в путь дополнительные префиксы при наличии вложенных папок
    if 'currMonth/' in file or 'prevMonth/' in file:
        file_to = file.split('/')[1]
    else:
        file_to = file

    # Сохраняем файл на сервере
    with open(path_tmp + file_to, "wb") as f:
        ftp.retrbinary("RETR " + file, f.write)

    return path_tmp + file_to


def ftp_make_list_files(ftp, reg):
    """Функция создания списка скачиваемых файлов
    :param ftp: FTP-соединение
    :param reg: Название региона
    :return: Возвращает список файлов для скачивания"""
    try:
        list_files = []

        # Переходим в папку с текущим регионом и получаем список архивов
        file_list_curr = ftp_cwd(ftp, '/fcs_regions/' + reg + '/contracts/currMonth')
        file_list_prev = ftp_cwd(ftp, '/fcs_regions/' + reg + '/contracts/prevMonth')
        file_list = ftp_cwd(ftp, '/fcs_regions/' + reg + '/contracts')
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
            year = file.replace('prevMonth/', '').replace('currMonth/', '').replace('contract_', '').replace(
                    'control99doc_', '').replace(reg + '_', '').split('_')[0][:4]
            if year.isdigit():
                year = int(year)
                if year != 2022:
                    continue
                list_files.append(file)
        return list_files
    except Exception as error:
        with open(direction + 'logs/error.txt', 'a') as log:
            log.write(f'Error of making a list (ftp)\n{reg}\n{error}\n\n')
