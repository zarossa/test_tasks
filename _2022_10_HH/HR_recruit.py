def str_to_int(stack):
    # Превращает символы в списке в числа
    new_stack = []
    for num in stack:
        if num == '-':
            break
        new_stack.append(int(num))
    return new_stack


def find_max(stack_1, stack_2, salary):
    # Возвращает максимальную стопку подходящих резюме
    # 1. Собрать максимальную сумму из первой стопки
    stack_confirm = []  # рассматриваемая стопка (плавно скользит между первой и второй стопками)
    for num in stack_1:  # наполнение стопки из первой папки
        stack_confirm.append(num)
        if sum(stack_confirm) > salary:
            # выйти, если превысили значение зарплаты
            del stack_confirm[-1]
            break
    resume_number_max = len(stack_confirm)  # максимальное число резюме
    stack_confirm.insert(0, 0)  # добавление символа-разделителя

    # 2. Добавить новый элемент из второй стопки
    for num in stack_2:
        stack_confirm.insert(0, num)
        while sum(stack_confirm) > salary:
            if stack_confirm[-1] == 0:
                # выйти, если выкинули всю первую стопку
                break
            del stack_confirm[-1]
        if sum(stack_confirm) <= salary:
            resume_number_max = max(resume_number_max, len(stack_confirm) - 1)

    # 3. Вернуть максимальное значение
    return resume_number_max


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

# testing data
resume_num = find_max(stack1, stack2, salaries)  # поиск наибольшего количества резюме

# 3. Вывод результата
print(resume_num)
