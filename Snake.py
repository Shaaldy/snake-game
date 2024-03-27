from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget


class Snake(QWidget):
    def __init__(self):
        super().__init__()
        self.snake_size = 20
        self._x = 0
        self._y = 0
        self.direction = 'Right'
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_snake)
        self.timer.start(100)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def paintEvent(self, event):
        qp = QPainter(self)
        self.draw_snake(qp)

    def draw_snake(self, qp):
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(self.x, self.y, self.snake_size, self.snake_size)

    def move_snake(self):
        if self.direction == 'Right':
            self._x += self.snake_size
            if self._x >= self.parent().width():
                self._x = 0
        elif self.direction == 'Left':
            self._x -= self.snake_size
            if self._x < 0:
                self._x = self.parent().width() - self.snake_size
        elif self.direction == 'Up':
            self._y -= self.snake_size
            if self._y < 0:
                self._y = self.parent().height() - self.snake_size
        elif self.direction == 'Down':
            self._y += self.snake_size
            if self._y >= self.parent().height():
                self._y = 0

        self.repaint()
