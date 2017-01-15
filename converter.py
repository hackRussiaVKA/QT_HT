import sys
from lxml import etree
import requests
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QDoubleSpinBox,
    QVBoxLayout
)

class Course(QObject):
    def get(self):
        page = requests.get('http://www.cbr.ru/scripts/RssCurrency.asp')
        text = page.content
        tree = etree.XML(text)
        raws = tree.xpath('//item')
        for raw in raws:
            courses = raw.xpath('description')[0].text
        for i, ch in enumerate(courses):
            if i == 301:
                dollar = ch
            if i == 302:
                dollar = dollar + ch
        return int(dollar)


class Converter(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
        self.initLayouts()
        self.initSignals()

    def initUi(self):
        self.setWindowTitle('Конвертер валют')
        self.srcLabel = QLabel('Сумма в рублях', self)
        self.resultLabel = QLabel('Сумма в долларах', self)
        self.srcAmount = QDoubleSpinBox(self)
        self.srcAmount.setMaximum(999999999)
        self.resultAmount = QDoubleSpinBox(self)
        self.resultAmount.setMaximum(999999999)
        self.convertBtn = QPushButton('Перевести', self)
        self.clearBtn = QPushButton('Очистить', self)

    def initSignals(self):
        self.convertBtn.clicked.connect(self.onConvertClick)
        self.clearBtn.clicked.connect(self.onClearClick)

    def initLayouts(self):
        self.w = QWidget()
        self.mainLayout = QVBoxLayout(self.w)
        self.mainLayout.addWidget(self.srcLabel)
        self.mainLayout.addWidget(self.srcAmount)
        self.mainLayout.addWidget(self.resultLabel)
        self.mainLayout.addWidget(self.resultAmount)
        self.mainLayout.addWidget(self.convertBtn)
        self.mainLayout.addWidget(self.clearBtn)
        self.setCentralWidget(self.w)

    def onConvertClick(self):
        value_1 = self.srcAmount.value()
        value_2 = self.resultAmount.value()

        if value_1:
            self.resultAmount.setValue(value_1 / Course().get())
        elif value_2:
            self.srcAmount.setValue(value_2 * Course().get())
        self.convertBtn.setEnabled(False)

    def onClearClick(self):
        self.srcAmmount.setValue(0)
        self.resultAmmount.setValue(0)
        self.convertBtn.setEnabled(True)

    def keyEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.onConvertClick()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    converter = Converter()
    converter.show()

    sys.exit(app.exec_())