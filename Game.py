import sys
from random import randint

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, \
    QMessageBox, QStatusBar, QPushButton

from Apple import Apple
from Audio import Audio
from Snake import Snake, Snake_Item

HEIGHT = 375
WIDTH = 375


class Field(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        dark_color = QColor(51, 102, 51)
        light_color = QColor(51, 153, 51)

        for i in range(8):
            for j in range(8):
                label = QWidget()
                color = dark_color if (i + j) % 2 == 0 else light_color
                label.setAutoFillBackground(True)
                p = label.palette()
                p.setColor(label.backgroundRole(), color)
                label.setPalette(p)
                layout.addWidget(label, i, j)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake")
        self.setGeometry(300, 300, HEIGHT, WIDTH)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QGridLayout()
        central_widget.setLayout(self.main_layout)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.score = 0
        self.high_score = self.load_from_file()
        self.update_score()

        self.chess_board = Field()
        self.head = Snake_Item()
        self.tail = Snake_Item()
        self.snake = Snake(self.head, self.tail)
        self.apple = Apple()

        self.main_layout.addWidget(self.chess_board, 0, 0)
        self.main_layout.addWidget(self.head, 0, 0)
        self.main_layout.addWidget(self.tail, 0, 0)
        self.main_layout.addWidget(self.snake, 0, 0)
        self.main_layout.addWidget(self.apple, 0, 0)

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(10)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.eaten_apple = False

        self.audio = Audio()
        self.audio.load_sounds_from_directory("sounds")

        self.audio.play_sound("651670__code_box__desert-snake.wav", loop_count=10)

        self.paused = False
        self.toggle_pause_key = Qt.Key.Key_Escape
        self.toggle_pause_button = QPushButton("Pause/Resume")
        self.toggle_pause_button.clicked.connect(self.toggle_pause)
        self.snake_timer = self.snake.timer

    def move_snake(self):
        self.snake.move_snake()

    def update_score(self):
        self.score += 10
        self.statusBar.showMessage(f"Score: {self.score}")

    def snake_apple(self):
        apple_x = self.apple.x
        apple_y = self.apple.y
        apple_size = self.apple.apple_size
        head_x = self.snake.head.x
        head_y = self.snake.head.y

        if (head_x < apple_x + apple_size and
                head_x + self.snake.head.snake_size > apple_x and
                head_y < apple_y + apple_size and
                head_y + self.snake.head.snake_size > apple_y):
            self.eaten_apple = True

    def snake_conflict(self):
        head_x = self.snake.head.x
        head_y = self.snake.head.y

        for segment in self.snake.snake_items[2:]:
            if head_x == segment.x and head_y == segment.y:
                return True
        return False

    def generate_apple_pos(self):
        snake_body = self.snake.snake_items
        positions = [(body.x, body.y) for body in snake_body]

        while True:
            new_x = randint(0, self.chess_board.width() - self.apple.apple_size)
            new_y = randint(0, self.chess_board.height() - self.apple.apple_size)
            if all(abs(new_x - x) > self.apple.apple_size or abs(new_y - y) > self.apple.apple_size for x, y in
                   positions):
                return new_x, new_y

    def update_game(self):
        if self.snake_conflict():
            self.game_over()

        self.snake_apple()
        if self.eaten_apple:
            self.audio.play_sound("411595__omgbong__eating-an-apple-03.wav", 800)
            self.snake.eat_apple()
            self.snake.tail = self.snake.snake_items[-1]
            self.main_layout.addWidget(self.tail, 0, 0)
            self.apple.x, self.apple.y = self.generate_apple_pos()
            self.eaten_apple = False
            self.update_score()

        self.apple.repaint()

    def game_over(self):
        self.toggle_pause()
        for sound in self.audio.sounds.values():
            sound.stop()
        message = QMessageBox()
        message.setWindowTitle("Game Over")
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            message.setText(f"Ты столкнулся с самим собой! Игра завершена.\nТы поставил новый рекорд!!! {self.score}")
            self.audio.play_sound("533034__evretro__8-bit-game-over-soundtune.wav")

        else:
            self.audio.play_sound("173859__jivatma07__j1game_over_mono.wav")
            message.setText(f"Ты столкнулся с самим собой! Игра завершена.\nТвой счет: {self.score}")

        message.addButton("Начать заново", QMessageBox.ButtonRole.AcceptRole)
        message.addButton("Выход", QMessageBox.ButtonRole.RejectRole)
        message.setDefaultButton(QMessageBox.StandardButton.Yes)
        message.buttonClicked.connect(self.handle_game_over_response)
        message.exec()

    def handle_game_over_response(self, button):
        if button.text() == "Начать заново":
            self.restart_game()
        else:
            sys.exit()

    def restart_game(self):
        self.main_layout.removeWidget(self.head)
        self.main_layout.removeWidget(self.tail)
        self.main_layout.removeWidget(self.snake)
        self.main_layout.removeWidget(self.apple)

        self.head = Snake_Item()
        self.tail = Snake_Item()
        self.snake = Snake(self.head, self.tail)
        self.apple = Apple()

        self.main_layout.addWidget(self.head, 0, 0)
        self.main_layout.addWidget(self.tail, 0, 0)
        self.main_layout.addWidget(self.snake, 0, 0)
        self.main_layout.addWidget(self.apple, 0, 0)

        self.score = 0
        self.update_score()

        self.audio.play_sound("651670__code_box__desert-snake.wav", loop_count=10)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.toggle_pause()
        if not self.paused:
            if event.key() == Qt.Key.Key_Left and self.snake.direction != 'Right':
                self.snake.direction = 'Left'
            elif event.key() == Qt.Key.Key_Right and self.snake.direction != 'Left':
                self.snake.direction = 'Right'
            elif event.key() == Qt.Key.Key_Up and self.snake.direction != 'Down':
                self.snake.direction = 'Up'
            elif event.key() == Qt.Key.Key_Down and self.snake.direction != 'Up':
                self.snake.direction = 'Down'
            event.accept()

    def load_from_file(self):
        try:
            with open("high_score.txt", 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", 'w') as file:
            file.write(str(self.high_score))

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.game_timer.stop()
            self.snake_timer.stop()
            self.statusBar.showMessage("Game Paused")
            self.audio.pause_music("651670__code_box__desert-snake.wav")
        else:
            self.game_timer.start()
            self.snake_timer.start()
            self.statusBar.showMessage(f"Score: {self.score}")
            self.audio.resume_music("651670__code_box__desert-snake.wav")