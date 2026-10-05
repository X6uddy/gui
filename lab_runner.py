import sys
from PyQt5.QtWidgets import QApplication

from lab1.main_molule import ImageApp
from lab2.currency_converter import CurrencyConverter


class LabRunner():
    def __init__(self):
        pass

    def start_1_lab(self):
        app = QApplication(sys.argv)
        ex = ImageApp()
        ex.show()
        sys.exit(app.exec_())


    def start_2_lab(self):
        app = QApplication(sys.argv)
        window = CurrencyConverter()
        window.show()
        sys.exit(app.exec_())