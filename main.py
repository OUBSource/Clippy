import tkinter as tk
from PIL import Image, ImageTk
import os
import threading
import time
import winsound
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

# Диалог выбора языка на PyQt5
class LanguageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.selected_language = "English"
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Select Language")
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        layout = QVBoxLayout()
        
        label = QLabel("Choose language:")
        layout.addWidget(label)
        
        self.combo = QComboBox()
        self.combo.addItems(["English", "Russian"])
        layout.addWidget(self.combo)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept_selection)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)
        
    def accept_selection(self):
        self.selected_language = self.combo.currentText()
        self.accept()

def select_language():
    app = QApplication([])
    dialog = LanguageDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selected_language
    return "English"

# Окно Help в стиле Windows 95
class Windows95HelpWindow:
    def __init__(self, parent, language="English"):
        self.parent = parent
        self.language = language
        self.root = tk.Toplevel(parent)
        self.setup_window()
        self.create_content()
        
    def setup_window(self):
        """Настройка окна в стиле Windows 95"""
        title = "Help" if self.language == "English" else "Помощь"
        self.root.title(title)
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#c0c0c0')
        self.root.attributes('-topmost', True)
        
        # Скрываем стандартную рамку и убираем из панели задач
        self.root.overrideredirect(True)
        self.root.attributes('-toolwindow', True)
        
        # Центрируем окно
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        # Создаем кастомную title bar
        self.create_custom_title_bar()
        
        # Переменные для перетаскивания
        self.x = 0
        self.y = 0
        
    def create_custom_title_bar(self):
        """Создает кастомную title bar с возможностью перетаскивания"""
        self.title_bar = tk.Frame(self.root, bg='#000080', height=20)
        self.title_bar.pack(fill='x', side='top')
        self.title_bar.pack_propagate(False)
        
        # Заголовок
        title = "Help" if self.language == "English" else "Помощь"
        title_label = tk.Label(self.title_bar, text=title, 
                              bg='#000080', fg='white', font=('MS Sans Serif', 8, 'bold'))
        title_label.pack(side='left', padx=2)
        
        # Крестик для закрытия (работающий)
        self.close_btn = tk.Label(self.title_bar, text="✕", 
                                 bg='#c0c0c0', fg='black', font=('Arial', 8, 'bold'),
                                 relief='raised', bd=1, width=3, height=1)
        self.close_btn.pack(side='right', padx=1, pady=1)
        self.close_btn.bind('<Button-1>', self.start_close_animation)
        self.close_btn.bind('<Enter>', lambda e: self.close_btn.config(bg='#ff0000', fg='white'))
        self.close_btn.bind('<Leave>', lambda e: self.close_btn.config(bg='#c0c0c0', fg='black'))
        
        # Привязываем события перетаскивания к title bar
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.on_move)
        title_label.bind('<Button-1>', self.start_move)
        title_label.bind('<B1-Motion>', self.on_move)
        
    def start_move(self, event):
        """Начало перемещения окна"""
        self.x = event.x_root
        self.y = event.y_root
        
    def on_move(self, event):
        """Перемещение окна"""
        deltax = event.x_root - self.x
        deltay = event.y_root - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        self.x = event.x_root
        self.y = event.y_root
        
    def create_content(self):
        """Создает содержимое окна Help"""
        self.content_frame = tk.Frame(self.root, bg='#c0c0c0', relief='sunken', bd=1)
        self.content_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Иконка
        icon_frame = tk.Frame(self.content_frame, bg='#c0c0c0')
        icon_frame.pack(side='left', padx=15, pady=20)
        
        icon_label = tk.Label(icon_frame, text="❓", 
                             font=('Arial', 24), bg='#c0c0c0', fg='blue')
        icon_label.pack()
        
        # Текст справки
        text_frame = tk.Frame(self.content_frame, bg='#c0c0c0')
        text_frame.pack(side='top', fill='both', expand=True, padx=(0, 15), pady=20)
        
        if self.language == "English":
            help_text = """Clippy Assistant Help

This is a virtual desktop assistant that can:
• Move around your screen with physics
• Respond to your clicks
• Offer help when needed
• Speak in different languages

Click on Clippy to interact with him.
Right-click for additional options.

Drag to move him around.
He will bounce off windows and screen edges."""
        else:
            help_text = """Справка помощника Clippy

Это виртуальный помощник для рабочего стола который может:
• Перемещаться по экрану с физикой
• Реагировать на клики
• Предлагать помощь когда нужно
• Говорить на разных языках

Нажмите на Clippy для взаимодействия.
Правая кнопка мыши - дополнительные опции.

Перетаскивайте чтобы перемещать.
Он будет отскакивать от окон и краев экрана."""
        
        help_label = tk.Label(text_frame, text=help_text,
                             bg='#c0c0c0', fg='black', font=('MS Sans Serif', 9),
                             justify='left', wraplength=300)
        help_label.pack(anchor='w')
        
        # Кнопка OK
        button_frame = tk.Frame(self.content_frame, bg='#c0c0c0')
        button_frame.pack(side='bottom', anchor='se', pady=15, padx=15)
        
        self.ok_btn = tk.Button(button_frame, text="OK", 
                               font=('MS Sans Serif', 9),
                               relief='raised', bd=2,
                               width=12, height=1,
                               command=self.start_close_animation)
        self.ok_btn.pack()
        self.root.bind('<Return>', lambda e: self.start_close_animation())
        
    def start_close_animation(self, event=None):
        """Запускает анимацию закрытия"""
        self.ok_btn.config(state='disabled')
        self.close_btn.config(state='disabled')
        self.animate_close(self.root.winfo_width(), self.root.winfo_height())
        
    def animate_close(self, width, height):
        """Анимация сжатия окна"""
        if height > 0:
            # Уменьшаем высоту
            new_height = max(0, height - 15)
            
            # Получаем текущую позицию
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            
            # Вычисляем новую позицию для сжатия к центру
            new_y = y + (height - new_height) // 2
            
            self.root.geometry(f"{width}x{new_height}+{x}+{new_y}")
            
            if new_height > 0:
                self.root.after(25, self.animate_close, width, new_height)
            else:
                # Гарантируем полное закрытие
                self.root.geometry(f"{width}x0+{x}+{new_y}")
                self.root.update()
                # Закрываем окно после завершения анимации
                self.root.after(50, self.root.destroy)
        else:
            self.root.after(50, self.root.destroy)

