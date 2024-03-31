from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget


class Apple(QWidget):
    def __init__(self):
        super().__init__()
        self.apple_size = 25
        self.x = 100
        self.y = 100

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.x, self.y, self.apple_size, self.apple_size)
