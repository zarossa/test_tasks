def str_to_int(stack):
    # Превращает символы в списке в числа
    new_stack = []
    for num in stack:
        if num == '-':
            break
        new_stack.append(int(num))
    return new_stack


# 1. Подготовка и считывание данных
len_stack1, len_stack2, salaries = map(lambda x: int(x), input().split())  # считывание длины 1, 2 стопок и зарплаты
stack1 = []  # массив первой стопки зарплат
stack2 = []  # массив второй стопки зарплат
for _ in range(max(len_stack1, len_stack2)):  # считывание и заполнение данных зарплат
    a, b = input().split()
    stack1.append(a)
    stack2.append(b)
stack1 = str_to_int(stack1)  # конвертация первой стопки в числовые значения
stack2 = str_to_int(stack2)  # конвертация второй стопки в числовые значения

# 2. Анализ

# 3. Вывод результата
