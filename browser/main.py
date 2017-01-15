# coding utf-8

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys

class Browser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()

    def initUi(self):
        loadUi('main_window.ui', self)
        self.statusBar().showMessage('Приложение запущено')

    def initSignals(self):
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)

    browser = Browser()
    browser.show()

    sys.exit(app.exec_())
