from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, \
    QDesktopWidget, QFrame
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QBasicTimer
import sys

from PyQt5 import QtCore, QtWidgets, QtGui


class SnakeGame(QMainWindow):
    def __init__(self):
        super(SnakeGame, self).__init__()
        self.sboard = Board(self)

        self.statusbar = self.statusBar()
        self.sboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.setCentralWidget(self.sboard)
        self.setWindowTitle('PyQt5 Snake game')
        self.resize(600, 400)
        self.show()


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.board = []
        self.direction = 1
        self.setFocusPolicy(Qt.StrongFocus)


def main():
    app = QApplication(sys.argv)
    ui = SnakeGame()  # Создаем экземпляр игры
    ui.show()  # Показываем окно игры
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
