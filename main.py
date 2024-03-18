from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Snake")
        self.setGeometry(400, 400, 520, 520)

        self.initUI()
        self.initSnake()
        self.initGame()

    def initUI(self):
        layout = QHBoxLayout()  # Вертикальный макет для размещения элементов

        self.tableWidget = QTableWidget()
        COUNT = 15
        self.tableWidget.setRowCount(COUNT)
        self.tableWidget.setColumnCount(COUNT)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        for i in range(COUNT):
            self.tableWidget.setColumnWidth(i, 5)
            self.tableWidget.setRowHeight(i, 5)
            for j in range(COUNT):
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if (i + j) % 2 == 0:
                    item.setBackground(QColor("#90EE90"))
                else:
                    item.setBackground(QColor("#6B8E23"))

                self.tableWidget.setItem(i, j, item)

        layout.addWidget(self.tableWidget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def initSnake(self):
        self.snake = [(0, 0)]
        self.direction = 'right'
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.moveSnake)

    def initGame(self):
        self.timer.start(1000)
        self.setFocusPolicy(Qt.StrongFocus)

    def moveSnake(self):
        head_x, head_y = self.snake[0]

        if self.direction == 'up':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'down':
            new_head = (head_x + 1, head_y)
        elif self.direction == 'left':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'right':
            new_head = (head_x, head_y + 1)

        self.snake.insert(0, new_head)

        tail_x, tail_y = self.snake[-1]
        self.tableWidget.takeItem(tail_x, tail_y)

        self.updateSnake()

    def updateSnake(self):
        head_x, head_y = self.snake[0]
        item = QTableWidgetItem()
        item.setBackground(Qt.darkBlue)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.tableWidget.setItem(head_x, head_y, item)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W and self.direction != 'down':
            self.direction = 'up'
        elif key == Qt.Key_S and self.direction != 'up':
            self.direction = 'down'
        elif key == Qt.Key_A and self.direction != 'right':
            self.direction = 'left'
        elif key == Qt.Key_D and self.direction != 'left':
            self.direction = 'right'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

