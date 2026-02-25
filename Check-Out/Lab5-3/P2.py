"""
Chatchana Chaenban
683040487-6
P2
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton,
    QMessageBox
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSet,
    QBarSeries, QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class SaleChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Chart")
        self.resize(900, 600)

        self.sales_data = {}

        self.months = ["Jan", "Feb", "Mar", "Apr", "May",
                    "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        self.categories = ["Electronics", "Clothing", "Food", "Others"]

        self.InitUI()

    def InitUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Input file fields
        input_layout = QHBoxLayout()

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter Filename")
        input_layout.addWidget(QLabel("Filename:"))
        input_layout.addWidget(self.filename_input)

        self.month_combo = QComboBox()
        self.month_combo.addItems(self.months)
        input_layout.addWidget(QLabel("Month:"))
        input_layout.addWidget(self.month_combo)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter sales amount")
        input_layout.addWidget(QLabel("Amount"))
        input_layout.addWidget(self.amount_input)

        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        input_layout.addWidget(QLabel("Categories:"))
        input_layout.addWidget(self.category_combo)

        main_layout.addLayout(input_layout)

        # Buttons fields
        button_layout = QHBoxLayout()

        self.import_btn = QPushButton("Import Data")
        self.import_btn.clicked.connect(self.import_data)
        button_layout.addWidget(self.import_btn)

        self.add_btn = QPushButton("Add Data")
        self.add_btn.clicked.connect(self.add_data)

        self.clear_btn = QPushButton("Clear Chart")
        self.clear_btn.clicked.connect(self.clear_chart)

        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.clear_btn)

        main_layout.addLayout(button_layout)


        self.chart = QChart()
        self.chart.setTitle("Monthly Sales Report")

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        main_layout.addWidget(self.chart_view)

        central_widget.setLayout(main_layout)

        self.update_chart()

    def import_data(self):
        filename = self.filename_input.text()

        if not os.path.exists(filename):
            QMessageBox.warning(self, "Error", "File does not exist!")
            return

        try:
            with open(filename, "r") as file:
                self.sales_data.clear()
                for line in file:
                    month, category, amount = line.strip().split(",")
                    self.sales_data[(month, category)] = float(amount)

            QMessageBox.information(self, "Success", "Data imported successfully!")
            self.update_chart()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid file format!\n{e}")

    def add_data(self):
        month = self.month_combo.currentText()
        category = self.category_combo.currentText()
        amount_text = self.amount_input.text()

        if not amount_text.isdigit():
            QMessageBox.warning(self, "Error", "Sales amount must be a number!")
            return

        amount = float(amount_text)

        self.sales_data[(month, category)] = amount

        # Save to file if filename provided
        filename = self.filename_input.text()
        if filename:
            with open(filename, "a") as file:
                file.write(f"{month},{category},{amount}\n")

        self.update_chart()

    def clear_chart(self):
        self.sales_data.clear()
        self.update_chart()

    def update_chart(self):
        self.chart.removeAllSeries()

        series = QBarSeries()

        for category in self.categories:
            bar_set = QBarSet(category)

            for month in self.months:
                value = self.sales_data.get((month, category), 0)
                bar_set.append(value)

            series.append(bar_set)

        self.chart.addSeries(series)

        # X-axis 
        axis_x = QBarCategoryAxis()
        axis_x.append(self.months)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Y-axis 
        axis_y = QValueAxis()
        axis_y.setTitleText("Sales Amount")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart.setTitle("Monthly Sales Report")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SaleChart()
    window.show()
    sys.exit(app.exec())