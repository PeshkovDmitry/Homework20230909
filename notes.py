import os
import datetime

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
    '''Выводит список в виде оформленной, отсортированной по дате изменения, таблицы'''
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
    data.sort(key = lambda x: x["Дата изменения"].lower())
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

def get_search_title() -> str:
    '''Функция для ввода фразы для поиска в заголовке'''
    title = input("Введите часть заголовка для поиска: ")
    return title

def find_by_title(data: list, title: str) -> list:
    '''Функция поиска указанной фразы в заголовке.
       Выдает список словарей для всех подходящих заметок'''
    res = []
    for i in data:
        if title.lower() in i["Заголовок"].lower():
            res.append(i)
    return res

def get_search_date() -> str:
    '''Функция для ввода даты для поиска'''
    date = input("Введите часть даты создания или изменения для поиска: ")
    return date

def find_by_date(data: list, date: str) -> list:
    '''Функция поиска по дате создания/изменения.
       Выдает список словарей для всех подходящих заметок'''
    res = []
    for i in data:
        if date.lower in i["Дата создания"] or date.lower in i["Дата изменения"]:
            res.append(i)
    return res

def get_new_note(data: list) -> dict:
    '''Функция для создания новой заметки'''
    res = {}
    ids = []
    for i in data:
        ids.append(int(i["Идентификатор"]))
    res["Идентификатор"] = str(max(ids) + 1)
    res["Заголовок"] = input(f"Введите заголовок: ")
    res["Тело"] = input(f"Введите текст заметки: ")
    res["Дата создания"] = str(datetime.datetime.now())
    res["Дата изменения"] = str(datetime.datetime.now())
    return res

def add_note(data: list, note: dict):
    '''Метод для добавления новой заметки в базу'''
    data.append(note)
    print_result([note])
    print("Новая заметка успешно добавлена")

def delete_note(data: list, name: str):
    '''Метод для удаления контакта из справочника'''
    users_for_delete = find_by_title(data, name)
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
    old_user_data = find_by_title(data, name)
    if len(old_user_data) == 0:
        print("По вашему запросу не найдено контактов")
        return
    elif len(old_user_data) > 1:
        print("По вашему запросу найдено несколько контактов, формулируйте запрос точнее")
        return
    print("Данные контакта для редактирования:")
    print_result(old_user_data)
    print("Введите новые данные. Если поле не требует изменения, оставьте его пустым")
    new_user_data = get_new_note(old_user_data[0].keys())
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
            title = get_search_title()
            print_result(find_by_title(notes, title))
        elif choice == 3:
            date = get_search_date()
            print_result(find_by_date(notes, date))
        elif choice == 4:
            note_data = get_new_note(notes)
            add_note(notes, note_data)
            write_csv('notes.csv', notes)
        elif choice == 5:
            title = get_search_title()
            change_user(notes, title)
            write_csv('notes.csv', notes)
        elif choice == 6:
            title = get_search_title()
            delete_note(notes, title)
            write_csv('notes.csv', notes)
        choice = show_main_menu()

work_with_notes()    