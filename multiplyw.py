from tkinter import *
from tkinter.scrolledtext import ScrolledText
import numpy as np
import datetime as dt
import os

FON1 = '#606060'                    # Фон окна
FON2 = '#808080'                    # Фон элементов
TEXT1 = '#ffffff'                   # Цвет текста
TEXT2 = '#ff0000'                   # Цвет выделенного текста
TEXT3 = '#aaaaaa'
FONT = ('Arial', '14', 'bold')      # Фонт
FONT_TIME = ('Arial', '12')         # Фонт даты и времени
FILENAME='data.dat'                 # Имя файла с историей
NUMBER_OF_TASKS = 40                # Минимальное число примеров для решения

# Класс для пары случайных сомножителей
class Randpair:
    def __init__(self):
        self.x1 = np.random.randint(2,10)
        self.x2 = np.random.randint(2,10)
        self.num =0

    def new_values(self):
        self.x1 = np.random.randint(2,10)
        self.x2 = np.random.randint(2,10)
        self.num += 1


# Преобразование даты, количества примеров и количества ошибок в строку для файла истории
def line_to_str(data, ex_number, errors_number):
    line = ''.join((data.replace('-', ''), str(ex_number).rjust(3,'0'), str(errors_number).rjust(3,'0')))
    return line


# Обратное преобразование строки файла истории в дату, количество примеров и количество ошибок
def str_to_line(string):
    d = f"{string[0:4]}-{string[4:6]}-{string[6:8]}"
    n = int(string[8:11])
    e = int(string[11:])
    return d, n, e


# Чтение истории из файла
def get_from_file(f_name):
    if os.path.exists(f_name):
        with open(f_name, 'r') as file:
            f_str = file.read()
    else:
        f_str = ""
    return f_str


# Запись истории в файл
def put_to_file(f_name, f_str):
    with open(f_name, 'w') as file:
        file.write(f_str)


# Формирование текста для вывода истории на экран
def output_window(data, titles):
    output_txt = ''.join(str(z).rjust(20, " ") for z in titles) + "\n"
    for line in data:
        data_, num_, err_ = str_to_line(line)
        if num_ > 0:
            output_txt = output_txt + f'{data_:>20}{num_:20d}{err_:20d}\n'
            # output_txt = output_txt + ''.join(str(z).rjust(20, " ") for z in out_) + "\n"

    return output_txt


# Вывод на экран истории в дополнительное окно
def output_results(*args):
    def dismiss(w):
        w.destroy()

    window = Toplevel(bg = FON1, pady=10, padx=10)
    window.title("Таблица результатов")
    window.geometry("600x400+300+300")
    window.resizable(False, False)
    window.overrideredirect(True)

    out_lbl = Label(
        window,
        borderwidth=0,
        relief=SUNKEN,
        text="Прошлые результаты",
        pady=10,
        width=40,
        bg=FON1,
        fg=TEXT1,
        font=FONT,
    )

    out_txt = ScrolledText(window, width=70, height=16, pady=10)

    scroll = Scrollbar(command=out_txt.yview)
    scroll.pack(side=LEFT, fill=Y)

    close_button = Button(window, text="Закрыть окно", command=lambda: dismiss(window), pady=10, padx=20)

    out_lbl.pack()
    out_txt.pack()
    close_button.pack(anchor="se", expand=1)

    titles_str = ('Дата', 'Решено', 'Ошибок')
    history = get_from_file(FILENAME)
    history_lst = [history[i:i+14] for i in range(0, len(history), 14)]
    print(history_lst)
    out_txt.insert("1.0", output_window(history_lst, titles_str))
    out_txt.configure(state="disabled")


# Обработка ввода ответа на пример
def rez(*args):
    x3 = base_ent.get()
    a = 0
    x1 = my_pair.x1
    x2 = my_pair.x2
    try:
        a = int(x3)
    except:
        method_lbl.configure(text="Неверный ввод")
        return

    if a == x1*x2:
        result.append((x1, x2, a))
        method_lbl.configure(text=f"Верно {a}", fg=TEXT1)
        my_pair.new_values()
        x1 = my_pair.x1
        x2 = my_pair.x2
        message = f"{x1} * {x2} = "
        base_lbl.configure(text=f"{message:>10}")
    else:
        method_lbl.configure(text=f"Неверно: {a}", fg=TEXT2)
        errors.append((x1, x2, a))

    method_lbl3.configure(text=f"{dt.datetime.now():%d-%m-%Y %H:%M}")
    base_ent.delete(0,3)
    return


