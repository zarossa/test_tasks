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
    """Функция получения списка незагруженных файлов
    :param ftp: FTP-соединение
    :param server_files: Файлы на сервере
    :param local_files: Файлы скачанные
    :return: Список файлов для загрузки"""
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
            year = int(
                file.replace('prevMonth/', '').replace('currMonth/', '').replace('contract_', '').replace(
                    'control99doc_', '').replace(reg + '_', '').split('_')[0][:4])
            if year != 2022:
                continue
            list_files.append(file)
        return list_files
    except Exception as error:
        print(f'Error of making a list\n{error}')
