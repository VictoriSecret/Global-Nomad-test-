import sqlite3
import re
from tkinter import *
from tkinter.messagebox import showerror, showwarning, showinfo
from ttkthemes import themed_style
from tkinter import ttk, filedialog, messagebox
from tkcalendar import Calendar
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

current_user_uid = None
pdfmetrics.registerFont(TTFont('Montserrat-Regular', 'fonts/Montserrat-Regular.ttf'))

def connect_db():
    return sqlite3.connect("global_nomad.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE CHECK (email LIKE '%_@_%._%'),
        password TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS direction (
        direction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_direction TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS packages (
        packages_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        direction_id INTEGER,
        date DATE NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(direction_id) REFERENCES direction(direction_id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS administrator (
            id_admin INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            admin_login	TEXT NOT NULL UNIQUE,
            admin_password TEXT NOT NULL UNIQUE,
            admin_name TEXT NOT NULL,
            admin_last_name	TEXT NOT NULL,
        )''')
    conn.commit()
    conn.close()
def choice_role_user():
    choice_window.destroy()
    #  функции для удаления текста в полях ввода при нажатии
    def on_entry_click1(event):
        if entry_login.get() == "Email пользователя":
            entry_login.delete(0, END)
            entry_login.config(foreground="black")

    def on_entry_click2(event):
        if entry_password.get() == "Пароль":
            entry_password.delete(0, END)
            entry_password.config(foreground="black")

    # окно регистрации
    def registration():
        def on_entry_click01(event):
            if entry_login_reg.get() == "Email пользователя":
                entry_login_reg.delete(0, END)
                entry_login_reg.config(foreground="black")

        def on_entry_click02(event):
            if entry_password_reg.get() == "Пароль":
                entry_password_reg.delete(0, END)
                entry_password_reg.config(foreground="black")


        # Функция для проверки формата электронной почты
        def is_valid_email(email):
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(email_regex, email) is not None

        # Функция для проверки пароля
        def is_valid_password(password):
            # Проверяем, что пароль соответствует критериям
            password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
            return re.match(password_regex, password) is not None

        # функция регистрации (в базу данных)
        def register_user():
            email = entry_login_reg.get()
            password = entry_password_reg.get()

            # Проверка формата электронной почты
            if not is_valid_email(email):
                messagebox.showerror("Ошибка", "Введите корректный адрес электронной почты.")
                return

                # Проверка формата пароля
            if not is_valid_password(password):
                messagebox.showerror("Ошибка",
                                     "Пароль должен содержать минимум 8 символов, "
                                     "включая заглавные и строчные буквы, цифры и специальные символы.")
                return
            conn = connect_db()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                               (email, password))
                conn.commit()
                messagebox.showinfo("Регистрация", "Пользователь успешно зарегистрирован!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Пользователь с таким email же существует.")
            finally:
                conn.close()

        window_registration = Toplevel()
        window_registration.title("Global Nomad регистрация")
        window_registration.geometry("952x682+70+60")
        window_registration.resizable(False, False)
        window_registration.config(background="#FAFAFA")

        title_lb_reg = ttk.Label(window_registration, text='Global Nomad', background="#FAFAFA", font=('Montserrat Alternates', 64))
        title_lb_reg.pack(anchor='center', pady=140)
        label1_reg = ttk.Label(window_registration, text="Зарегистрируйтесь для входа",
                               background="#FAFAFA", font=("Montserrat",12), foreground="#625D5D")
        label1_reg.place(x=350, y=250)

        # стиль для Entry
        style_reg = themed_style.ThemedStyle(window_registration)
        style_reg.theme_use("clam")
        style_reg.configure("TEntry", padding=10)
        # Ввод логина
        entry_login_reg = ttk.Entry(window_registration, width=30)
        entry_login_reg.place(x=290, y=330)
        entry_login_reg.insert(0, "Email пользователя")
        entry_login_reg.config(font=("Montserrat", 12), foreground="#625D5D")
        entry_login_reg.bind("<FocusIn>", on_entry_click01)
        # Ввод пароля
        entry_password_reg = ttk.Entry(window_registration, width=30)
        entry_password_reg.place(x=290, y=400)
        entry_password_reg.insert(0, "Пароль")
        entry_password_reg.config(font=("Montserrat", 12), foreground="#625D5D")
        entry_password_reg.bind("<FocusIn>", on_entry_click02)
        # кнопка для регистрации
        btn_reg = Button(window_registration, text="Регистрация", bg='#162013', width=20, fg="#FFFFFF", font=("Montserrat", 12), command=register_user)
        btn_reg.place(x=360, y=500, height=45)

        label2_registration = ttk.Label(window_registration, text="Регистрируясь, вы принимаете наши Условия", background="#FAFAFA",
                                         font=("Montserrat", 12), foreground="#625D5D")
        label2_registration.place(x=280, y=598)

        label3_registration = ttk.Label(window_registration, text="и Политику использования данных", background="#FAFAFA",
                                         font=("Montserrat", 12), foreground="#625D5D")
        label3_registration.place(x=318, y=625)


    # окно выбора дат и направлений
    def travel_packages():
        login = entry_login.get()
        password = entry_password.get()
        if login and password and len(login) >= 5 and 8 <= len(password) <= 20:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                               (login, password))
                user = cursor.fetchone()
                conn.close()

                if user:
                    showinfo(title='Вход', message='Успешный вход')
                    global current_user_uid
                    current_user_uid = user[0]
                    main_root.destroy()
                    # окно профиля
                    def profile():
                        # функция для экспорта данных пользователя в PDF
                        def export_to_pdf():
                            conn = connect_db()
                            cursor = conn.cursor()

                            pdfmetrics.registerFont(TTFont('Montserrat-Regular', 'fonts/Montserrat-Regular.ttf'))

                            # Получение данных пользователя
                            cursor.execute("SELECT email FROM users WHERE user_id=?", (current_user_uid,))
                            user_data = cursor.fetchone()

                            # Получение выбранных путевок
                            cursor.execute("SELECT date, direction_id, id_payment_method FROM packages WHERE user_id=?",
                                           (current_user_uid,))
                            packages_list = cursor.fetchall()

                            # Проверка что данные пользователя получены
                            if user_data:
                                user_info = user_data[0]
                            else:
                                messagebox.showerror("Ошибка", "Не удалось получить данные пользователя.")
                                conn.close()  # Закрываем соединение перед выходом
                                return

                            # диалоговое окно для выбора места сохранения файла
                            pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                                        filetypes=[("PDF files", "*.pdf"),
                                                                                   ("All files", "*.*")],
                                                                        title="Сохранить PDF как")
                            if not pdf_filename:  # Если пользователь отменил выбор
                                conn.close()
                                return

                            # Создание PDF документа
                            pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
                            styles = getSampleStyleSheet()
                            styles['Title'].fontName = 'Montserrat-Regular'
                            styles['Heading2'].fontName = 'Montserrat-Regular'
                            styles['BodyText'].fontName = 'Montserrat-Regular'

                            elements = []

                            # Заголовок
                            elements.append(Paragraph(f"Данные пользователя: {user_info}", styles['Title']))
                            elements.append(Spacer(1, 12))

                            # Добавление путевок
                            elements.append(Paragraph("Ваши выбранные путевки:", styles['Heading2']))
                            elements.append(Spacer(1, 12))

                            if packages_list:
                                for package in packages_list:
                                    date, direction_id, id_payment_method = package

                                    # Получение названия направления
                                    cursor.execute("SELECT name_direction FROM direction WHERE direction_id=?",
                                                   (direction_id,))
                                    direction_name = cursor.fetchone()
                                    direction_name = direction_name[0] if direction_name else "Неизвестное направление"

                                    # Получение названия способа оплаты
                                    cursor.execute(
                                        "SELECT name_payment_method FROM payment_methods WHERE id_payment_method=?",
                                        (id_payment_method,))
                                    payment_method_name = cursor.fetchone()
                                    payment_method_name = payment_method_name[
                                        0] if payment_method_name else "Неизвестный способ оплаты"

                                    elements.append(
                                        Paragraph(
                                            f"Дата: {date}, Направление: {direction_name}, Способ оплаты: {payment_method_name}",
                                            styles['BodyText']))
                                    elements.append(Spacer(1, 12))
                            else:
                                elements.append(Paragraph("Путевок нет", styles['BodyText']))

                            # Сохранение PDF
                            pdf.build(elements)
                            messagebox.showinfo("Экспорт в PDF",
                                                f"Данные пользователя успешно экспортированы в {pdf_filename}")

                            # Закрытие соединения с базой данных после завершения всех операций
                            conn.close()

                        window_profile = Toplevel()
                        window_profile.title("Global Nomad профиль пользователя")
                        window_profile.geometry("952x682+70+60")
                        window_profile.resizable(False, False)
                        window_profile.config(background="#FAFAFA")

                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("SELECT email FROM users WHERE user_id=?", (current_user_uid,))
                        user_data = cursor.fetchone()
                        conn.close()
                        if user_data:
                            global_label_profile = ttk.Label(window_profile, text="Global Nomad",
                                                             font=('Montserrat Alternates', 12), background="#FAFAFA")
                            global_label_profile.pack(anchor="nw", pady=20, padx=15)

                            greeting_lb = ttk.Label(window_profile, text="Здравствуй, глобальный кочевник!",
                                                    font=("Montserrat", 25), background="#FAFAFA")
                            greeting_lb.pack(anchor="nw", pady=80, padx=15)

                            user_packages_lb = ttk.Label(window_profile, text="Ваши выбранные путевки",
                                                         background="#FAFAFA", font=("Montserrat", 12),
                                                         foreground="#625D5D")
                            user_packages_lb.place(x=15, y=200)

                            # Отображение путевок пользователя
                            packages_listbox = Listbox(window_profile, width=80, height=10, font=("Montserrat", 12))
                            packages_listbox.place(y=240, x=15)

                            # Получфем данных о путевках пользователя
                            conn = connect_db()
                            cursor = conn.cursor()
                            cursor.execute("SELECT date, direction_id, id_payment_method FROM packages WHERE user_id=?",
                                           (current_user_uid,))
                            packages_list = cursor.fetchall()
                            conn.close()

                            if packages_list:
                                for package in packages_list:
                                    date, direction_id, id_payment_method = package

                                    conn = connect_db()
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT name_direction FROM direction WHERE direction_id=?",
                                                   (direction_id,))
                                    direction_name = cursor.fetchone()
                                    cursor.execute(
                                        "SELECT name_payment_method FROM payment_methods WHERE id_payment_method=?",
                                        (id_payment_method,))
                                    payment_method_name = cursor.fetchone()
                                    conn.close()
                                    direction_name = direction_name[0] if direction_name else "Неизвестное направление"
                                    payment_method_name = payment_method_name[0] if payment_method_name else "Неизвестный метод оплаты"
                                    packages_listbox.insert(END, f"Дата: {date}, Направление: {direction_name}, Способ оплаты: {payment_method_name}")
                            else:
                                packages_listbox.insert(END, "Путевок нет")

                            # Кнопка для экспорта данных в PDF
                            export_pdf_btn = Button(window_profile, text="Экспорт билета в PDF", command=export_to_pdf,
                                                    bg='#162013',
                                                    fg="#FFFFFF", font=("Montserrat", 12))
                            export_pdf_btn.place(x=15, y=600)

                    def update_description(event):
                        selected_direction_name = travel_packages_choice_combobox.get()
                        if selected_direction_name:
                            conn = connect_db()
                            cursor = conn.cursor()
                            cursor.execute("SELECT description FROM direction WHERE name_direction=?",
                                           (selected_direction_name,))
                            description = cursor.fetchone()
                            conn.close()
                            if description:
                                description_label.config(text=description[0])  # Обновляем текст описания
                            else:
                                description_label.config(text="Описание не найдено.")

                    # добавление данных о путевках и датах в базу данных
                    def add_travel_data():
                        selected_direction_name = travel_packages_choice_combobox.get()
                        selected_date = calendar.get_date()
                        selected_payment_method_name = payment_method_combobox.get()

                        if selected_date and selected_direction_name and selected_payment_method_name:
                            try:

                                conn = connect_db()
                                cursor = conn.cursor()
                                cursor.execute("SELECT direction_id FROM direction WHERE name_direction=?",
                                               (selected_direction_name,))
                                direction_id_row = cursor.fetchone()
                                cursor.execute("SELECT id_payment_method FROM payment_methods WHERE name_payment_method=?",
                                               (selected_payment_method_name,))
                                payment_method_row = cursor.fetchone()  # Получите идентификатор метода оплаты
                                conn.close()

                                if direction_id_row and payment_method_row:
                                    direction_id = direction_id_row[0]
                                    payment_method_id = payment_method_row[0]

                                    conn = connect_db()
                                    cursor = conn.cursor()
                                    cursor.execute(
                                        "INSERT INTO packages (user_id, direction_id, date, id_payment_method) VALUES (?, ?, ?, ?)",
                                        (current_user_uid, direction_id, selected_date, payment_method_id))
                                    conn.commit()
                                    conn.close()
                                    showinfo(title="Путевки", message="Путевка выбрана")
                                else:
                                    showerror(title="Ошибка", message="Направление не найдено в базе данных.")
                            except Exception as e:
                                showwarning(title="Предупреждение", message=f"Ошибка при оформлении путевки: {e}")
                        else:
                            showerror(title="Ошибка", message="Все данные должны быть выбраны")

                    window_travels = Tk()
                    window_travels.title("Global Nomad туристические путевки")
                    window_travels.geometry("952x682+70+60")
                    window_travels.resizable(False, False)
                    window_travels.config(background="#FAFAFA")

                    # кнопка для открытия окна профиля
                    profile_btn = Button(window_travels, text="Профиль", width=15, fg="#000000", font=("Montserrat", 12),
                                         bg="#FAFAFA",  command=profile)
                    profile_btn.place(x=800, y=17)
                    profile_btn['borderwidth'] = 0

                    global_label = ttk.Label(window_travels, text="Global Nomad", font=('Montserrat Alternates', 12),
                                             background="#FAFAFA")
                    global_label.pack(anchor="nw", pady=20, padx=15)

                    travel_lb1 = ttk.Label(window_travels, text="Выбирайте путевки", font=("Montserrat", 35),
                                           background="#FAFAFA")
                    travel_lb1.pack(anchor="nw", pady=80, padx=15)
                    travel_lb2 = ttk.Label(window_travels, text="для души!", font=("Montserrat", 35), background="#FAFAFA")
                    travel_lb2.place(x=15, y=200)

                    travel_lb3 = ttk.Label(window_travels, text="у нас собраны лучшие направления", background="#FAFAFA",
                                           font=("Montserrat", 12), foreground="#625D5D")
                    travel_lb3.place(x=15, y=275)
                    travel_lb4 = ttk.Label(window_travels, text="и удобные даты, чтобы каждый мог понять,",
                                           background="#FAFAFA", font=("Montserrat", 12), foreground="#625D5D")
                    travel_lb4.place(x=15, y=300)
                    travel_lb5 = ttk.Label(window_travels, text="что путешествию есть время - всегда.",
                                           background="#FAFAFA", font=("Montserrat", 12), foreground="#625D5D")
                    travel_lb5.place(x=15, y=325)

                    # Добавление Label для отображения описания
                    description_label = ttk.Label(window_travels, text="", background="#FAFAFA",
                                                  font=("Montserrat", 12), wraplength=360)
                    description_label.place(x=15, y=380)

                    # выбор направлений
                    travel_packages_choice = ttk.Label(window_travels, text="Направления", background="#FAFAFA",
                                                       font=("Montserrat", 12))
                    travel_packages_choice.place(x=800, y=170)

                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("SELECT name_direction FROM direction")
                    directions = cursor.fetchall()
                    conn.close()

                    # из списка кортежей в простой список
                    packages = [direction[0] for direction in directions]

                    travel_packages_choice_combobox = ttk.Combobox(window_travels, values=packages,
                                                                   state="readonly",
                                                                   justify="left", background="#fafafa", height=40)
                    travel_packages_choice_combobox.place(x=785, y=200)

                    # Привязка события выбора направления к функции обновления описания
                    travel_packages_choice_combobox.bind("<<ComboboxSelected>>", update_description)

                    # выбор дат
                    travel_packages_date = ttk.Label(window_travels, text="Даты", background="#FAFAFA",
                                                     font=("Montserrat", 12))
                    travel_packages_date.place(x=873, y=250)
                    calendar = Calendar(window_travels, selectmode='day', year=datetime.now().year,
                                        month=datetime.now().month)
                    calendar.place(x=680, y=280)

                    #выбор методов оплаты
                    payment_method_label = ttk.Label(window_travels, text="Способы оплаты",
                                                     background="#FAFAFA",
                                                     font=("Montserrat", 12))
                    payment_method_label.place(x=790, y=490)

                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute("SELECT name_payment_method FROM payment_methods")
                    payment_methods = cursor.fetchall()
                    conn.close()

                    #из списка кортежей в простой список
                    payment_methods_list = [method[0] for method in payment_methods]


                    payment_method_combobox = ttk.Combobox(window_travels,
                                                           values=payment_methods_list, state="readonly",
                                                           justify="left", background="#fafafa", height=40)
                    payment_method_combobox.place(x=785, y=520)

                    # кнопка для добавления даты и направления
                    choice = Button(window_travels, text="Выбрать", bg='#162013', width=20, fg="#FFFFFF",
                                    font=("Montserrat", 12), command=add_travel_data)
                    choice.place(height=45, x=720, y=570)
                else:
                    showerror(title="Ошибка", message="Неверный логин или пароль.")
            except Exception as e:
                showwarning(title="Предупреждение", message="Ошибка при входе в систему: " + str(e))
        else:
            showerror(title="Ошибка", message="Логин или пароль не соответствуют требованиям.")




    # окно входа
    main_root = Tk()
    main_root.title("Global Nomad")
    main_root.geometry('952x682+70+60')
    main_root.resizable(False, False)
    main_root.config(background="#FAFAFA")

    # # Загрузка изображения
    # background_image = PhotoImage(file="img/bcg.png")
    # background_label = ttk.Label(main_root, image=background_image)
    # background_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_lb = ttk.Label(main_root, text='Global Nomad', background="#FAFAFA", font=('Montserrat Alternates', 64))
    title_lb.pack(anchor='center', pady=140)
    label1 = ttk.Label(main_root, text="Введите данные для входа", background="#FAFAFA", font=("Montserrat", 12), foreground="#625D5D")
    label1.place(x=350, y=250)

    style = themed_style.ThemedStyle(main_root)
    style.theme_use("clam") # тема "clam", которая поддерживает "padding"
    style.configure("TEntry", padding=10)

    # Ввод логина
    entry_login = ttk.Entry(main_root, width=30)
    entry_login.place(x=290, y=330)
    entry_login.insert(0, "Email пользователя")
    entry_login.config(font=("Montserrat", 12), foreground="#625D5D")
    entry_login.bind("<FocusIn>", on_entry_click1)

    # Ввод пароля
    entry_password = ttk.Entry(main_root, width=30)
    entry_password.place(x=290, y=400)
    entry_password.insert(0, "Пароль")
    entry_password.config(font=("Montserrat", 12), foreground="#625D5D")
    entry_password.bind("<FocusIn>", on_entry_click2)

    # кнопка входа в приложение
    btn_enter = Button(main_root, text="Войти", bg='#162013', width=20, fg="#FFFFFF",
                       font=("Montserrat", 12), command=travel_packages)
    btn_enter.place(x=360, y=500, height=45)

    # кнопка регистрации
    btn_registr = Button(main_root, text="Регистрация", width=15, fg="#000000",
                         font=("Montserrat", 12), bg="#FAFAFA",
                         command=registration)
    btn_registr.place(x=15, y=10)
    btn_registr['borderwidth'] = 0



def choice_role_admin():
    choice_window.destroy()
    #  функции для удаления текста в полях ввода при нажатии
    def on_entry_click1(event):
        if entry_login_admin.get() == "Логин администратора":
            entry_login_admin.delete(0, END)
            entry_login_admin.config(foreground="black")

    def on_entry_click2(event):
        if entry_password_admin.get() == "Пароль":
            entry_password_admin.delete(0, END)
            entry_password_admin.config(foreground="black")


    def administrator_work_window():
        login_admin = entry_login_admin.get().strip()
        password_admin = entry_password_admin.get().strip()
        if login_admin and password_admin:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM administrator WHERE admin_login=? AND admin_password=?",
                               (login_admin, password_admin))
                admin = cursor.fetchone()
                conn.close()

                if admin:
                    showinfo(title='Вход', message='Успешный вход')
                    admin_root.destroy()
                    def on_entry_add_direction_click(event):
                        if entry_direction.get() == "Введите новое направление":
                            entry_direction.delete(0, END)
                            entry_direction.config(foreground="black")

                    def on_entry_discription_click(event):
                        if entry_description.get() == "Введите описание":
                            entry_description.delete(0, END)
                            entry_description.config(foreground="black")


                    # Отображение списка пользователей
                    def display_users():
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("SELECT user_id, email FROM users")
                        users = cursor.fetchall()
                        conn.close()

                        user_listbox.delete(0, END)  # Очистка списка перед добавлением новых данных
                        for user in users:
                            user_listbox.insert(END, f"№ пользователя: {user[0]}, Email: {user[1]}")

                    # Функция для добавления нового направления
                    def add_direction():
                        direction_name = entry_direction.get()
                        direction_description = entry_description.get()
                        if direction_name and direction_description:
                            conn = connect_db()
                            cursor = conn.cursor()
                            try:
                                cursor.execute("INSERT INTO direction (name_direction, description) VALUES (?, ?)",
                                               (direction_name, direction_description))
                                conn.commit()
                                showinfo("Успех", "Направление успешно добавлено!")
                                display_directions()  # Обновляем список направлений
                            except sqlite3.IntegrityError:
                                showerror("Ошибка", "Направление с таким именем уже существует.")
                            finally:
                                conn.close()
                        else:
                            showerror("Ошибка", "Введите название и описание направления.")

                    # Функция для отображения направлений
                    def display_directions():
                        conn = connect_db()
                        cursor = conn.cursor()
                        cursor.execute("SELECT direction_id, name_direction FROM direction")
                        directions = cursor.fetchall()
                        conn.close()

                        direction_listbox.delete(0, END)  # Очистка списка перед добавлением новых данных
                        for direction in directions:
                            direction_listbox.insert(END, f"№: {direction[0]}, Направление: {direction[1]}")

                    admin_window = Tk()
                    admin_window.title('Окно администрирования')
                    admin_window.geometry('1000x720')
                    admin_window.resizable(False, False)
                    admin_window.config(background='#fafafa')

                    title_lb = ttk.Label(admin_window, text='Global Nomad - Администрирование', background="#FAFAFA",
                                         font=('Montserrat Alternates', 24))
                    title_lb.pack(anchor='center', pady=20)
                    # Список пользователей
                    user_listbox = Listbox(admin_window, width=40, height=15, font=("Montserrat", 12))
                    user_listbox.place(x=15, y=80)

                    # Кнопка для отображения пользователей
                    btn_show_users = Button(admin_window, text="Показать пользователей", command=display_users,
                                            bg='#162013',
                                            fg="#FFFFFF", font=("Montserrat", 12))
                    btn_show_users.place(x=15, y=450)


                    # Список направлений
                    direction_listbox = Listbox(admin_window, width=40, height=15, font=("Montserrat", 12))
                    direction_listbox.place(x=530, y=80)

                    # Кнопка для отображения направлений
                    btn_show_directions = Button(admin_window, text="Показать направления", command=display_directions,
                                                 bg='#162013', fg="#FFFFFF", font=("Montserrat", 12))
                    btn_show_directions.place(x=530, y=450)


                    style = themed_style.ThemedStyle(admin_window)
                    style.theme_use("clam")  # тема "clam", которая поддерживает "padding"
                    style.configure("TEntry", padding=10)

                    # Поле для добавления нового направления
                    entry_direction = ttk.Entry(admin_window, width=30)
                    entry_direction.place(x=530, y=510)
                    entry_direction.insert(0, "Введите новое направление")
                    entry_direction.config(font=("Montserrat", 12), foreground="#625D5D")
                    entry_direction.bind("<FocusIn>", on_entry_add_direction_click)

                    # Поле для добавления описания нового направления
                    entry_description = ttk.Entry(admin_window, width=30)
                    entry_description.place(x=530, y=565)
                    entry_description.insert(0, "Введите описание")
                    entry_description.config(font=("Montserrat", 12), foreground="#625D5D")
                    entry_description.bind("<FocusIn>", on_entry_discription_click)

                    # Кнопка для добавления нового направления
                    btn_add_direction = Button(admin_window, text="Добавить направление", command=add_direction,
                                               bg='#162013',
                                               fg="#FFFFFF", font=("Montserrat", 12))
                    btn_add_direction.place(x=530, y=630)

                    # Закрытие окна администратора
                    btn_close = Button(admin_window, text="Закрыть", command=admin_window.destroy, bg='#FF0000',
                                       fg="#FFFFFF",
                                       font=("Montserrat", 12))
                    btn_close.place(x=890, y=660)
                else:
                    showerror(title='Предупреждение', message='Неверный логин или пароль администратора')
            except Exception as e:
                showerror(title="Ошибка", message=f"Ошибка при входе в систему: {str(e)}")


    # окно входа
    admin_root = Tk()
    admin_root.title("Global Nomad")
    admin_root.geometry('952x682+70+60')
    admin_root.resizable(False, False)
    admin_root.config(background="#FAFAFA")

    title_lb = ttk.Label(admin_root, text='Global Nomad', background="#FAFAFA", font=('Montserrat Alternates', 64))
    title_lb.pack(anchor='center', pady=140)
    label1 = ttk.Label(admin_root, text="Введите данные для входа", background="#FAFAFA", font=("Montserrat", 12),
                       foreground="#625D5D")
    label1.place(x=350, y=250)

    style = themed_style.ThemedStyle(admin_root)
    style.theme_use("clam")  # тема "clam", которая поддерживает "padding"
    style.configure("TEntry", padding=10)

    # Ввод логина
    entry_login_admin = ttk.Entry(admin_root, width=30)
    entry_login_admin.place(x=290, y=330)
    entry_login_admin.insert(0, "Логин администратора")
    entry_login_admin.config(font=("Montserrat", 12), foreground="#625D5D")
    entry_login_admin.bind("<FocusIn>", on_entry_click1)

    # Ввод пароля
    entry_password_admin = ttk.Entry(admin_root, width=30)
    entry_password_admin.place(x=290, y=400)
    entry_password_admin.insert(0, "Пароль")
    entry_password_admin.config(font=("Montserrat", 12), foreground="#625D5D")
    entry_password_admin.bind("<FocusIn>", on_entry_click2)

    # кнопка входа в окно администрирования
    btn_enter = Button(admin_root, text="Войти", bg='#162013', width=20, fg="#FFFFFF",
                       font=("Montserrat", 12), command=administrator_work_window)
    btn_enter.place(x=360, y=500, height=45)



choice_window = Tk()
choice_window.title('Выбор роли')
choice_window.geometry('400x300')
choice_window.configure(background='#fafafa')

label = ttk.Label(choice_window, text="Выберите вашу роль", font=("Montserrat", 20), background="#FAFAFA")
label.pack(pady=50)

user_button = Button(choice_window, text="Пользователь", command=choice_role_user, width=20)
user_button.pack(pady=10)

admin_button = Button(choice_window, text="Администратор", width=20, command=choice_role_admin)
admin_button.pack(pady=10)

choice_window.mainloop()


