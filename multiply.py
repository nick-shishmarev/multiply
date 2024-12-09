import numpy as np
import os
import datetime as dt

def line_to_str(data, ex_number, errors_number):
    line = ''.join((data.replace('-', ''), str(ex_number).rjust(3,'0'), str(errors_number).rjust(3,'0')))
    return line


def str_to_line(string):
    d = f"{string[0:4]}-{string[4:6]}-{string[6:8]}"
    n = int(string[8:11])
    e = int(string[11:])
    return d, n, e


def get_from_file(f_name):
    if os.path.exists(f_name):
        with open(f_name, 'r') as file:
            f_str = file.read()
    else:
        f_str = ""
    return f_str


def put_to_file(f_name, f_str):
    with open(f_name, 'w') as file:
        file.write(f_str)


def print_history(f_name):
    history = get_from_file(f_name)
    history_lst = [history[i:i+14] for i in range(0, len(history), 14)]
    for l in history_lst:
        date, number, errors = str_to_line(l)
        print(f"{date}  {number:>10} {errors:>10}") 
    
    return 0   


def train(n):
    repeat = False
    res = []

    while True:
        n += 1
        if not repeat:
            a1 = np.random.randint(2,10)
            a2 = np.random.randint(2,10)
        a3 = input(f"{a1} * {a2} = ")
        try:
            a3 = int(a3)
        except:
            print("Ошибка")
            continue

        if a3 == 0:
            if n > 30:
                break
            else:
                print("Решено мало примеров. Надо продолжать")
                repeat = True
                continue

        if a3 == (a1 * a2):
            print("Верно")
            repeat = False
        else:
            print("Ошибка")
            repeat = True
            res.append((a1, a2, a3))

    return n, res

FILENAME = 'data.dat'
QUIT_CMD = '0'
TRAIN_CMD = '1'
HISTORY_CMD = '2'
number = 0
result = []

while True:
    action = input(f"{TRAIN_CMD}-тренировка, {HISTORY_CMD}-история, {QUIT_CMD}-выход: ")
    if action == TRAIN_CMD:
        number, result = train(number)
        print("===============================================")
        print(f"Решено {number} примеров")
        if len(result) == 0:
            print("Ошибок нет")
        else:
            print(f"Количество ошибок: ({len(result)})")
            for a in result:
                print(f"{a[0]} * {a[1]} = {a[2]}")

    elif action == HISTORY_CMD:
        print_history(FILENAME)

    elif action == QUIT_CMD:
        print("До свидания!")
        if number > 0:
            date_now = f"{dt.datetime.now():%Y%m%d}"
            errors = len(result)
            history = get_from_file(FILENAME)
            history += line_to_str(date_now, number, errors)
            put_to_file(FILENAME, history)
        break

    else:
        print("Не понял")

