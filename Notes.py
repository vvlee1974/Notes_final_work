
import csv
import datetime
from os import path

file_base = "notes.csv"
last_id = 0
all_data = []

if not path.exists(file_base):
    with open(file_base, "w", encoding="utf-8") as _:
        pass


def read_records():
    global last_id, all_data
    with open(file_base, 'r', encoding="utf-8") as file:
        all_data = [i.strip() for i in file]
        if all_data:
            last_id = int(all_data[-1].split(';')[0])
            return all_data
        return []


def show_all():
    global all_data
    if all_data:
        with open(file_base, 'r', encoding='utf-8') as data:
            reader = csv.reader(data, delimiter=';')
            reader = sorted(reader, key=lambda x: datetime.datetime.strptime(x[3], '%Y-%m-%d == %H:%M:%S'), reverse=True)
            for row in reader:
                print(row)
    else:
        print("Empty data\n============")


def confirmation(text: str): 
    print("--------------------------")
    confirm = input(f"Подтвердите {text} записи: y - да, n - нет\n")
    print("--------------------------")
    while confirm not in ("y", "n"):
        print('Введены неверные данные')
        print("--------------------------")
        confirm = input(f"Подтвердите {text} записи: y - да, n - нет\n")
        print("--------------------------")
    return confirm


def new_records():
    global last_id, all_data
    with open(file_base, 'r+', encoding='utf-8') as data:
        for line in data:
            if line != '':
                last_id = line.split(';')[0]
        file_writer = csv.writer(data, delimiter=';', lineterminator='\r')
        title = input('Введите заголовок: ') 
        body = input('Введите текст заметки: ')  
        print("--------------------------")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d == %H:%M:%S')
        all_data = [int(last_id) + 1, title, body, timestamp]
        confirm = confirmation('добавление')
        if confirm == 'y':
            file_writer.writerow(all_data)
            print('Успешное добавление записи!')


def find_char():
    print('Выберите характеристику:')
    print('0 - id, 1 - Заголовок, 2 - Дата, q - выйти')
    char = input()
    while char not in ('0', '1', '2', 'q'):
        print('Введены неверные данные')
        print('Выберите характеристику:')
        print('0 - id, 1 - Заголовок, 2 - Дата, q - выйти')
        char = input()
    if char != 'q':
        inp = input('Введите значение\n')
        return char, inp
    else:
        return 'q', 'q'

def find_records(char, inp):
    if inp !='q':
        printed = False
        with open(file_base, 'r', encoding='utf-8') as data:
            for line in data:
                if inp == line.split(';')[int(char)]:
                    print(*line.split(';'))
                    printed = True
        if not printed:
            print("Не найдено")
        return printed


def check_id_record(text: str):
    global last_id
    decision = input(f'Вы знаете id записи которую хотите {text}? 1 - да, 2 - нет, q - выйти\n')
    print("--------------------------")
    while decision not in ('1', 'q'):
        if decision != '2':
            print('Введены неверные данные')
        else:
            find_records(*find_char())
        decision = input(f'Вы знаете id записи которую хотите {text}? 1 - да, 2 - нет, q - выйти\n')
        print("--------------------------")
    if decision == '1':
        last_id = input('Введите id, q - выйти\n')
        print("--------------------------")
        while not find_records('0', last_id) and last_id != 'q':
            last_id = input('Введите id, q - выйти\n')
            print("--------------------------")
        return last_id
    return decision


def replace_record_line(replaced_line: str):
    global last_id
    replaced = ''
    with open(file_base, 'r', encoding='utf-8') as data:
        for line in data:
            replaced += line
            if last_id == line.split(';', 2)[0]:
                replaced = replaced.replace(line, replaced_line)
    with open(file_base, 'w', encoding='utf-8') as data:
        data.write(replaced)
        print("--------------------------")


def change_records():
    global  last_id
    last_id = check_id_record('изменить')
    if last_id != 'q':
        title = input('Введите заголовок: ') 
        body = input('Введите текст заметки: ')  
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d == %H:%M:%S')
        all_data = [last_id, title, body, timestamp]
        confirm = confirmation('изменение')
        if confirm == 'y':
            print("Успешное изменение записи!")
            replace_record_line(";".join(all_data)+ ' \n')


def delete_records():
    global last_id
    last_id = check_id_record('удалить')
    if last_id != 'q':
        confirm = confirmation('удаление')
        if confirm == 'y':
            print("Успешное удаление записи!")
            replace_record_line('')


def main_menu():
    play = True
    while play:
        read_records()
        answer = input("============\nNotes:\n"
                       "============\n"
                       "1. Show all records\n"
                       "2. Add a record\n"
                       "3. Change\n"
                       "4. Delete\n"
                       "5. Exit\n"
                        "============\n"
                        )
        match answer:
            case "1":
                print("--------------------------")
                show_all()
            case "2":
                print("--------------------------")
                new_records()
            case "3":
                print("--------------------------")
                change_records()
            case "4":
                print("--------------------------")
                delete_records()
            case "5":
                play = False
            case _:
                print("--------------------------")
                print("Try again!\n")

main_menu()