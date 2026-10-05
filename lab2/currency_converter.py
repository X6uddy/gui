from functools import partial

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit
)
from PyQt5.QtGui import QDoubleValidator


RATES = {
    "USD": 1.0,
    "RUB": 90.0,
    "EUR": 0.92,
}

# подписи у полей ввода
LABELS = {
    "USD": "USD:",
    "RUB": "RUB:",
    "EUR": "EUR (€):",
}


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.inputs: dict[str, QLineEdit] = {}

        self.initUI()


    def initUI(self):

        self.setWindowTitle("Лаб 2 | Конвертер валют")
        self.setGeometry(100, 100, 350, 200)

        main_layout = QVBoxLayout()

        validator = QDoubleValidator(0.0, 10000000.0, 2, self)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        for code in RATES:
            line_edit = QLineEdit()
            line_edit.setValidator(validator)
            line_edit.setPlaceholderText('0.00')
            line_edit.textChanged.connect(partial(self.on_changed, code))
            self.inputs[code] = line_edit

            row = QHBoxLayout()
            row.addWidget(QLabel(LABELS[code]))
            row.addWidget(line_edit)
            main_layout.addLayout(row)

        self.setLayout(main_layout)


    def parse_value(self, text : str):
        """Вспомогательный метод для безопасной конвертации текста в float"""

        text = text.replace(',', '.')
        try:
            return float(text)
        except ValueError:
            return 0.0


    def on_changed(self, source : str, text : str):
        """Общий обработчик: пересчитывает все поля, кроме изменённого (source)"""

        if not text:
            self.clear_other_fields(except_code=source)
            return

        # переводим введённое значение в USD, а затем в каждую из остальных валют
        usd_val = self.parse_value(text) / RATES[source]

        for code, field in self.inputs.items():
            if code != source:
                field.blockSignals(True)
                field.setText(f"{usd_val * RATES[code]:.2f}")
                field.blockSignals(False)


    def clear_other_fields(self, except_code : str):
        """Очистка остальных полей, если текущее поле пустое"""

        for code, field in self.inputs.items():
            if code != except_code:
                field.blockSignals(True)
                field.clear()
                field.blockSignals(False)
