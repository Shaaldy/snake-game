from random import randint

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QFrame, QApplication, QGridLayout, QWidget, QVBoxLayout, QStackedLayout

from Apple import Apple
from Snake import Snake, Snake_Item


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

        self.main_layout = QGridLayout()
        central_widget.setLayout(self.main_layout)

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

        self.snake_timer = QTimer(self)
        self.snake_timer.timeout.connect(self.move_snake)
        self.snake_timer.start(30000)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.eaten_apple = False

    def move_snake(self):
        self.snake.move_snake()  # Двигаем змейку
        self.snake.repaint()  # Перерисовываем змейку

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

    def generate_apple_pos(self):
        snake_segments = self.snake.snake_items
        positions = [(segment.x, segment.y) for segment in snake_segments]

        while True:
            new_x = randint(0, self.chess_board.width() - self.apple.apple_size)
            new_y = randint(0, self.chess_board.height() - self.apple.apple_size)
            if all(abs(new_x - x) > self.apple.apple_size or abs(new_y - y) > self.apple.apple_size for x, y in
                   positions):
                return new_x, new_y

    def update_game(self):
        self.snake_apple()

        if self.eaten_apple:
            self.snake.eat_apple()
            self.snake.tail = self.snake.snake_items[-1]
            self.main_layout.addWidget(self.tail, 0, 0)
            self.apple.x, self.apple.y = self.generate_apple_pos()
            self.eaten_apple = False

        self.apple.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left and self.snake.direction != 'Right':
            self.snake.direction = 'Left'
        elif event.key() == Qt.Key.Key_Right and self.snake.direction != 'Left':
            self.snake.direction = 'Right'
        elif event.key() == Qt.Key.Key_Up and self.snake.direction != 'Down':
            self.snake.direction = 'Up'
        elif event.key() == Qt.Key.Key_Down and self.snake.direction != 'Up':
            self.snake.direction = 'Down'
        event.accept()
