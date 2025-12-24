from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QPushButton
from db import DBManager
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Склад")
        self.setGeometry(100, 100, 800, 600)
        self.db = DBManager()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.free_slots_label = QLabel()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Стеллаж", "Заполнение (%)", "Допустимая масса"])

        btn_update = QPushButton("Обновить данные")
        btn_update.clicked.connect(self.load_data)

        layout.addWidget(self.free_slots_label)
        layout.addWidget(self.table)
        layout.addWidget(btn_update)

        self.load_data()

# Флаги для отладки модуля UI (запускать в режиме debug - жучок около кнопки плей сверху зеленое ЗАПУСКАТЬ МЕЙН НЕ ЭТОТ ФАЙЛ)
    def load_data(self):
        try:
            free = self.db.get_free_slots()
            self.free_slots_label.setText(f"Свободных ячеек: {free}")
            print(f"Загружено: {free} свободных ячеек")

            stats = self.db.get_rack_stats()
            self.table.setRowCount(len(stats))
            for i, (num, fill, weight) in enumerate(stats):
                self.table.setItem(i, 0, QTableWidgetItem(str(num)))
                self.table.setItem(i, 1, QTableWidgetItem(str(fill)))
                self.table.setItem(i, 2, QTableWidgetItem(str(weight)))
            print("Статистика по стеллажам обновлена")
        except Exception as e:
            self.free_slots_label.setText(f"Ошибка: {str(e)}")
            print("Не удалось обновить данные")