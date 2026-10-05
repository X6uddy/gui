from pathlib import Path

from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


IMAGE_PATH = Path(__file__).parent / "nature.jpeg"
IMAGE_SIZE = 300

class ImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        """Настройка главного виджета по умолчанию"""

        # настройка параметров окна
        self.setWindowTitle("Лаб 1 | Замена надписи на изображение")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()  # создаём вертикальный слой

        # создаём надпись с текстом
        self.label = QLabel("Здесь будет изображение!", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # создаём кнопку
        self.btn = QPushButton("Показать картинку", self)
        # подключаем событие нажатие кнопки
        self.btn.clicked.connect(self.__change_to_image_btn_click)
        layout.addWidget(self.btn)

        self.setLayout(layout)


    def __change_to_image_btn_click(self):

        pixmap = QPixmap(str(IMAGE_PATH))

        if pixmap.isNull():
            self.label.setText(f"Ошибка: не удалось загрузить {IMAGE_PATH.name}")
            return

        self.label.setPixmap(pixmap.scaled(
            IMAGE_SIZE, IMAGE_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ))
