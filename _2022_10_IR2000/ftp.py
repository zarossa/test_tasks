from ftplib import FTP


def ftp_connect():
    """Функция подключения к FTP госзакупок
    :return: Возвращает соединение"""
    ftp = False
    for i in range(0, 5):
        try:
            ftp = FTP(host='ftp.zakupki.gov.ru', user='free', passwd='free')  # Устанавливаем соединение
            break
        except Exception as e:
            print(f'Неудачная попытка соединения #{i+1}\n{e}')
            continue
    return ftp


def ftp_cwd(ftp, direction):
    """Функция получения списка файлов и папок в директории на FTP
    :param ftp: FTP-соединение
    :param direction: Директория, из которой нужно получить список файлов и папок
    :return: Возвращает список файлов и папок"""
    ftp.cwd(direction)  # Переходим в нужную директорию
    return ftp.nlst()


def ftp_list_of_download(ftp, server_files, local_files):
    """Функция получения списка файлов для дозагрузки нескачанных файлов
    :param ftp: FTP-соединение
    :param server_files: Файлы на сервере
    :param local_files: Файлы скачанные
    :return: Список файлов для дозагрузки"""
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


def ftp_download(ftp, file, path_tmp='tmp/'):
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
