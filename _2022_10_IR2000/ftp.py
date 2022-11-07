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


def ftp_download(ftp, file):
    """Функция скачивания файла с FTP
    :param ftp: FTP-соединение
    :param file: Путь до файла, относительно текущей директории (устонавливается перед запуском функции)
    :return: Возвращает путь до файла во временной папке"""
    # path_tmp = '/home/parser/contracts/tmp/'  # Расположение временной папки
    path_tmp = 'tmp/'  # Расположение временой папки

    # Дописываем в путь дополнительные префиксы при наличии вложенных папок
    if 'currMonth/' in file or 'prevMonth/' in file:
        file = file.split('/')[1]
    # Сохраняем файл на сервере
    with open(path_tmp + file, "wb") as f:
        ftp.retrbinary("RETR " + file, f.write)

    return path_tmp + file