# Окно About в стиле Windows 95
class Windows95AboutWindow:
    def __init__(self, parent, language="English"):
        self.parent = parent
        self.language = language
        self.root = tk.Toplevel(parent)
        self.setup_window()
        self.create_content()
        
    def setup_window(self):
        """Настройка окна в стиле Windows 95"""
        title = "About" if self.language == "English" else "О программе"
        self.root.title(title)
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        self.root.configure(bg='#c0c0c0')
        self.root.attributes('-topmost', True)
        
        # Скрываем стандартную рамку и убираем из панели задач
        self.root.overrideredirect(True)
        self.root.attributes('-toolwindow', True)
        
        # Центрируем окно
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        # Создаем кастомную title bar
        self.create_custom_title_bar()
        
        # Переменные для перетаскивания
        self.x = 0
        self.y = 0
        
    def create_custom_title_bar(self):
        """Создает кастомную title bar с возможностью перетаскивания"""
        self.title_bar = tk.Frame(self.root, bg='#000080', height=20)
        self.title_bar.pack(fill='x', side='top')
        self.title_bar.pack_propagate(False)
        
        # Заголовок
        title = "About" if self.language == "English" else "О программе"
        title_label = tk.Label(self.title_bar, text=title, 
                              bg='#000080', fg='white', font=('MS Sans Serif', 8, 'bold'))
        title_label.pack(side='left', padx=2)
        
        # Крестик для закрытия (работающий)
        self.close_btn = tk.Label(self.title_bar, text="✕", 
                                 bg='#c0c0c0', fg='black', font=('Arial', 8, 'bold'),
                                 relief='raised', bd=1, width=3, height=1)
        self.close_btn.pack(side='right', padx=1, pady=1)
        self.close_btn.bind('<Button-1>', self.start_close_animation)
        self.close_btn.bind('<Enter>', lambda e: self.close_btn.config(bg='#ff0000', fg='white'))
        self.close_btn.bind('<Leave>', lambda e: self.close_btn.config(bg='#c0c0c0', fg='black'))
        
        # Привязываем события перетаскивания к title bar
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<B1-Motion>', self.on_move)
        title_label.bind('<Button-1>', self.start_move)
        title_label.bind('<B1-Motion>', self.on_move)
        
    def start_move(self, event):
        """Начало перемещения окна"""
        self.x = event.x_root
        self.y = event.y_root
        
    def on_move(self, event):
        """Перемещение окна"""
        deltax = event.x_root - self.x
        deltay = event.y_root - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        self.x = event.x_root
        self.y = event.y_root
        
    def create_content(self):
        """Создает содержимое окна About"""
        self.content_frame = tk.Frame(self.root, bg='#c0c0c0', relief='sunken', bd=1)
        self.content_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Иконка
        icon_frame = tk.Frame(self.content_frame, bg='#c0c0c0')
        icon_frame.pack(side='left', padx=15, pady=20)
        
        icon_label = tk.Label(icon_frame, text="ℹ️", 
                             font=('Arial', 24), bg='#c0c0c0', fg='navy')
        icon_label.pack()
        
        # Текст информации
        text_frame = tk.Frame(self.content_frame, bg='#c0c0c0')
        text_frame.pack(side='top', fill='both', expand=True, padx=(0, 15), pady=20)
        
        if self.language == "English":
            about_text = """Clippy Assistant
Version 1.0

A virtual desktop assistant inspired by Microsoft Office Assistant.

Features:
• Physics-based movement
• Multi-language support
• Interactive animations
• Context menu

Created with Python and tkinter"""
        else:
            about_text = """Помощник Clippy
Версия 1.0

Виртуальный помощник для рабочего стола вдохновленный помощником Microsoft Office.

Возможности:
• Движение с физикой
• Поддержка нескольких языков
• Интерактивные анимации
• Контекстное меню

Создано на Python и tkinter"""
        
        about_label = tk.Label(text_frame, text=about_text,
                              bg='#c0c0c0', fg='black', font=('MS Sans Serif', 9),
                              justify='left', wraplength=250)
        about_label.pack(anchor='w')
        
        # Кнопка OK
        button_frame = tk.Frame(self.content_frame, bg='#c0c0c0')
        button_frame.pack(side='bottom', anchor='se', pady=15, padx=15)
        
        self.ok_btn = tk.Button(button_frame, text="OK", 
                               font=('MS Sans Serif', 9),
                               relief='raised', bd=2,
                               width=12, height=1,
                               command=self.start_close_animation)
        self.ok_btn.pack()
        self.root.bind('<Return>', lambda e: self.start_close_animation())
        
    def start_close_animation(self, event=None):
        """Запускает анимацию закрытия"""
        self.ok_btn.config(state='disabled')
        self.close_btn.config(state='disabled')
        self.animate_close(self.root.winfo_width(), self.root.winfo_height())
        
    def animate_close(self, width, height):
        """Анимация сжатия окна"""
        if height > 0:
            # Уменьшаем высоту
            new_height = max(0, height - 15)
            
            # Получаем текущую позицию
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            
            # Вычисляем новую позицию для сжатия к центру
            new_y = y + (height - new_height) // 2
            
            self.root.geometry(f"{width}x{new_height}+{x}+{new_y}")
            
            if new_height > 0:
                self.root.after(25, self.animate_close, width, new_height)
            else:
                # Гарантируем полное закрытие
                self.root.geometry(f"{width}x0+{x}+{new_y}")
                self.root.update()
                # Закрываем окно после завершения анимации
                self.root.after(50, self.root.destroy)
        else:
            self.root.after(50, self.root.destroy)

