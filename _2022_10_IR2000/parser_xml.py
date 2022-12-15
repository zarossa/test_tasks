import xml.etree.ElementTree as ET
import re
from data import link_place
from data import direction



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


def go_deeper(dictionary, search_word):
    queue = list()
    for child in dictionary:
        if child == search_word:
            return [child]
        else:
            queue.append([dictionary[child], [child]])
    while queue:
        vertex = queue.pop(0)
        if type(vertex[0]) == str:
            continue
        if type(vertex[0]) == list:
            continue
        for child in vertex[0]:
            if child == search_word:
                return list(vertex[1]) + [child]
            else:
                queue.append([vertex[0][child], list(vertex[1]) + [child]])
    return None


def right_return(line, way):
    if type(line) == list:
        line = line[0]
    try:
        if len(way) > 1:
            result = right_return(line[way[0]], way[1:])
        else:
            return line[way[0]]
        return result
    except KeyError:
        return None
    except TypeError:
        pass
    # except Exception as ex:
    #     print('\n', ex)
    #     print(way, line)


def xml_reader(list_data, xml_file, link_names, id_obj, data_type='main', coord=''):
    text = ''
    for link in link_names:
        try:
            sep_link = link.split(',')
            text = right_return(xml_file, sep_link)
            if text is None:
                continue
            if type(text) == dict:
                data_type_text = link_names[link][1]
                coord_text = len(list_data[link_names[link][1]])
                try:
                    list_data[data_type][coord][link_names[link][0]] += f';:;_{data_type_text}_{id_obj}_{coord_text}'
                except KeyError:
                    list_data[data_type][coord][link_names[link][0]] = f'_{data_type_text}_{id_obj}_{coord_text}'
                list_data[data_type_text][f'{id_obj}_{coord_text}'] = {}
                xml_reader(list_data, text, link_place[data_type_text], id_obj, data_type_text, f'{id_obj}_{coord_text}')
                pass
            elif type(text) == list:
                data_type_text = link_names[link][1]
                for i in text:
                    coord_text = len(list_data[link_names[link][1]])
                    try:
                        list_data[data_type][coord][link_names[link][0]] += f';:;_{data_type_text}_{id_obj}_{coord_text}'
                    except KeyError:
                        list_data[data_type][coord][link_names[link][0]] = f'_{data_type_text}_{id_obj}_{coord_text}'
                    list_data[data_type_text][f'{id_obj}_{coord_text}'] = {}
                    xml_reader(list_data, i, link_place[data_type_text], id_obj, data_type_text, f'{id_obj}_{coord_text}')
                pass
            else:
                list_data[data_type][coord][link_names[link]] = text
                pass
        except KeyError as error:
            with open(direction + 'logs/error.txt', 'a') as log:
                log.write(f'Error in xml_reader\n{error}\n{data_type, link, text}\n\n')
    return True


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
    xml_object['archive_name'] = archive.split('/')[-1]
    return xml_object
