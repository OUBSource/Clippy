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

# Основной плеер на tkinter
class DesktopVideoPlayer:
    def __init__(self, language="English"):
        self.language = language
        self.audio_file = "hello.wav" if language == "English" else "hello_rus.wav"
        
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
        
        # Показываем первый кадр из clippy.webp
        self.show_first_frame()
        
        # Бинды
        self.image_label.bind("<ButtonPress-1>", self.on_press)
        self.image_label.bind("<ButtonRelease-1>", self.on_release)
        self.image_label.bind("<B1-Motion>", self.on_drag)
        
        # Таймер для физики
        self.physics_timer()
        
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
            
            # Сразу после clippy.webp воспроизводим clippy2.webp С АУДИО
            if os.path.exists("clippy2.webp"):
                try:
                    # Запускаем аудио одновременно с clippy2.webp
                    audio_thread = threading.Thread(target=self.play_audio, daemon=True)
                    audio_thread.start()
                    
                    self.play_animated_webp("clippy2.webp", 3)
                except Exception as e:
                    print(f"Error playing clippy2.webp: {e}")
                    time.sleep(2)
            
            # После завершения показываем последний кадр clippy2.webp
            self.root.after(0, self.show_last_frame_of_clippy2)
        
        threading.Thread(target=play_sequence, daemon=True).start()
    
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
    
    def show_last_frame_of_clippy2(self):
        """Показываем последний кадр clippy2.webp"""
        if os.path.exists("clippy2.webp"):
            try:
                webp_image = Image.open("clippy2.webp")
                if hasattr(webp_image, 'n_frames') and webp_image.n_frames > 1:
                    webp_image.seek(webp_image.n_frames - 1)
                
                image = webp_image.resize((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            except Exception as e:
                print(f"Error showing last frame: {e}")
        
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
    
    required_files = ["clippy.webp", "clippy2.webp"]
    audio_file = "hello.wav" if language == "English" else "hello_rus.wav"
    required_files.append(audio_file)
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"Warning: {file} not found!")
    
    player = DesktopVideoPlayer(language)
    player.run()