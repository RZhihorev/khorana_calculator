import tkinter as tk
from tkinter import ttk, messagebox
from khorana_engine import khorana_report


def report_craft():
    global report
    cancer_site = localization_cmb.get()
    if not cancer_site:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите локализацию опухоли!'
        )
        localization_cmb.focus_set()
        return

    platelets = platelets_entry.get().strip()
    try:
        platelets = int(float(platelets.replace(',', '.')))
    except ValueError:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите количество тромбоцитов!'
        )
        platelets_entry.focus_set()
        return
    if not 0 <= platelets <= 2000:
        messagebox.showerror(
            title='Ошибка ввода',
            message=(
                'Количество тромбоцитов выходит '
                'за допустимый диапазон (0-2000)'
            )
        )
        platelets_entry.focus_set()
        return

    hemoglobin = hemoglobin_entry.get().strip()
    try:
        hemoglobin = int(float(hemoglobin.replace(',', '.')))
    except ValueError:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите концентрацию гемоглобина!'
        )
        hemoglobin_entry.focus_set()
        return
    if not 0 <= hemoglobin <= 200:
        messagebox.showerror(
            title='Ошибка ввода',
            message=(
                'Концентрация гемоглобина выходит '
                'за пределы допустимых значений (0-200)!'
            )
        )
        hemoglobin_entry.focus_set()
        return

    epoetin = epoetin_var.get()

    leukocytes = leukocytes_entry.get().strip()
    try:
        leukocytes = round(float(leukocytes.replace(',', '.')), 2)
    except ValueError:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите количество лейкоцитов'
        )
        leukocytes_entry.focus_set()
        return
    if not 0 <= leukocytes <= 200:
        messagebox.showerror(
            title='Ошибка ввода',
            message=(
                'Количтво лейкоцитов выходит '
                'за пределы допустимых значений (0-200)!'
            )
        )
        leukocytes_entry.focus_set()
        return

    try:
        height = round(float(height_entry.get()) / 100, 2)
    except ValueError:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите рост пациента!'
        )
        height_entry.focus_set()
        return
    if not 0.5 <= height <= 2.5:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Рост пациента выходит за допустимый диапазон (0.5-2.5 м)!'
        )
        height_entry.focus_set()
        return

    try:
        weight = round(float(weight_entry.get()), 2)
    except ValueError:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите вес пациента!'
        )
        weight_entry.focus_set()
        return
    if not 20 <= weight <= 300:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Вес пациента выходит за допустимый диапазон (20-300 кг)!'
        )
        weight_entry.focus_set()
        return

    bmi = round((weight / height ** 2), 2)

    report = khorana_report(
        cancer_site,
        platelets,
        hemoglobin,
        epoetin,
        leukocytes,
        bmi
        )

    report_label.config(text=report)
    root.geometry('800x340')


def copy_report():
    report_text = report_label.cget('text')

    if not report_text:
        messagebox.showwarning(
            title='Нет данных',
            message='Сначала выполните расчёт'
        )
        return

    root.clipboard_clear()
    root.clipboard_append(report_text)
    root.update()

    messagebox.showinfo(
        title='Готово',
        message='Текст отчёта скопирован в буфер обмена.'
    )


report = ''

root = tk.Tk()
root.title('Расчёт шкалы Khorana')
root.geometry('500x215')

localization_label = tk.Label(text='1. Локализация опухоли')
localization_label.place(x=10, y=5)

localization_list = [
    'Желудок, поджелудочная железа',
    'Лёгкое, лимфома, женская репродуктивная система, мочевой пузырь, яичко',
    'Прочее'
]
localization_cmb = ttk.Combobox(
    root,
    values=localization_list,
    state='readonly',
    width=73
)
localization_cmb.place(x=20, y=30)

platelets_label = tk.Label(text=(
    '2. Количество тромбоцитов до химиотерапии:'
    '                        * 10^9/л'
))
platelets_label.place(x=10, y=55)

platelets_entry = tk.Entry(width=5)
platelets_entry.place(x=300, y=55)

hemoglobin_label = tk.Label(text=(
    '3. Концентрация гемоглобина:'
    '                                                     * 10^9/л'
))
hemoglobin_label.place(x=10, y=80)

hemoglobin_entry = tk.Entry(width=5)
hemoglobin_entry.place(x=300, y=80)

epoetin_var = tk.BooleanVar(value=False)

epoetin_checkbutton = ttk.Checkbutton(
    text='Использование эритропоэтина',
    variable=epoetin_var,
)
epoetin_checkbutton.place(x=20, y=105)

leukocytes_label = tk.Label(text=(
    '4. Количество лейкоцитов до химиотерапии:'
    '                           * 10^9/л'
))
leukocytes_label.place(x=10, y=130)

leukocytes_entry = tk.Entry(width=5)
leukocytes_entry.place(x=300, y=130)

height_label = tk.Label(text='5. Рост:                    см')
height_label.place(x=10, y=155)

height_entry = tk.Entry(width=5)
height_entry.place(x=70, y=155)

weight_label = tk.Label(text='5а. Вес:                    кг')
weight_label.place(x=10, y=180)

weight_entry = tk.Entry(width=5)
weight_entry.place(x=70, y=180)

main_button = tk.Button(
    text='Запустить расчёт',
    command=report_craft,
    width=46,
    height=2
)
main_button.place(x=150, y=160)

report_label = tk.Label(text=report, justify='left', anchor='nw')
report_label.place(x=10, y=210)

disclaimer = tk.Label(
    text=(
        'ДИСКЛЕЙМЕР\n'
        ' - Программа предназначена исключительно для обучения\n'
        'и проверки расчёта по опубликованной шкале.\n'
        ' - Она не устанавливает диагноз, не формирует назначений\n'
        'и не заменяет клиническое решение врача.\n'
        ' - Пользователь обязан самостоятельно проверить\n'
        'исходные данные, актуальность источника и применимость\n'
        'результата в конкретной клинической ситуации.'
    ),
    justify='left',
    anchor='nw',
    font=('Segoe UI', 7),
    bd=1,
    relief='solid'
)
disclaimer.place(x=520, y=40)

copy_button = tk.Button(
    text='Копировать расчёт в буфер обмена',
    command=copy_report,
    width=39,
    height=2
)
copy_button.place(x=500, y=160)

copyright_label = tk.Label(
    text='© 2026 Жихорев Р. С. | Версия 1.0.0 | Сборка от 14.08.2026',
    font=('Segoe UI', 7),
    fg='gray'
)
copyright_label.place(x=280, y=320)

root.mainloop()