# Обработка кнопки стоп
def stop(*args):
    if my_pair.num < NUMBER_OF_TASKS:
        method_lbl.configure(text=f"Мало примеров: {my_pair.num}. Продолжайте!", fg="#ff0000")
        return

    base_lbl.destroy()
    base_ent.destroy()
    stop_btn.destroy()
    frame.bind_all("<Return>", exit_f)
    method_lbl.configure(text=f"Решено: {my_pair.num} ошибок: {len(errors)}", fg="#ffff00")

    method_lbl2.place(x=10, y=60)
    # Время работы с программой
    dk = dt.datetime.now()
    dp = dk - dn
    hrs, minutes, scs = str(dp).split(':', 2)
    scs = scs[:2]
    hrs = int(hrs)
    minutes = int(minutes)
    scs = int(scs)
    method_lbl2.configure(text=f"Время работы: {minutes} минут {scs} секунд", fg="#ffffff")
    exit_btn.place(x=350, y=110)

    return


def exit_f(*args):
    main.quit()
    return


result = []
errors = []

# string = get_from_file(FILENAME)
# history_lst = [string[i:i+14] for i in range(0, len(string), 14)]

my_pair = Randpair()
message = f"{my_pair.x1} * {my_pair.x2} = "
dn = dt.datetime.now()
date_now = f"{dn:%Y-%m-%d}"

# Основное окно приложения
main = Tk()
main.title("Умножение")
main.geometry("500x240+300+300")
main.resizable(False, False)
main.overrideredirect(True)

# Основной фрейм
frame = Frame(
    master=main,
    padx=40,
    pady=20,
    relief=RAISED,
    borderwidth=5,
    bg=FON1,
    width=500,
    height=200,
)
frame_title = Frame(
    master=main,
    padx=0,
    pady=0,
    relief=RAISED,
    borderwidth=5,
    bg=FON1,
    width=500,
    height=40,
)

# Титул окна
method_tit = Label(
    master=frame_title,
    # frame,
    # borderwidth=5,
    # relief=SUNKEN,
    text="Тренажер таблица умножения",
    width=40,
    bg=FON1,
    fg=TEXT1,
    font=FONT,
    padx=0,
    pady=0,
)


method_lbl = Label(
    frame,
    borderwidth=5,
    relief=SUNKEN,
    text="Введите результат умножения",
    width=30,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
)


method_lbl2 = Label(
    frame,
    borderwidth=5,
    relief=SUNKEN,
    text="",
    width=30,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
)

# Текущая дата и время
method_lbl3 = Label(
    frame,
    # borderwidth=5,
    text=f"{dt.datetime.now():%Y-%m-%d %H:%M}",
    width=14,
    bg=FON1,
    fg=TEXT3,
    font=FONT_TIME,
    padx=0,
)

# Поле для сомножителей
base_lbl = Label(
    frame,
    borderwidth=5,
    relief=SUNKEN,
    text=f"{message:>10}",
    width=10,
    justify=RIGHT,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
)

# Поле для ввода ответа
base_ent = Entry(
    frame,
    borderwidth=5,
    relief=SUNKEN,
    width=10,
    justify=LEFT,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
)

# Кнопка СТОП
stop_btn = Button(
    frame,
    text="Стоп",
    command=stop,
    borderwidth=5,
    relief=RAISED,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
    width=6,
    height=1,
)

# Кнопка вывода истории
show_btn = Button(
    frame,
    text="Результаты",
    command=output_results,
    borderwidth=5,
    relief=RAISED,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
    width=10,
    height=1,
)

# Кнопка завершения работы
exit_btn = Button(
    frame,
    text="Выход",
    command=exit_f,
    borderwidth=5,
    relief=RAISED,
    bg=FON2,
    fg=TEXT1,
    font=FONT,
    width=6,
    height=1,
)

frame_title.grid_propagate(False)
frame_title.pack(expand=True)

frame.grid_propagate(False)
frame.pack(expand=True)

method_tit.grid_propagate(False)
# method_tit.pack(anchor='center', expand=True)
# method_tit.grid(row=1, column=0, sticky="nsew")
method_tit.grid()
method_lbl.grid_propagate(False)
method_lbl.place(x=10,y=10)
method_lbl3.grid_propagate(False)
method_lbl3.place(x=10,y=120)
base_lbl.grid_propagate(False)
base_lbl.place(x=50, y=60)
base_ent.grid_propagate(False)
base_ent.place(x=200, y=60)
stop_btn.place(x=350, y=110)
show_btn.place(x=200, y=110)
frame.bind_all("<Return>", rez)
frame.bind_all("<Escape>", stop)
frame.bind_all("<Control-q>", exit_f)       # Немедленное завершение работы
base_ent.focus()

main.mainloop()

# Сохранение результатов работы в историю
if my_pair.num > 0:
    history = get_from_file(FILENAME)
    history += line_to_str(date_now, my_pair.num, len(errors))
    put_to_file(FILENAME, history)