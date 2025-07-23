import customtkinter as ctk  # Импортируем современный модуль для создания интерфейсов на Tkinter
import psutil  # Модуль для получения системной информации (загрузка CPU, RAM и т.д.)
import time  # Модуль для работы со временем
import os  # Модуль для работы с файлами и папками
import datetime  # Модуль для получения текущей даты и времени

# Устанавливаем темную тему для интерфейса
ctk.set_appearance_mode("dark")
# Устанавливаем цветовую схему (синий цвет) для интерфейса
ctk.set_default_color_theme("blue")

# Имя файла, из которого изначально будем загружать заметки при первом открытии
NOTES_FILE = "notes.txt"


class StylishSticker(ctk.CTk):
    def __init__(self):
        super().__init__()  # Инициализируем родительский класс (CTk)

        # Задаём размер окна и его расположение на экране
        self.geometry("320x350+100+100")
        # Задаём цвет фона главного окна — тёмно-серый
        self.configure(fg_color="#222222")
        # Устанавливаем заголовок окна
        self.title("Системный подоконник")

        # Создаём фрейм (контейнер) внутри окна с закруглёнными углами и своим фоном
        self.container = ctk.CTkFrame(self, corner_radius=20, fg_color="#2E2E2E")
        # Устанавливаем фрейму режим заполнения окна с отступами
        self.container.pack(expand=True, fill="both", padx=15, pady=15)

        # Создаём метку — заголовок внутри фрейма с крупным жирным шрифтом
        self.title_label = ctk.CTkLabel(
            self.container,
            text="Монитор системы",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        # Размещаем заголовок с отступами сверху и снизу
        self.title_label.pack(pady=(10, 15))

        # Метка для отображения загрузки процессора (CPU)
        self.cpu_label = ctk.CTkLabel(
            self.container, text="CPU Load: 0%", font=ctk.CTkFont(size=14)
        )
        self.cpu_label.pack()
        # Прогрессбар, показывающий визуально загрузку CPU
        self.cpu_progress = ctk.CTkProgressBar(self.container, width=250)
        self.cpu_progress.pack(pady=(5, 10))

        # Метка и прогрессбар для загрузки оперативной памяти (RAM)
        self.ram_label = ctk.CTkLabel(
            self.container, text="RAM Load: 0%", font=ctk.CTkFont(size=14)
        )
        self.ram_label.pack()
        self.ram_progress = ctk.CTkProgressBar(self.container, width=250)
        self.ram_progress.pack(pady=(5, 10))

        # Метка для отображения времени работы системы
        self.uptime_label = ctk.CTkLabel(
            self.container, text="Uptime: 0d 0h 0m 0s", font=ctk.CTkFont(size=14)
        )
        self.uptime_label.pack(pady=(15, 10))

        # Кнопка, которая при нажатии откроет окно с заметками
        self.open_text_button = ctk.CTkButton(
            self.container, text="Открыть заметки", command=self.open_text_window
        )
        self.open_text_button.pack(pady=10)

        # Кнопка "Выход" для закрытия всего приложения
        self.close_button = ctk.CTkButton(
            self.container,
            text="Выход",
            command=self.close_all,  # При нажатии вызывается метод close_all
            fg_color="#D9534F",  # Красный цвет кнопки
            hover_color="#C9302C",  # Цвет при наведении мыши
        )
        self.close_button.pack(pady=(0, 5))

        # Ссылка на окно заметок, пока окна нет — значение None
        self.text_window = None

        # Перехватываем нажатие на крестик главного окна и вызываем метод close_all,
        # чтобы корректно закрыть и заметки, если они открыты
        self.protocol("WM_DELETE_WINDOW", self.close_all)

        # Запускаем обновление системной информации (CPU, RAM, Uptime)
        self.update_stats()

    def update_stats(self):
        # Получаем процент загрузки CPU из psutil
        cpu_load = psutil.cpu_percent(interval=None)
        # Обновляем текст метки CPU
        self.cpu_label.configure(text=f"CPU Load: {cpu_load}%")
        # Обновляем прогрессбар (значение от 0 до 1)
        self.cpu_progress.set(cpu_load / 100)

        # Аналогично для RAM
        ram_load = psutil.virtual_memory().percent
        self.ram_label.configure(text=f"RAM Load: {ram_load}%")
        self.ram_progress.set(ram_load / 100)

        # Считаем количество секунд с момента загрузки системы
        uptime_sec = time.time() - psutil.boot_time()
        # Форматируем это время в «дни, часы, минуты, секунды» и обновляем метку
        self.uptime_label.configure(text=f"Uptime: {self.format_time(uptime_sec)}")

        # Планируем следующий вызов update_stats через 1000 мс (1 секунда)
        self.after(1000, self.update_stats)

    def format_time(self, seconds):
        # Делим секунды на количество дней и остаток
        days, rem = divmod(seconds, 86400)
        # Делим остаток на часы и остаток
        hours, rem = divmod(rem, 3600)
        # Делим остаток на минуты и секунды
        minutes, seconds = divmod(rem, 60)
        # Возвращаем отформатированную строку
        return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

    def open_text_window(self):
        # Проверяем, если окно заметок не создано или было уничтожено, создаём новое
        if self.text_window is None or not self.text_window.winfo_exists():
            self.text_window = ctk.CTkToplevel(self)  # Создаём новое окно (вторичное)
            self.text_window.geometry(
                "350x300+450+100"
            )  # Задаём размер и положение окна
            self.text_window.title("Заметки")  # Заголовок окна
            self.text_window.configure(fg_color="#2E2E2E")  # Цвет фона окна заметок

            # При закрытии окна заметок мышью вызываем on_close_notes_window,
            # чтобы сохранить заметки и скрыть окно (не уничтожать)
            self.text_window.protocol("WM_DELETE_WINDOW", self.on_close_notes_window)

            # Создаём многострочное текстовое поле для заметок
            self.textbox = ctk.CTkTextbox(self.text_window, font=ctk.CTkFont(size=12))
            self.textbox.pack(expand=True, fill="both", padx=15, pady=15)

            # --- Загружаем текст из файла, если он есть ---
            if os.path.exists(NOTES_FILE):
                try:
                    with open(NOTES_FILE, "r", encoding="utf-8") as f:
                        notes_content = f.read()  # Считываем все содержимое файла
                except Exception as e:
                    # Если произошла ошибка при чтении файла — покажем в текстовом поле ошибку
                    notes_content = f"Ошибка чтения файла: {e}\n"
            else:
                # Если файла нет, вставляем подсказку
                notes_content = "Введите свои заметки здесь..."

            # Добавляем загруженный текст в текстовое поле
            self.textbox.insert("0.0", notes_content)
        else:
            # Если окно заметок уже открыто, просто поднимаем его на передний план
            self.text_window.deiconify()  # Показываем окно, если было скрыто
            self.text_window.lift()  # Поднимает поверх других окон
            self.text_window.focus_force()  # Дает фокус (активное окно)

    def save_notes(self):
        # Проверяем, что окно заметок существует и активно
        if self.text_window and self.text_window.winfo_exists():
            # Получаем весь текст из текстового поля (без последнего лишнего переноса строки)
            current_notes = self.textbox.get("0.0", "end-1c")
            # Формируем новую папку для хранения заметок (если её нет — создаём)
            folder = "notes_history"
            os.makedirs(folder, exist_ok=True)
            # Формируем имя файла с текущей датой и временем (например, notes_2025-07-22_17-55-30.txt)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(folder, f"notes_{timestamp}.txt")
            try:
                # Записываем текст в новый файл
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(current_notes)
            except Exception as e:
                # Если произошла ошибка сохранения — выводим в консоль (можно заменить на всплывающее окно)
                print(f"Ошибка сохранения заметок: {e}")

    def on_close_notes_window(self):
        # Вызывается при закрытии окна заметок
        self.save_notes()  # Сначала сохраняем заметки в отдельный файл с датой/временем
        self.text_window.withdraw()  # Потом просто скрываем окно заметок (не уничтожаем)

    def close_all(self):
        # Обрабатываем полное закрытие главного окна программы
        # Если окно заметок открыто — сначала сохраним заметки и уничтожим окно заметок
        if self.text_window is not None and self.text_window.winfo_exists():
            self.save_notes()  # Сохраняем заметки
            self.text_window.destroy()  # Закрываем окно заметок
            self.text_window = None  # Обнуляем ссылку

        # Закрываем главное окно, что остановит программу полностью
        self.destroy()


# Запуск программы — создаём объект приложения и запускаем главный цикл
if __name__ == "__main__":
    app = StylishSticker()
    app.mainloop()
