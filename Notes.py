# Создать телефонный справочник с возможностью импорта и
# экспорта данных в формате .txt. Фамилия, имя, отчество,
# номер телефона - данные, которые должны находиться в файле.

# Программа должна выводить данные
# Программа должна сохранять данные в текстовом файле
# Пользователь может ввести одну из характеристик для поиска 
# определенной записи(Например имя или фамилию человека)
# Использование функций. Ваша программа не должна быть линейной

# Дополнить телефонный справочник возможностью изменения и
# удаления данных. Пользователь также может ввести имя или фамилию,
# и Вы должны реализовать функционал для изменения и удаления данных


# r - только чтение файла
# a - дозапись в файл
# w - перезапись файла

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
    if all_data:
        print(*all_data, sep="\r\n")
    else:
        print("Empty data\n============\n")


def confirmation(text: str): 
    confirm = input(f"Подтвердите {text} записи: y - да, n - нет\n")
    while confirm not in ("y", "n"):
        print('Введены неверные данные')
        confirm = input(f"Подтвердите {text} записи: y - да, n - нет\n")
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
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        all_data = [int(last_id) + 1, title, body, timestamp]
        confirm = confirmation('добавление')
        if confirm == 'y':
            file_writer.writerow(all_data)


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
    while decision not in ('1', 'q'):
        if decision != '2':
            print('Введены неверные данные')
        else:
            find_records(*find_char())
        decision = input(f'Вы знаете id записи которую хотите {text}? 1 - да, 2 - нет, q - выйти\n')
    if decision == '1':
        last_id = input('Введите id, q - выйти\n')
        while not find_records('0', last_id) and last_id != 'q':
            last_id = input('Введите id, q - выйти\n')
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


def change_records():
    global  last_id
    last_id = check_id_record('изменить')
    if last_id != 'q':
        title = input('Введите заголовок: ') 
        body = input('Введите текст заметки: ')  
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        all_data = [last_id, title, body, timestamp]
        confirm = confirmation('изменение')
        if confirm == 'y':
            replace_record_line(";".join(all_data)+ ' \n')


def delete_records():
    global last_id
    last_id = check_id_record('удалить')
    if last_id != 'q':
        confirm = confirmation('удаление')
        if confirm == 'y':
            replace_record_line('')


def main_menu():
    play = True
    while play:
        read_records()
        answer = input("============\nNotes:\n"
                       "============\n"
                       "1. Show all records\n"
                       "2. Add a record\n"
                       "3. Search a record\n"
                       "4. Change\n"
                       "5. Delete\n"
                       "6. Exp/Imp\n"
                       "7. Exit\n"
                        "============\n"
                        )
        match answer:
            case "1":
                show_all()
            case "2":
                new_records()
            case "3":
                find_records(*find_char())
            case "4":
                change_records()
            case "5":
                 delete_records()
            case "6":
                pass
            case "7":
                play = False
            case _:
                print("Try again!\n")


main_menu()