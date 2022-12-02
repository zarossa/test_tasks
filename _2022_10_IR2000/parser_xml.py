import xml.etree.ElementTree as ET
import re


def etree_to_json(etree_data):
    """Функция преобразования объекта etree в JSON-массив
    :param etree_data: etree-объект
    :return: JSON-массив"""
    json_data = [{etree_data.tag: parse_json(etree_data)}]
    return json_data


def parse_json(parents):
    """Функция перебора структуры для JSON
    :param parents: Родительский элемент, который перебераем
    :return: Возвращает результат перебора"""
    result = []
    for child in parents:
        if child.text is None:  # Если дочерний элемент не текст, то рекурсивно заходим глубже
            result.append({child.tag: parse_json(child)})
        else:  # Если дочерний элемент является текстом, то записываем результат перебора
            result.append({child.tag: child.text})
    return result


def etree_to_dict(etree_data):
    """Функция преобразования объекта etree в словарь
    :param etree_data: etree-объект
    :return: Возвращает словарь"""
    dict_data = {etree_data.tag: parse_dict(etree_data)}
    return dict_data[list(dict_data.keys())[0]]


def parse_dict(parents):
    """Функция перебора структуры для словаря
    :param parents: Родительский элемент, который перебераем
    :return: Возвращает результат перебора"""
    result = {}  # Переменная для записи результата перебора

    for child in parents:
        if child.tag not in result:  # Если в переменной нет записи по текущему дочернему элементу, то делаем проверку
            if child.text is None:  # Если дочерний элемент является текстом, то записываем результат перебора
                result[child.tag] = parse_dict(child)
            else:  # Если дочерний элемент не текст, то рекурсивно заходим глубже
                result[child.tag] = child.text
        else:  # Если в переменной есть запись по текущему дочернему элементу, то обрабатываем эту запись
            if isinstance(result[child.tag], dict):  # Если текущий дочерний элемент - словарь, то создаем список
                # и добавляем в него дочерний элемент и вызываем рекурсию
                result[child.tag] = [result[child.tag]]
                result[child.tag].append(parse_dict(child))
            elif isinstance(result[child.tag], str):
                pass
            else:  # Если текущий дочерний элемент не словарь, то добавляем в него дочерний элемент и вызываем рекурсию
                result[child.tag].append(parse_dict(child))
    return result


def parse_xml(xml_object):
    """Функция парсера
    :param xml_object: Объект для обработки
    :return: Возвращает результат перебора"""
    try:
        result = {}  # Переменная для записи результата перебора
        file_id = xml_object['id']  # Получаем id файла и создаем массив для него
        result[file_id] = {}
        # Перебор элементов объекта и запись в массив
        for child in xml_object:
            if isinstance(xml_object[child], str):  # Если дочерний элемент - строка, то делаем запись без обработки
                result[file_id][child] = xml_object[child]
            elif isinstance(xml_object[child], list):
                temp = {child: xml_object[child]}
                res = get_field(temp, child)
                result[file_id].update(res)
            else:  # Если дочерний элемент - это не строка, то делаем обработку перед записью
                res = get_field(xml_object[child], child)  # Вызываем рекурсивную функцию для перебора дочерних эл-тов
                result[file_id].update(res)  # Результат добавляем в основной массив
        return result
    except Exception as ex:
        pass


def get_field(parent_element, parent_name='', parent_type=False):
    """Функция получения поля и его значения
    :param parent_element: Родительский элемент, чьи поля будем сохранять
    :param parent_name: Имя родителя для склейки имен (по-умолчанию пустое)
    :param parent_type:
    :return:
    """
    result = {}  # Переменная для записи результата перебора

    for elem in parent_element:
        if parent_type:
            if isinstance(parent_element[elem], str):
                result[parent_name + elem] = parent_element[elem]
            elif isinstance(parent_element[elem], list):
                # ЭТО ПОЛНАЯ ЗАЛЕПА, ЭТУ ЧАСТЬ КОДА Я ПИСАЛ ПОД ЖЕСТКИМИ ПЫТКАМИ #
                for el in parent_element[elem]:
                    res = get_field(el, '', True)

                    for r in res:
                        e_key = parent_name + elem + r
                        if e_key not in result:
                            result[e_key] = res[r]
                        else:
                            result[e_key] += ';:;' + res[r]
            else:
                res = get_field(parent_element[elem], elem, True)
                for r in res:
                    result[r] = res[r]
        elif isinstance(parent_element[elem], str):
            # Если текущий элемент - это строка, то делаем запись в переменную
            result[parent_name + elem] = parent_element[elem]
        elif isinstance(parent_element[elem], list):

            for el in parent_element[elem]:
                res = get_field(el, '', True)

                for r in res:
                    e_key = parent_name + elem + r
                    if e_key not in result:
                        result[e_key] = res[r]
                    else:
                        result[e_key] += ';:;' + res[r]

        else:
            # Если текущий элемент - это не строка и не список, то вызываем рекурсию, передавая в нее дочерний элемент
            res = get_field(parent_element[elem], parent_name + elem)
            for r in res:
                result[r] = res[r]  # Результат рекурсии записываем в переменную
    return result


def read_xml(xml_file, region_name, archive):
    """Функция чтения файла и первичной обработки перед парсером
    :param xml_file: xml-файл в байтовом виде
    :return: Возвращает информацию для БД"""
    xml_file = xml_file.decode('utf-8')  # Преобразуем байтовый файл в строку, меняя кодировку в utf-8
    xml_file = re.sub(r'<ns\d:', '<', xml_file)  # Убираем не нужные префиксы из тегов
    xml_file = re.sub(r'</ns\d:', '</', xml_file)  # ...
    xml_file = re.sub(r' xmlns:ns\d+=\"[\w:/.]+\"', '', xml_file)  # Убираем ненужные атрибуты из тегов
    xml_file = re.sub(r' xmlns=\"[\w:/.]+\"', '', xml_file)  # ...
    xml_file = re.sub(r'\n', '', xml_file)  # Удаляем лишние переносы строк и табуляцию
    xml_file = re.sub(r'>[ ]+<', '><', xml_file)  # Удаляем бробелы между тегами
    xml_file = re.sub(r'<cryptoSigns>[\w/+"=>< -]+<\/cryptoSigns>', '', xml_file)
    xml_object = ET.fromstring(xml_file)  # Преобразуем строку в объект
    xml_object = etree_to_dict(xml_object[0])  # Преобразуем обьект в словарь для более удобной работы
    xml_object['region'] = region_name
    xml_object['archive_name'] = archive
    return parse_xml(xml_object)
