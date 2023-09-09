import os

def cls():
    '''Очищение консоли'''
    os.system('cls')

def show_main_menu() -> int:
    print("\nВыберите необходимое действие:\n"
          "1. Показать все заметки\n"
          "2. Найти заметку по заголовку\n"
          "3. Найти заметку по дате создания/изменения\n"
          "4. Создать новую заметку\n"
          "5. Редактировать заметку\n"
          "6. Удалить заметку\n"
          "7. Закончить работу")
    choice = int(input("Ваш выбор: "))
    return choice

def read_csv(filename: str) -> list:
    '''Считывание csv-файла в список словарей'''
    data = []
    fields = ["Идентификатор", "Заголовок", "Тело", "Дата создания","Дата изменения"]
    with open(filename, 'r', encoding='utf-8') as fin:
        for line in fin:
            record = dict(zip(fields, line.strip().split(';')))
            data.append(record)
    return data

def write_csv(filename: str, data: list):
    '''Запись в csv-файл списка словарей'''
    with open(filename, 'w', encoding='utf-8') as fout:
        for i in range(len(data)):
            s = ''
            for v in data[i].values():
                s += v + ';'
            fout.write(f'{s[:-1]}\n')

def get_formatted_result(data: list) -> str:
    '''Выводит список в виде оформленной отсортированной по фамилии таблицы с заголовками'''
    if len(data) == 0:
        return "Список пуст"
    # Формируем список максимальных длин полей (с учетом заголовка)
    lens = []
    for key in data[0].keys():
        vals = [d[key] for d in data]
        vals.append(key)
        lens.append(len(max(vals, key = lambda x : len(x))))
    # Выводим заголовок таблицы
    lines = ["─"*i for i in lens]
    key_names = list(map(lambda x, y: f"{x:<{y}}", data[0].keys(), lens))
    s =  "┌" + "┬".join(lines) + "┐" + "\n"
    s += "│" + "│".join(key_names) + "│" + "\n"
    s += "├" + "┼".join(lines) + "┤" + "\n"
    # Сортируем содержимое таблицы по столбцу "Фамилия" по алфавиту
    data.sort(key = lambda x: x["Фамилия"].lower())
    # Выводим содержимое таблицы
    for d in data:
        vals = list(map(lambda x, y: f"{x:<{y}}", d.values(), lens))
        s += "│" + "│".join(vals) + "│"  + "\n"
    # Обрамляем таблицу снизу        
    s += "└" + "┴".join(lines) + "┘"
    return s

def print_result(data: list):
    '''Вывод таблицы с данными в консоль'''
    print(get_formatted_result(data))

def get_search_name() -> str:
    '''Функция для ввода фразы для поиска в имени или фамилии'''
    name = input("Введите часть имени или фамилии для поиска: ")
    return name

def find_by_name(data: list, name: str) -> list:
    '''Функция поиска указанной фразы в именах или фамилиях.
       Выдает список словарей для всех подходящих контактов'''
    res = []
    for i in data:
        if name.lower() in i["Фамилия"].lower() or name.lower() in i["Имя"].lower():
            res.append(i)
    return res

def get_search_number() -> str:
    '''Функция для ввода номера телефона для поиска'''
    number = input("Введите часть номера для поиска: ")
    return number

def find_by_number(data: list, number: str) -> list:
    '''Функция поиска по номеру телефона.
       Выдает список словарей для всех подходящих контактов'''
    res = []
    for i in data:
        if number in i["Телефон"]:
            res.append(i)
    return res

def get_new_user(keys: list) -> dict:
    '''Функция для создания нового контакта.
       Функции передается список запрашиваемых ключей на случай расширения функциональности справочника'''
    print("Введите данные")
    res = {}
    for key in keys:
        res[key] = input(f"{key}: ")
    return res

def add_user(data: list, user_data: dict):
    '''Метод для добавления нового контакта в базу'''
    data.append(user_data)
    print_result([user_data])
    print("Новый контакт успешно добавлен")

def delete_user(data: list, name: str):
    '''Метод для удаления контакта из справочника'''
    users_for_delete = find_by_name(data, name)
    if len(users_for_delete) == 0:
        print("По вашему запросу не найдено контактов")
        return
    print("Контакты для удаления:")
    print_result(users_for_delete)
    d = input("Удалить указанные контакты? (да/нет): ")
    if d.lower() == "да":
        for user in users_for_delete:
            data.remove(user)
            print(f"Контакт {user['Фамилия']} {user['Имя']} удален из справочника.")

def change_user(data: list, name: str):
    '''Метод для редактирования данных контакта в справочнике'''
    old_user_data = find_by_name(data, name)
    if len(old_user_data) == 0:
        print("По вашему запросу не найдено контактов")
        return
    elif len(old_user_data) > 1:
        print("По вашему запросу найдено несколько контактов, формулируйте запрос точнее")
        return
    print("Данные контакта для редактирования:")
    print_result(old_user_data)
    print("Введите новые данные. Если поле не требует изменения, оставьте его пустым")
    new_user_data = get_new_user(old_user_data[0].keys())
    for key in new_user_data.keys():
        if new_user_data[key] == "":
            new_user_data[key] = old_user_data[0][key]
    data.remove(old_user_data[0])
    data.append(new_user_data)
    print("Контакт успешно отредактирован")

def work_with_notes():
    choice = show_main_menu()
    notes = read_csv('notes.csv')
    while (choice != 7):
        cls()
        if choice == 1:
            print_result(notes)
        elif choice == 2:
            name = get_search_name()
            print_result(find_by_name(notes, name))
        elif choice == 3:
            number = get_search_number()
            print_result(find_by_number(notes, number))
        elif choice == 4:
            user_data = get_new_user(notes[0].keys())
            add_user(notes, user_data)
            write_csv('notes.csv', notes)
        elif choice == 5:
            name = get_search_name()
            change_user(notes, name)
            write_csv('notes.csv', notes)
        elif choice == 6:
            name = get_search_name()
            delete_user(notes, name)
            write_csv('notes.csv', notes)
        choice = show_main_menu()

work_with_notes()    