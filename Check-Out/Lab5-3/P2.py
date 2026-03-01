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
    QMessageBox, QSpinBox, QGroupBox
)
from PySide6.QtCharts import (
    QChart, QChartView, QBarSet,
    QBarSeries, QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt

class MonthlySalesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Data Chart")
        self.resize(1100, 600)

        self.sales_data = []

        self.create_ui()

    def create_ui(self):
        main_layout = QHBoxLayout(self)

        left_layout = QVBoxLayout()

        # ---- Import Group ----
        import_group = QGroupBox("Import Data")
        import_layout = QVBoxLayout()

        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("sales_data.txt")

        self.import_btn = QPushButton("Import Data")
        self.import_btn.clicked.connect(self.import_data)

        import_layout.addWidget(self.filename_input)
        import_layout.addWidget(self.import_btn)
        import_group.setLayout(import_layout)

        add_group = QGroupBox("Add Data")
        add_layout = QVBoxLayout()

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

        self.add_btn = QPushButton("+ Add Data")
        self.add_btn.clicked.connect(self.add_data)

        self.clear_btn = QPushButton("✖ Clear Chart")
        self.clear_btn.clicked.connect(self.clear_chart)

        add_layout.addWidget(QLabel("Month"))
        add_layout.addWidget(self.month_combo)
        add_layout.addWidget(QLabel("Sales Amount ($)"))
        add_layout.addWidget(self.sales_input)
        add_layout.addWidget(QLabel("Product Category"))
        add_layout.addWidget(self.category_combo)
        add_layout.addWidget(self.add_btn)
        add_layout.addWidget(self.clear_btn)

        add_group.setLayout(add_layout)

        left_layout.addWidget(import_group)
        left_layout.addWidget(add_group)
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
            QMessageBox.warning(self, "Error", "Enter filename.")
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
        self.update_chart()

    def update_chart(self):
        self.chart.removeAllSeries()

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        categories = ["Electronics", "Clothing", "Food", "Others"]

        colors = {
            "Electronics": QColor("#4A90E2"),
            "Clothing": QColor("#F5A623"),
            "Food": QColor("#7ED321"),
            "Others": QColor("#BD10E0")
        }

        series = QBarSeries()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MonthlySalesApp()
    window.show()
    sys.exit(app.exec())