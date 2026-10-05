import os

# Находим путь к установленной библиотеке PyQt5
import PyQt5
pyqt_path = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(pyqt_path, "Qt5", "plugins", "platforms")

# Если папки Qt5 нет, проверяем прямую папку plugins
if not os.path.exists(plugin_path):
    plugin_path = os.path.join(pyqt_path, "Qt", "plugins", "platforms")

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path