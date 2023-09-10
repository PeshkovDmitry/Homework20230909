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
    '''Считывание csv-файла с заметками'''
    data = []
    fields = ["Идентификатор", "Заголовок", "Тело", "Дата создания","Дата изменения"]
    with open(filename, 'r', encoding='utf-8') as fin:
        for line in fin:
            record = dict(zip(fields, line.strip().split(';')))
            data.append(record)
    return data

def write_csv(filename: str, data: list):
    '''Запись в csv-файл заметок'''
    with open(filename, 'w', encoding='utf-8') as fout:
        for i in range(len(data)):
            s = ''
            for v in data[i].values():
                s += v + ';'
            fout.write(f'{s[:-1]}\n')

def print_result(data: list):
    '''Выводит список в виде оформленной, отсортированной по дате изменения, таблицы'''
    if len(data) == 0:
        print("Список пуст")
        return 
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
    print(s)

def find_by_title(data: list, title: str) -> list:
    '''Функция поиска указанной фразы в заголовке.
       Выдает список словарей для всех подходящих заметок'''
    res = []
    for i in data:
        if title.lower() in i["Заголовок"].lower():
            res.append(i)
    return res

def find_by_date(data: list, date: str) -> list:
    '''Функция поиска по дате создания/изменения.
       Выдает список словарей для всех подходящих заметок'''
    res = []
    for i in data:
        if date.lower() in i["Дата создания"] or date.lower() in i["Дата изменения"]:
            res.append(i)
    return res

def find_by_id(notes: list, id: str) -> dict:
    '''Функция поиска по идентификатору'''
    for note in notes:
        if id == note["Идентификатор"]:
            return note
    return None

def get_new_note(notes: list) -> dict:
    '''Функция для создания новой заметки'''
    res = {}
    ids = []
    for notes in notes:
        ids.append(int(notes["Идентификатор"]))
    res["Идентификатор"] = str(max(ids) + 1)
    res["Заголовок"] = input(f"Введите заголовок: ")
    res["Тело"] = input(f"Введите текст заметки: ")
    res["Дата создания"] = str(datetime.datetime.now())
    res["Дата изменения"] = str(datetime.datetime.now())
    return res

def delete_note(notes: list, id: str):
    '''Метод для удаления заметки'''
    note = find_by_id(notes, id)
    if note == None:
        print("Заметки с таким Id не найдено")    
        return
    notes.remove(note)

def change_note(notes: list, id: str):
    '''Метод для редактирования заметки'''
    note = find_by_id(notes, id)
    if note == None:
        print("Заметки с таким Id не найдено")
        return
    delete_note(notes, id)
    print("Введите новые данные. Если поле не требует изменения, оставьте его пустым")
    s = input(f"Введите новый заголовок: ")
    if len(s) > 0:
        note["Заголовок"] = s
    s = input(f"Введите новый текст заметки: ")
    if len(s) > 0:
        note["Тело"] = s
    note["Дата изменения"] = str(datetime.datetime.now())
    notes.append(note)
    print("Контакт успешно отредактирован")

def work_with_notes():
    notes = read_csv('notes.csv')
    choice = show_main_menu()
    while (choice != 7):
        cls()
        if choice == 1:
            print_result(notes)
        elif choice == 2:
            title = input("Введите часть заголовка для поиска: ")
            print_result(find_by_title(notes, title))
        elif choice == 3:
            date = input("Введите часть даты создания или изменения для поиска: ")
            print_result(find_by_date(notes, date))
        elif choice == 4:
            note_data = get_new_note(notes)
            notes.append(note_data)
            print("Новая заметка успешно добавлена")
            write_csv('notes.csv', notes)
        elif choice == 5:
            id = input("Введите Id редактируемой заметки заметки: ")
            change_note(notes, id)
            write_csv('notes.csv', notes)
        elif choice == 6:
            id = input("Введите Id удаляемой заметки: ")
            delete_note(notes, id)
            write_csv('notes.csv', notes)
        choice = show_main_menu()

work_with_notes()    