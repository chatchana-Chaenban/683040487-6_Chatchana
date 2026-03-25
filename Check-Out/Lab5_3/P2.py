"""
Chatchana Chaenban
683040487-6
P2
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QMessageBox, QSpinBox
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt


class MonthlySalesChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Chart")
        self.resize(1000, 600)

        self.sales_data = []

        self.create_ui()


    def create_ui(self):
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter filename (e.g., sales_data.txt)")

        self.import_button = QPushButton("Import Data")
        self.import_button.clicked.connect(self.import_data)

        self.month_combo = QComboBox()
        self.month_combo.addItems(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        )

        self.sales_input = QSpinBox()
        self.sales_input.setRange(0, 1000000)

        self.category_combo = QComboBox()
        self.category_combo.addItems(
            ["Electronics", "Clothing", "Food", "Others"]
        )

        self.add_button = QPushButton("Add Data")
        self.add_button.clicked.connect(self.add_data)

        self.clear_button = QPushButton("Clear Chart")
        self.clear_button.clicked.connect(self.clear_chart)

        left_layout.addWidget(QLabel("Filename"))
        left_layout.addWidget(self.filename_input)
        left_layout.addWidget(self.import_button)

        left_layout.addSpacing(20)

        left_layout.addWidget(QLabel("Month"))
        left_layout.addWidget(self.month_combo)

        left_layout.addWidget(QLabel("Sales Amount"))
        left_layout.addWidget(self.sales_input)

        left_layout.addWidget(QLabel("Product Category"))
        left_layout.addWidget(self.category_combo)

        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.clear_button)
        left_layout.addStretch()

        self.chart = QChart()
        self.chart.setTitle("Monthly Sales by Product Category")

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.chart_view, 3)

    def import_data(self):
        filename = self.filename_input.text()

        if not filename:
            QMessageBox.warning(self, "Error", "Please enter a filename.")
            return

        if not os.path.exists(filename):
            QMessageBox.warning(self, "Error", "File does not exist.")
            return

        self.sales_data.clear()

        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    month, sales, category = parts
                    try:
                        self.sales_data.append(
                            (month, int(sales), category)
                        )
                    except ValueError:
                        continue

        self.update_chart()

    def add_data(self):
        month = self.month_combo.currentText()
        sales = self.sales_input.value()
        category = self.category_combo.currentText()

        self.sales_data.append((month, sales, category))

        self.update_chart()
  
    def clear_chart(self):
        self.sales_data.clear()
        self.chart.removeAllSeries()

    def update_chart(self):
        self.chart.removeAllSeries()

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        categories = ["Electronics", "Clothing", "Food", "Others"]

        colors = {
            "Electronics": QColor("blue"),
            "Clothing": QColor("green"),
            "Food": QColor("red"),
            "Others": QColor("orange")
        }

        series = QBarSeries()
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        for category in categories:
            bar_set = QBarSet(category)
            bar_set.setColor(colors[category])

            for month in months:
                total = sum(
                    sales for m, sales, c in self.sales_data
                    if m == month and c == category
                )
                bar_set.append(total)

            series.append(bar_set)

        self.chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(months)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Sales Amount")
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)


# ================= MAIN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MonthlySalesChart()
    window.show()
    sys.exit(app.exec())