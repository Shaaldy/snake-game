from random import randint

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QFrame, QApplication, QGridLayout, QWidget, QVBoxLayout, QStackedLayout

from Apple import Apple
from Snake import Snake


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
        self.setGeometry(300, 300, 500, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout()  # Используем QGridLayout
        central_widget.setLayout(main_layout)

        self.chess_board = Field()
        self.snake = Snake()
        self.apple = Apple()

        main_layout.addWidget(self.chess_board, 0, 0)
        main_layout.addWidget(self.snake, 0, 0)
        main_layout.addWidget(self.apple, 0, 0)

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(10)  # Вызываем update_game каждые 10 мс

        self.snake_timer = QTimer(self)
        self.snake_timer.timeout.connect(self.move_snake)
        self.snake_timer.start(300)  # Двигаем змейку каждые 300 мс
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.eaten_apple = False

    def move_snake(self):
        self.snake.move_snake()  # Двигаем змейку
        self.snake.repaint()  # Перерисовываем змейку

    def snake_apple(self):
        snake_head_x = self.snake.x
        snake_head_y = self.snake.y
        apple_x = self.apple.x
        apple_y = self.apple.y
        apple_size = self.apple.apple_size

        if (snake_head_x < apple_x + apple_size and
                snake_head_x + self.snake.snake_size > apple_x and
                snake_head_y < apple_y + apple_size and
                snake_head_y + self.snake.snake_size > apple_y):
            self.eaten_apple = True

    def update_game(self):
        self.snake_apple()

        if self.eaten_apple:
            self.apple.x = randint(0, self.chess_board.width() - self.apple.apple_size)
            self.apple.y = randint(0, self.chess_board.height() - self.apple.apple_size)
            self.eaten_apple = False

        self.apple.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.snake.direction = 'Left'
        elif event.key() == Qt.Key.Key_Right:
            self.snake.direction = 'Right'
        elif event.key() == Qt.Key.Key_Up:
            self.snake.direction = 'Up'
        elif event.key() == Qt.Key.Key_Down:
            self.snake.direction = 'Down'
        event.accept()

