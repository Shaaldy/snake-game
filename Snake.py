from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class Snake_Item(QWidget):
    def __init__(self):
        super().__init__()
        self.snake_size = 20
        self.x = 0
        self.y = 0
        self.prev_x = 0
        self.prev_y = 0

    def paintEvent(self, event):
        qp = QPainter(self)
        self.draw_snake(qp)

    def draw_snake(self, qp):
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(self.x, self.y, self.snake_size, self.snake_size)


class Snake(QWidget):
    def __init__(self, head, tail):
        super().__init__()
        self.snake_items = []
        self.head = head
        self.tail = tail
        self.snake_items.append(self.head)
        self.snake_items.append(self.tail)

        self.direction = 'Right'
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(100)

    def move_snake(self):
        # Новые координаты головы в зависимости от направления движения
        if self.direction == 'Right':
            self.head.x += self.snake_items[0].snake_size
            if self.head.x >= self.parent().width():
                self.head.x = 0
        elif self.direction == 'Left':
            self.head.x -= self.snake_items[0].snake_size
            if self.head.x < 0:
                self.head.x = self.parent().width() - self.head.snake_size
        elif self.direction == 'Up':
            self.head.y -= self.snake_items[0].snake_size
            if self.head.y < 0:
                self.head.y = self.parent().height() - self.head.snake_size
        elif self.direction == 'Down':
            self.head.y += self.snake_items[0].snake_size
            if self.head.y >= self.parent().height():
                self.head.y = 0

        for i in range(1, len(self.snake_items)):
            self.snake_items[i].x = self.snake_items[i - 1].prev_x
            self.snake_items[i].y = self.snake_items[i - 1].prev_y

        # Сохраняем предыдущие координаты головы для следующего шага
        for item in self.snake_items:
            item.prev_x = item.x
            item.prev_y = item.y

        self.repaint()

    def eat_apple(self):
        new_tail = Snake_Item()
        new_tail.x = self.tail.x
        new_tail.y = self.tail.y
        self.snake_items.append(new_tail)
        self.tail = new_tail

    def paintEvent(self, event):
        qp = QPainter(self)
        for item in self.snake_items:
            item.draw_snake(qp)