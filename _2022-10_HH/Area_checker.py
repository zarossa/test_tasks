import sys

sys.setrecursionlimit(10000)


def region_checker(x_coord, y_coord):
    # Рекурсивно исследует карту и записывает координаты участка
    if x_coord not in range(m) or y_coord not in range(n):
        # выйти, если исследуемая ячейка за границами карты
        return
    if not area_map[x_coord][y_coord]:
        # выйти, если участок неплодородный
        return
    if area_accounting[x_coord][y_coord]:
        # выйти, если участок уже просмотрен ранее
        return
    area_accounting[x_coord][y_coord] = True
    global fields_coord
    if not fields_coord[-1]:  # запись первой кооодинаты участка
        fields_coord[-1] = [x_coord, x_coord, y_coord, y_coord]
    else:  # ввод крайних координат участка
        if fields_coord[-1][0] > x_coord:
            fields_coord[-1][0] = x_coord
        if fields_coord[-1][1] < x_coord:
            fields_coord[-1][1] = x_coord
        if fields_coord[-1][2] > y_coord:
            fields_coord[-1][2] = y_coord
        if fields_coord[-1][3] < y_coord:
            fields_coord[-1][3] = y_coord

    for x in range(x_coord - 1, x_coord + 2):
        for y in range(y_coord - 1, y_coord + 2):
            region_checker(x, y)  # рекурсивное исследование соседних ячеек карты


def square_finder(field_coord):
    # Описание плодородности и площади участка
    if not field_coord:
        return
    global fields_attribute
    fields_attribute.append([0, 0])
    for x in range(field_coord[0], field_coord[1] + 1):
        for y in range(field_coord[2], field_coord[3] + 1):
            fields_attribute[-1][1] += 1
            fields_attribute[-1][0] += area_map[x][y]
    fields_attribute[-1][0] = fields_attribute[-1][0] / fields_attribute[-1][1]


# 1. Подготовка и считывание данных
n, m = map(lambda x: int(x), input().split())  # считывание количества стобцов (n) и строк (m)
area_map = []  # массив для хранения карты региона
for i in range(m):  # считывание и заполнение данных карты в массив
    string = list(map(lambda x: int(x), input().split()))
    area_map.append(string)
area_accounting = [[0 for _ in range(n)] for _ in range(m)]  # матрица учета осмотра ячеек
fields_coord = [[]]  # координаты всех подходящих участков
fields_attribute = []  # массив со списком плодородности и площадью всех участков

# 2. Осмотр всей карты для поиска подходящих участков
for i in range(m):
    for j in range(n):
        region_checker(i, j)
        fields_coord.append([])
del area_accounting  # удаление матрицы учета осмотра ячеек

# 3. Характеризация подходящих участков
for field in fields_coord:
    square_finder(field)
del area_map  # удаление карты региона

# 4. Вывод наиболее эффективного участка для покупки
fields_attribute = sorted(fields_attribute, reverse=True)  # сортировка участков
if not fields_attribute:
    print(0)
for idx, field in enumerate(fields_attribute):
    if field[1] > 1:
        print(field[1])
        break
    if idx + 1 == len(fields_attribute):
        print(0)
