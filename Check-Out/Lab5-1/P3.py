"""
Chatchana Chaenban
683040487-6
P3
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class BMIcal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setFixedSize(350, 620)
        self.setStyleSheet("""
            QWidget {
                background-color: #eeeeee;
                color: #333;
                font-family: Arial;
                font-size: 13px;
            }

            QLineEdit, QComboBox {
                background-color: #f5f5f5;
                border: 1px solid #bbb;
                border-radius: 4px;
                padding: 4px;
            }

            QPushButton {
                background-color: #e6e6e6;
                border: 1px solid #bbb;
                border-radius: 4px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #dcdcdc;
            }
        """)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)

        # Outer container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #f7f7f7;
                border: 1px solid #bbb;
                border-radius: 8px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)
        container_layout.setContentsMargins(12, 12, 12, 12)

        headline = QLabel("Adult and Child BMI calculator")
        headline.setAlignment(Qt.AlignCenter)
        headline.setFixedHeight(45)
        headline.setStyleSheet("""
            background-color: #b84a3a;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 4px;
        """)
        container_layout.addWidget(headline)

        form = QGridLayout()
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(8)

        form.addWidget(QLabel("Calculate BMI for"), 0, 0)

        self.age_box = QComboBox()
        self.age_box.addItems(["Adult Age 20+"])
        form.addWidget(self.age_box, 0, 1, 1, 2)

        form.addWidget(QLabel("Weight:"), 1, 0)
        weight = QLineEdit()
        weight.setFixedWidth(80)
        form.addWidget(weight, 1, 1)
        weight_unit = QComboBox()
        weight_unit.addItems(["pounds"])
        form.addWidget(weight_unit, 1, 2)

        form.addWidget(QLabel("Height:"), 2, 0)
        feet = QLineEdit()
        feet.setFixedWidth(80)
        form.addWidget(feet, 2, 1)

        height_unit = QComboBox()
        height_unit.addItems(["feet"])
        form.addWidget(height_unit, 2, 2)

        inches = QLineEdit()
        inches.setFixedWidth(80)
        form.addWidget(inches, 3, 1)
        inches_label = QLabel("inches")
        form.addWidget(inches_label, 3, 2)

        container_layout.addLayout(form)

        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        calc_btn = QPushButton("Calculate")

        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(calc_btn)

        container_layout.addLayout(btn_layout)

        answer_frame = QFrame()
        answer_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #bbb;
                border-radius: 6px;
                background-color: #f9f9f9;
            }
        """)
        answer_layout = QVBoxLayout(answer_frame)
        answer_layout.setContentsMargins(10, 10, 10, 10)

        answer_layout.addWidget(QLabel("Answer:"))

        result = QLabel("BMI = ")
        result.setAlignment(Qt.AlignCenter)
        result.setFont(QFont("Arial", 11, QFont.Bold))
        answer_layout.addWidget(result)

        adult_label = QLabel("Adult BMI")
        adult_label.setAlignment(Qt.AlignCenter)
        adult_label.setFont(QFont("Arial", 10, QFont.Bold))
        answer_layout.addWidget(adult_label)

        table = QGridLayout()
        table.setSpacing(0)

        table.addWidget(self.table_cell("BMI", header=True), 0, 0)
        table.addWidget(self.table_cell("Status", header=True), 0, 1)

        table.addWidget(self.table_cell("<= 18.4", "#ffe082"), 1, 0)
        table.addWidget(self.table_cell("Underweight"), 1, 1)

        table.addWidget(self.table_cell("18.5 - 24.9", "#aed581"), 2, 0)
        table.addWidget(self.table_cell("Normal"), 2, 1)

        table.addWidget(self.table_cell("25.0 - 39.9", "#ffb74d"), 3 ,0)
        table.addWidget(self.table_cell("Overweight"), 3, 1)

        table.addWidget(self.table_cell(">= 40.0", "#ef5350"), 4, 0)
        table.addWidget(self.table_cell("Obese"), 4, 1)

        answer_layout.addLayout(table)
        container_layout.addWidget(answer_frame)
        main_layout.addWidget(container)

    def table_cell(self, text, color=None, header=False):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)

        if header:
            lbl.setStyleSheet("""
            background-color: #d0d0d0;
            border: 1px solid #b5b5b5;
            padding: 6px;
            font-weight: bold;
        """)
        else:
            lbl.setStyleSheet(f"""
            background-color: {color if color else '#ffffff'};
            border: 1px solid #c9c9c9;
            padding: 6px;
        """)

        return lbl
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    window = BMIcal()
    window.show()
    sys.exit(app.exec())