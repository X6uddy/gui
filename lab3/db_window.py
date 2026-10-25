from functools import partial

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableView, QFileDialog, QAction, QComboBox, 
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery


# индексы вкладок QTabWidget
TAB_SCHEMA, TAB_OBJECTS, TAB_TABLE, TAB_TABLES_SQL, TAB_OTHER_SQL = range(5)

# SQL-запросы, привязанные к кнопкам
QUERY_ALL_SCHEMA = "SELECT * FROM sqlite_master"
QUERY_OBJECTS = "SELECT type, name, tbl_name FROM sqlite_master"
QUERY_TABLES_SQL = "SELECT type, name, sql FROM sqlite_master WHERE type='table'"
QUERY_OTHER_SQL = "SELECT type, name, sql FROM sqlite_master WHERE type IN ('index', 'trigger', 'view')"
QUERY_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table'"


class DbWindow(QMainWindow):
    def __init__(self):

        super().__init__()

        self.setWindowTitle("Лабораторная работа № 3")
        self.setGeometry(100, 100, 900, 600)

        self.db = None
        self.is_connected = False

        self.init_ui()

    def init_ui(self):
        #Меню приложения
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Соединение")

        act_connect = QAction("Set connection", self)
        act_connect.triggered.connect(self.set_connection)
        file_menu.addAction(act_connect)

        act_close = QAction("Close connection", self)
        act_close.triggered.connect(self.close_connection)
        file_menu.addAction(act_close)

        # Центральный виджет и компоновка
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Панель управления (Кнопки и QComboBox)
        control_layout = QHBoxLayout()

        self.btn_bt1 = QPushButton("bt1 (Имена таблиц)")
        self.btn_bt1.clicked.connect(partial(self.show_query_in_tab, QUERY_OBJECTS, TAB_OBJECTS))
        control_layout.addWidget(self.btn_bt1)

        control_layout.addWidget(QLabel("Выбор таблицы:"))
        self.combo_tables = QComboBox()
        self.combo_tables.currentIndexChanged.connect(self.on_combo_changed)
        control_layout.addWidget(self.combo_tables)

        self.btn_bt2 = QPushButton("bt2 (Запрос Tab4)")
        self.btn_bt2.clicked.connect(partial(self.show_query_in_tab, QUERY_TABLES_SQL, TAB_TABLES_SQL))
        control_layout.addWidget(self.btn_bt2)

        self.btn_bt3 = QPushButton("bt3 (Запрос Tab5)")
        self.btn_bt3.clicked.connect(partial(self.show_query_in_tab, QUERY_OTHER_SQL, TAB_OTHER_SQL))
        control_layout.addWidget(self.btn_bt3)

        main_layout.addLayout(control_layout)

        # Вкладки (QTabWidget)
        self.tabs = QTabWidget()
        self.tab_views = []

        # Создаем 5 вкладок с QTableView
        for i in range(1, 6):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            table_view = QTableView()
            tab_layout.addWidget(table_view)
            self.tabs.addTab(tab, f"Tab {i}")
            self.tab_views.append(table_view)

        main_layout.addWidget(self.tabs)

        # Блокируем кнопки до подключения
        self.set_controls_enabled(False)

    def set_controls_enabled(self, state: bool):
        """Включение/выключение кнопок управления"""
        for widget in (self.btn_bt1, self.btn_bt2, self.btn_bt3, self.combo_tables):
            widget.setEnabled(state)

    def execute_query_to_tab(self, query_str: str, tab_index: int):
        """Выполняет SQL-запрос и выводит результат в указанную вкладку"""
        if not self.is_connected:
            return

        model = QSqlQueryModel()
        model.setQuery(query_str, self.db)

        if model.lastError().isValid():
            QMessageBox.warning(self, "Ошибка БД", f"Ошибка выполнения запроса:\n{model.lastError().text()}")
            return

        self.tab_views[tab_index].setModel(model)
        self.tab_views[tab_index].resizeColumnsToContents()

    def set_connection(self):
        """Открытие диалогового окна и подключение к SQLite БД"""
        db_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл базы данных SQLite", "", "SQLite Databases (*.db *.sqlite *.sqlite3);;All Files (*)"
        )

        if not db_path:
            return

        # Если было старое подключение — закрываем
        if self.is_connected:
            self.close_connection(notify=False)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)

        if not self.db.open():
            error_text = self.db.lastError().text()
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к базе данных!\n{error_text}")
            return

        self.is_connected = True
        self.set_controls_enabled(True)

        # Запрос в Tab1: SELECT * FROM sqlite_master
        self.execute_query_to_tab(QUERY_ALL_SCHEMA, TAB_SCHEMA)

        # Заполняем QComboBox именами таблиц
        self.load_table_names()

        QMessageBox.information(self, "Успех", "Соединение с БД успешно установлено!")

    def load_table_names(self):
        """Загрузка списка таблиц базы данных в QComboBox"""
        self.combo_tables.blockSignals(True)
        self.combo_tables.clear()

        query = QSqlQuery(QUERY_TABLE_NAMES, self.db)
        while query.next():
            self.combo_tables.addItem(query.value(0))

        self.combo_tables.blockSignals(False)

        # Если таблицы есть, загружаем первую в Tab3
        if self.combo_tables.count() > 0:
            self.on_combo_changed(0)

    def close_connection(self, notify=True):
        """Очистка отображения и закрытие соединения с БД"""
        # Очищаем модели во всех вкладках
        for view in self.tab_views:
            view.setModel(None)

        self.combo_tables.blockSignals(True)
        self.combo_tables.clear()
        self.combo_tables.blockSignals(False)

        if self.is_connected:
            connection_name = self.db.connectionName()
            self.db.close()
            self.db = None
            QSqlDatabase.removeDatabase(connection_name)
            self.is_connected = False

        self.set_controls_enabled(False)
        if notify:
            QMessageBox.information(self, "Соединение", "Соединение с БД закрыто, интерфейс очищен.")

    # --- Обработчики сигналов ---

    def show_query_in_tab(self, query_str: str, tab_index: int):
        """Запрос по кнопке: результат выводится во вкладку, и она становится активной"""
        self.execute_query_to_tab(query_str, tab_index)
        self.tabs.setCurrentIndex(tab_index)

    def on_combo_changed(self, index):
        """Обработка выбора элемента из QComboBox (Запрос в Tab3)"""
        table_name = self.combo_tables.currentText()
        if table_name:
            self.execute_query_to_tab(f'SELECT * FROM "{table_name}"', TAB_TABLE)
