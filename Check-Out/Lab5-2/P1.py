"""
Chatchana Chaenban
683040487-6
P1
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QFormLayout,
                             QGridLayout, QWidget, QLabel, QLineEdit,
                             QPushButton, QComboBox, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class BMIcalcMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 400, 600)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.input_section = InputSection()
        self.output_section = OutputSection()

        result_container = QWidget()
        result_container.setStyleSheet("background-color: #FAF0E6;")
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.output_section)
        result_container.setLayout(result_layout)

        main_layout.addWidget(self.input_section)
        main_layout.addWidget(result_container)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.input_section.submit_btn.clicked.connect(
            lambda: self.input_section.submit_reg(self.output_section)
        )
        self.input_section.clear_btn.clicked.connect(
            lambda: self.input_section.clear_form(self.output_section)
        )

class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.title = QLabel("Your BMI")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: black; font-size: 14px;")

        self.bmi_value = QLabel("0.00")
        self.bmi_value.setAlignment(Qt.AlignCenter)
        self.bmi_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.bmi_value.setStyleSheet("color: blue;")

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.bmi_value)

    def update_results(self, bmi, age_group):
        self.clear_result()
        self.bmi_value.setText(f"{bmi:.2f}")

        if age_group == adult:
            self.show_adult_table()
        else:
            self.show_child_links()

    def show_adult_table(self):
        table_layout = QGridLayout()
        table_layout.setVerticalSpacing(8)
        table_layout.setHorizontalSpacing(50)

        header_font = QFont("Arial", 11, QFont.Bold)

        bmi_header = QLabel("BMI")
        condition_header = QLabel("Condition")

        bmi_header.setFont(header_font)
        condition_header.setFont(header_font)

        bmi_header.setStyleSheet("color: black;")
        condition_header.setStyleSheet("color: black;")

        table_layout.addWidget(bmi_header, 0, 0, alignment=Qt.AlignCenter)
        table_layout.addWidget(condition_header, 0, 1, alignment=Qt.AlignCenter)

        data_font = QFont("Arial", 10)

        data = [
            ["< 18.5", "Thin"],
            ["18.5 - 25.0", "Normal"],
            ["25.1 - 30.0", "Overweight"],
            ["> 30.0", "Obese"]
    ]
        for row, (bmi_range, condition) in enumerate(data, start=1):
            bmi_label = QLabel(bmi_range)
            condition_label = QLabel(condition)

            bmi_label.setFont(data_font)
            condition_label.setFont(data_font)

            bmi_label.setStyleSheet("color: black;")
            condition_label.setStyleSheet("color: black;")

            table_layout.addWidget(bmi_label, row, 0, alignment=Qt.AlignCenter)
            table_layout.addWidget(condition_label, row, 1, alignment=Qt.AlignCenter)

            wrapper = QHBoxLayout()
            wrapper.addStretch()
            wrapper.addLayout(table_layout)
            wrapper.addStretch()

            self.layout.addSpacing(15)
            self.layout.addLayout(wrapper)

    def show_child_links(self):
        info = QLabel(
            "For child's BMI interpretation, please click one of the following links."
        )
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: black; font-size: 10px;")

        link_label = QLabel(
            '<a href="https://www.who.int">BMI graph for BOYS</a>    '
            '<a href="https://www.who.int">BMI graph for GIRLS</a>'
        )
        link_label.setAlignment(Qt.AlignCenter)
        link_label.setOpenExternalLinks(True)
        link_label.setStyleSheet("""
            QLabel {
                color: #2F5BFF;
                font-size: 11px;
            }
            QLabel:hover {
                text-decoration: underline;
            }
        """)

        self.layout.addSpacing(15)
        self.layout.addWidget(info)
        self.layout.addSpacing(5)
        self.layout.addWidget(link_label)

    def clear_result(self):
        self.bmi_value.setText("0.00")

        while self.layout.count() > 2:
            item = self.layout.takeAt(2)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())


class InputSection(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Adult and Child BMI Calculator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            background-color:#b22222;
            color:white;
            padding:8px;
            font-weight:bold;
        """)
        title.setFixedHeight(28) 
        main_layout.addWidget(title)

        grid = QGridLayout()
        grid.setVerticalSpacing(12)
        grid.setHorizontalSpacing(10)

        age_label = QLabel("BMI age group:")
        self.age_combo = QComboBox()
        self.age_combo.addItems([adult, child])

        grid.addWidget(age_label, 0, 0)
        grid.addWidget(self.age_combo, 0, 1, 1, 2)

        weight_label = QLabel("Weight:")
        self.weight_input = QLineEdit()
        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])

        grid.addWidget(weight_label, 1, 0)
        grid.addWidget(self.weight_input, 1, 1)
        grid.addWidget(self.weight_unit, 1, 2)

        height_label = QLabel("Height:")
        self.height_input = QLineEdit()
        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, ft])

        grid.addWidget(height_label, 2, 0)
        grid.addWidget(self.height_input, 2, 1)
        grid.addWidget(self.height_unit, 2, 2)

        main_layout.addLayout(grid)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.clear_btn = QPushButton("clear")
        self.submit_btn = QPushButton("Submit Registration")

        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.submit_btn)

        main_layout.addSpacing(15)
        main_layout.addLayout(button_layout)

    def clear_form(self, output_section):
        self.weight_input.clear()
        self.height_input.clear()
        output_section.clear_result()

    def submit_reg(self, output_section):
        bmi = self.calculate_BMI()
        if bmi is not None:
            output_section.update_results(bmi, self.age_combo.currentText())

    def calculate_BMI(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")

            if self.weight_unit.currentText() == lb:
                weight *= 0.453592

            if self.height_unit.currentText() == cm:
                height /= 100
            else:
                height *= 0.3048

            bmi = weight / (height ** 2)
            return bmi

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
            return None

        except:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values.")
            return None


def main():
    app = QApplication(sys.argv)
    window = BMIcalcMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()