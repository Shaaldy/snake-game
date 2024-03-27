import sys

from PyQt6.QtWidgets import QApplication

from Game import Game

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    app.exec()
