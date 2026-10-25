from pathlib import Path

from PyQt5.QtCore import QObject, QTimer, QMetaObject, Q_ARG, pyqtSlot, QVariant
from PyQt5.QtQml import QQmlApplicationEngine


# пути строятся от расположения файла, поэтому не зависят от папки запуска
LAB_DIR = Path(__file__).parent
QML_PATH = LAB_DIR / "resources" / "template" / "mainWindow.qml"
SAVE_PATH = LAB_DIR / "saved_canvas.png"

AUTOSAVE_INTERVAL_MS = 5000


class Interface(QObject):
    def __init__(self, engine=None):

        super().__init__()
        self.engine = engine if engine else QQmlApplicationEngine()

        # создаем таймер для автосохранения
        self.timer = QTimer(self)
        self.timer.setInterval(AUTOSAVE_INTERVAL_MS)
        self.timer.timeout.connect(self.autosave)
        self.timer.start()


    @pyqtSlot()
    def autosave(self):
        """Слот, вызываемый по таймеру для автосохранения canvas"""

        root_objects = self.engine.rootObjects()
        if not root_objects:
            print("Ошибка: Не удалось получить корневой объект QML!")
            return

        # находим объект canvas по objectName из QML
        canvas = root_objects[0].findChild(QObject, "canvas")
        if not canvas:
            print("Ошибка: Не удалось найти объект canvas в QML!")
            return

        # вызываем JS-функцию saveCanvas(filePath), объявленную в QML
        QMetaObject.invokeMethod(canvas, "saveCanvas", Q_ARG(QVariant, str(SAVE_PATH)))
        print(f"[Backend] автосохранение выполнено: {SAVE_PATH}")
