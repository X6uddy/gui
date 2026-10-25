import os
from pathlib import Path

import PyQt5
from PyQt5.QtCore import QCoreApplication


def _qt_subdir(name: str) -> Path:
    """Папка внутри пакета PyQt5: Qt5/<name>, а если такой структуры нет — Qt/<name>"""

    pyqt_dir = Path(PyQt5.__file__).parent
    path = pyqt_dir / "Qt5" / name
    return path if path.exists() else pyqt_dir / "Qt" / name


def setup_qt_paths():
    """Указывает Qt пути к плагинам и QML-модулям.

    Нужно вызвать ДО создания QApplication. Лечит ошибки вида
    «Driver not found» (lab3) и «could not find the Qt platform plugin» (lab1, lab4).
    """

    plugins_dir = _qt_subdir("plugins")

    os.environ["QT_PLUGIN_PATH"] = str(plugins_dir)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(plugins_dir / "platforms")
    os.environ["QML2_IMPORT_PATH"] = str(_qt_subdir("qml"))
    QCoreApplication.addLibraryPath(str(plugins_dir))
