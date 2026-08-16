import tkinter as tk
from tkinter import ttk, messagebox
from khorana_engine import khorana_report
from constants import APP_VERSION, BUILD_DATE


def read_float(entry, field_name, min_value, max_value, *, divisor=1.0):
    raw = entry.get().strip().replace(',', '.')

    try:
        value = float(raw) / divisor
    except ValueError:
        messagebox.showerror(
            'Ошибка ввода',
            f'Введите корректное значение: {field_name}'
        )
        entry.focus_set()
        return None

    if not min_value <= value <= max_value:
        messagebox.showerror(
            'Ошибка ввода',
            f'{field_name}, допустимый диапазон: {min_value}-{max_value}'
        )
        entry.focus_set()
        return None

    return value


def report_craft():
    cancer_site = localization_cmb.get()
    if not cancer_site:
        messagebox.showerror(
            title='Ошибка ввода',
            message='Введите локализацию опухоли!'
        )
        localization_cmb.focus_set()
        return

    platelets = read_float(platelets_entry, 'Тромбоциты, х 10^9/кл', 0, 2000)
    if platelets is None:
        return

    hemoglobin = read_float(hemoglobin_entry, 'Гемоглобин, г/л', 0, 300)
    if hemoglobin is None:
        return

    epoetin = epoetin_var.get()

    leukocytes = read_float(leukocytes_entry, 'Лейкоциты, х 10^9/кл', 0, 200)
    if leukocytes is None:
        return

    height = read_float(height_entry, 'Рост, см', 50, 250)
    if height is None:
        return

    weight = read_float(weight_entry, 'Вес, кг', 20, 300)
    if weight is None:
        return

    bmi = weight / (height / 100) ** 2

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
    '                                                     * г/л'
))
hemoglobin_label.place(x=10, y=80)

hemoglobin_entry = tk.Entry(width=5)
hemoglobin_entry.place(x=300, y=80)

epoetin_var = tk.BooleanVar(value=False)

epoetin_checkbutton = ttk.Checkbutton(
    text='Применение эритропоэз-стимулирующего препарата (ЭСП)',
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

report_label = tk.Label(text='', justify='left', anchor='nw')
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
    text=(
        '© 2026 Жихорев Р. С. '
        f'| Версия {APP_VERSION} | Сборка от {BUILD_DATE}'
        ),
    font=('Segoe UI', 7),
    fg='gray'
)
copyright_label.place(x=520, y=320)

source_label = tk.Label(
    root,
    text=(
        "Источник шкалы: Khorana et al., Blood, 2008; 111(10):4902–4907."
    ),
    justify="left",
    anchor="w",
    font=("Segoe UI", 7),
    fg="gray",
)
source_label.place(x=10, y=320)

root.mainloop()