# Основной плеер на tkinter
class DesktopVideoPlayer:
    def __init__(self, language="English"):
        self.language = language
        self.audio_file = "hello.wav" if language == "English" else "hello_rus.wav"
        self.text_to_display = "Would you like help?" if language == "English" else "Вам нужна помощь?"
        
        self.root = tk.Tk()
        self.is_playing = False
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.friction = 0.98
        self.click_start_time = 0
        
        # Настройка прозрачного окна
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'white')
        self.root.attributes('-alpha', 0.99)
        
        # Размеры
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_size = 300
        
        # Начальная позиция - правый нижний угол
        self.x_pos = screen_width - window_size - 50
        self.y_pos = screen_height - window_size - 100
        
        self.root.geometry(f"{window_size}x{window_size}+{self.x_pos}+{self.y_pos}")
        self.root.configure(bg='white')
        
        # Label для отображения изображений
        self.image_label = tk.Label(self.root, bg='white')
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Label для отображения текста в левом верхнем углу
        # Используем указанный фон, шрифт и размер
        self.text_label = tk.Label(self.root, bg='#fffdcf', fg='black', font=('MS Sans Serif', 20),
                                  wraplength=250, justify='left', anchor='nw')
        self.text_label.place(x=15, y=30)  # Позиция в левом верхнем углу, пропустив 2 строки
        self.text_label.lower()  # Сразу скрываем текст
        
        # Создаем контекстное меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        
        # Показываем первый кадр из clippy.webp
        self.show_first_frame()
        
        # Бинды
        self.image_label.bind("<ButtonPress-1>", self.on_press)
        self.image_label.bind("<ButtonRelease-1>", self.on_release)
        self.image_label.bind("<B1-Motion>", self.on_drag)
        self.image_label.bind("<Button-3>", self.show_context_menu)  # Правая кнопка мыши
        
        # Таймер для физики
        self.physics_timer()
        
    def update_context_menu(self):
        """Обновляем контекстное меню в зависимости от языка"""
        self.context_menu.delete(0, tk.END)  # Очищаем меню
        
        if self.language == "English":
            self.context_menu.add_command(label="Hide", command=self.hide_window)
            self.context_menu.add_command(label="Help", command=self.show_help)
            self.context_menu.add_command(label="About", command=self.show_about)
        else:  # Russian
            self.context_menu.add_command(label="Скрыть", command=self.hide_window)
            self.context_menu.add_command(label="Помощь", command=self.show_help)
            self.context_menu.add_command(label="О программе", command=self.show_about)
    
    def show_context_menu(self, event):
        """Показываем контекстное меню"""
        self.update_context_menu()
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def hide_window(self):
        """Скрывает окно (закрывает программу)"""
        self.root.quit()
        self.root.destroy()
    
    def show_help(self):
        """Показывает справку в стиле Windows 95"""
        Windows95HelpWindow(self.root, self.language)
    
    def show_about(self):
        """Показывает информацию о программе в стиле Windows 95"""
        Windows95AboutWindow(self.root, self.language)
        
    def show_first_frame(self):
        """Показываем первый кадр из clippy.webp"""
        if os.path.exists("clippy.webp"):
            try:
                image = Image.open("clippy.webp")
                image = image.resize((300, 300), Image.Resampling.LANCZOS)
                self.current_image = ImageTk.PhotoImage(image)
                self.image_label.configure(image=self.current_image)
            except Exception as e:
                print(f"Error loading clippy.webp: {e}")
                self.show_placeholder()
        else:
            self.show_placeholder()
    
    def show_placeholder(self):
        """Заглушка если файлы не найдены"""
        self.image_label.configure(image='', bg='lightgray', text="No video files")
        
    def on_press(self, event):
        """Нажатие кнопки мыши - только запоминаем позицию"""
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        self.click_start_time = time.time()
        self.velocity_y = 0
        
    def on_drag(self, event):
        """Перетаскивание - устанавливаем флаг и перемещаем"""
        # Если переместили мышь достаточно далеко - это перетаскивание
        move_threshold = 5  # пикселей
        if (abs(event.x_root - self.drag_start_x) > move_threshold or 
            abs(event.y_root - self.drag_start_y) > move_threshold):
            self.is_dragging = True
        
        if self.is_dragging:
            x = self.root.winfo_x() + (event.x_root - self.drag_start_x)
            y = self.root.winfo_y() + (event.y_root - self.drag_start_y)
            
            # Ограничиваем перемещение в пределах экрана
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            x = max(0, min(x, screen_width - window_width))
            y = max(0, min(y, screen_height - window_height))
            
            self.root.geometry(f"+{int(x)}+{int(y)}")
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
            self.velocity_y = 0
            
    def on_release(self, event):
        """Отпускание кнопки мыши"""
        # Если это был клик (не перетаскивание) и не воспроизводится - запускаем видео
        if not self.is_dragging and not self.is_playing:
            click_duration = time.time() - self.click_start_time
            # Проверяем что это был короткий клик (не долгое удержание)
            if click_duration < 0.5:  # 500ms
                self.play_clippy_webp()
        
        self.is_dragging = False
        
    def play_audio(self):
        """Воспроизведение аудио"""
        if os.path.exists(self.audio_file):
            try:
                winsound.PlaySound(self.audio_file, winsound.SND_FILENAME)
                print(f"Audio played: {self.audio_file}")
            except Exception as e:
                print(f"Audio error: {e}")
        
    def play_clippy_webp(self):
        """Воспроизведение clippy.webp как видео"""
        if self.is_playing:
            return
            
        self.is_playing = True
        
        def play_sequence():
            # Воспроизводим clippy.webp (первое видео) БЕЗ АУДИО
            if os.path.exists("clippy.webp"):
                try:
                    self.play_animated_webp("clippy.webp", 3)
                except Exception as e:
                    print(f"Error playing clippy.webp: {e}")
                    time.sleep(2)
            
            # Сразу после clippy.webp воспроизводим clippit_text.png С АУДИО
            if os.path.exists("clippit_text.png"):
                try:
                    # Запускаем аудио одновременно с clippit_text.png
                    audio_thread = threading.Thread(target=self.play_audio, daemon=True)
                    audio_thread.start()
                    
                    # Показываем статичное изображение clippit_text.png
                    self.root.after(0, self.show_clippit_text_with_typing)
                    
                    # Ждем завершения аудио
                    time.sleep(self.get_audio_duration())
                    
                except Exception as e:
                    print(f"Error playing clippit_text.png: {e}")
                    time.sleep(2)
            
            # После завершения показываем последний кадр clippy.webp
            self.root.after(0, self.show_last_frame_of_clippy)
        
        threading.Thread(target=play_sequence, daemon=True).start()
    
    def get_audio_duration(self):
        """Получаем длительность аудиофайла"""
        try:
            import wave
            with wave.open(self.audio_file, 'rb') as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                duration = frames / float(rate)
                return duration
        except:
            # Если не удалось определить длительность, возвращаем значение по умолчанию
            return 3.0
    
    def show_clippit_text_with_typing(self):
        """Показываем clippit_text.png с постепенной печатью текста"""
        try:
            # Загружаем и показываем изображение
            image = Image.open("clippit_text.png")
            image = image.resize((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
            
            # Показываем текстовый лейбл и запускаем анимацию печати
            self.text_label.lift()
            self.start_typing_animation()
            
        except Exception as e:
            print(f"Error loading clippit_text.png: {e}")
    
    def start_typing_animation(self):
        """Запускаем анимацию постепенной печати текста"""
        audio_duration = self.get_audio_duration()
        
        # Рассчитываем время для печати текста (немного меньше длительности аудио)
        typing_duration = audio_duration - 0.3
        
        # Запускаем печать в отдельном потоке
        threading.Thread(target=self.type_text_gradually, 
                        args=(self.text_to_display, typing_duration), 
                        daemon=True).start()
    
    def type_text_gradually(self, text, duration):
        """Постепенно печатает текст с синхронизацией по аудио"""
        current_text = ""
        total_chars = len(text)
        delay_per_char = duration / total_chars if total_chars > 0 else 0
        
        for i, char in enumerate(text):
            if not self.is_playing:  # Прерываем если остановлено
                break
                
            current_text += char
            
            # Обновляем текст в основном потоке tkinter
            self.root.after(0, lambda t=current_text: self.update_text(t))
            
            # Задержка между символами
            time.sleep(delay_per_char)
    
    def update_text(self, text):
        """Обновляет текст на экране"""
        self.text_label.configure(text=text)
    
    def play_animated_webp(self, webp_path, duration_seconds):
        """Воспроизведение анимированного WebP"""
        try:
            webp_image = Image.open(webp_path)
            frames = []
            
            for frame in range(webp_image.n_frames):
                webp_image.seek(frame)
                frame_image = webp_image.copy()
                frame_image = frame_image.resize((300, 300), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame_image))
            
            frame_delay = duration_seconds / len(frames)
            
            for frame in frames:
                if not self.is_playing:
                    break
                self.root.after(0, lambda f=frame: self.update_frame(f))
                time.sleep(frame_delay)
            
        except Exception as e:
            print(f"Error playing animated WebP {webp_path}: {e}")
            self.root.after(0, lambda: self.show_static_webp(webp_path))
            time.sleep(duration_seconds)
    
    def update_frame(self, frame_image):
        """Обновление кадра на экране"""
        self.image_label.configure(image=frame_image)
        # Скрываем текст при показе анимированных кадров
        self.text_label.lower()
        self.text_label.configure(text="")
    
    def show_static_webp(self, webp_path):
        """Показ статичного WebP"""
        try:
            image = Image.open(webp_path)
            image = image.resize((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            print(f"Error showing static WebP: {e}")
    
    def show_last_frame_of_clippy(self):
        """Показываем последний кадр clippy.webp"""
        if os.path.exists("clippy.webp"):
            try:
                webp_image = Image.open("clippy.webp")
                if hasattr(webp_image, 'n_frames') and webp_image.n_frames > 1:
                    webp_image.seek(webp_image.n_frames - 1)
                
                image = webp_image.resize((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            except Exception as e:
                print(f"Error showing last frame: {e}")
        
        # Скрываем текст
        self.text_label.lower()
        self.text_label.configure(text="")
        self.is_playing = False
        
    def check_window_collision(self, x, y):
        """Проверяем столкновение с другими окнами"""
        try:
            import win32gui
            
            our_left = x
            our_top = y
            our_right = x + self.root.winfo_width()
            our_bottom = y + self.root.winfo_height()
            
            def enum_windows_callback(hwnd, collisions):
                if (win32gui.IsWindowVisible(hwnd) and 
                    win32gui.IsWindowEnabled(hwnd) and
                    hwnd != self.root.winfo_id()):
                    
                    try:
                        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                        window_title = win32gui.GetWindowText(hwnd)
                        
                        # Игнорируем системные окна без заголовков
                        if not window_title:
                            return True
                            
                        # Проверяем пересечение
                        if (our_left < right and our_right > left and
                            our_top < bottom and our_bottom > top):
                            collisions.append((left, top, right, bottom, window_title))
                    except:
                        pass
                return True
            
            collisions = []
            win32gui.EnumWindows(enum_windows_callback, collisions)
            
            return collisions
            
        except ImportError:
            return []
        
    def physics_timer(self):
        """Физика с проверкой столкновений с окнами и панелью задач"""
        if not self.is_dragging:  # Только когда НЕ перетаскиваем
            # Применяем гравитацию
            self.velocity_y += self.gravity
            
            # Получаем текущую позицию
            current_x = self.root.winfo_x()
            current_y = self.root.winfo_y()
            new_y = current_y + self.velocity_y
            
            screen_height = self.root.winfo_screenheight()
            window_height = self.root.winfo_height()
            
            # Сначала проверяем столкновение с панелью задач (нижняя граница экрана)
            taskbar_height = 40
            if new_y + window_height > screen_height - taskbar_height:
                new_y = screen_height - window_height - taskbar_height
                self.velocity_y = -self.velocity_y * 0.7
                if abs(self.velocity_y) < 1:
                    self.velocity_y = 0
            
            # Затем проверяем столкновения с другими окнами
            collisions = self.check_window_collision(current_x, new_y)
            
            if collisions:
                for left, top, right, bottom, title in collisions:
                    if new_y + window_height > top and current_y + window_height <= top:
                        new_y = top - window_height
                        self.velocity_y = 0
                        break
                    elif new_y < bottom and current_y >= bottom:
                        new_y = bottom
                        self.velocity_y = -self.velocity_y * 0.7
                        break
            
            # Проверяем верхнюю границу экрана
            elif new_y < 0:
                new_y = 0
                self.velocity_y = -self.velocity_y * 0.7
            
            # Применяем трение
            self.velocity_y *= self.friction
            
            if abs(self.velocity_y) < 0.1:
                self.velocity_y = 0
            
            # Обновляем позицию
            self.root.geometry(f"+{current_x}+{int(new_y)}")
        
        self.root.after(30, self.physics_timer)
        
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.destroy()

if __name__ == "__main__":
    language = select_language()
    print(f"Selected language: {language}")
    
    required_files = ["clippy.webp", "clippit_text.png"]
    audio_file = "hello.wav" if language == "English" else "hello_rus.wav"
    required_files.append(audio_file)
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"Warning: {file} not found!")
    
    player = DesktopVideoPlayer(language)
    player.run()