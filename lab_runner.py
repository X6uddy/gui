import sys

import qt_setup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl

from lab1.main_molule import ImageApp
from lab2.currency_converter import CurrencyConverter
from lab3.db_helper import Dbhelper
from lab3.db_window import DbWindow
from lab4.interface import Interface, QML_PATH


class LabRunner():
    def __init__(self):
        # пути к плагинам Qt нужно задать до создания QApplication
        qt_setup.setup_qt_paths()

    def start_widget_lab(self, window_class):
        """Общий запуск для лабораторных на QWidget: приложение -> окно -> цикл событий"""
        app = QApplication(sys.argv)
        window = window_class()
        window.show()
        sys.exit(app.exec_())


    def start_1_lab(self):
        self.start_widget_lab(ImageApp)


    def start_2_lab(self):
        self.start_widget_lab(CurrencyConverter)


    def start_3_lab(self):
        Dbhelper.create_test_db()   # пересоздаём тестовую БД, которую потом выбираем в диалоге
        self.start_widget_lab(DbWindow)


    def start_4_lab(self):
        app = QApplication(sys.argv)

        engine = QQmlApplicationEngine()
        interface = Interface(engine)   # хранит таймер автосохранения, ссылку держим до конца работы
        engine.rootContext().setContextProperty("_backend", interface)
        engine.load(QUrl.fromLocalFile(str(QML_PATH)))

        if not engine.rootObjects():
            print("Ошибка: Не удалось загрузить QML файл!")
            sys.exit(-1)

        sys.exit(app.exec_())
