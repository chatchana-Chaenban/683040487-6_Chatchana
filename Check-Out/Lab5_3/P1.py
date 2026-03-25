"""
chatchana chaenban
683040487-6
P1
"""

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QComboBox, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class StudentGradeCalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Grade Calculator")
        self.setGeometry(100, 100, 825, 625)

        self.setStyleSheet("Background-color: #f2f2f2;")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Student ID : Student Name -> dict
        self.students = {}

        self.input_section()
        self.button()
        self.create_table()
        self.load_f_students()

        self.apply_style()

    def load_f_students(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "students.txt")

            with open(file_path, "r", encoding="utf-8") as file:
                self.id_combobox.setPlaceholderText("Select Student ID")

                for line in file:
                    student_id, name = line.strip().split(",")
                    self.students[student_id] = name
                    self.id_combobox.addItem(student_id)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading file:\n{e}")

    def update_name(self, student_id):
        if student_id in self.students:
            self.name_label.setText(self.students[student_id])
        else:
            self.name_label.setText("")


    def input_section(self):
        name_input_layout = QHBoxLayout()
        self.main_layout.addLayout(name_input_layout)

        name_input_layout.addWidget(QLabel("Student ID:"))
        self.id_combobox = QComboBox()
        self.id_combobox.currentTextChanged.connect(self.update_name)
        name_input_layout.addWidget(self.id_combobox)

        name_input_layout.addWidget(QLabel("Student Name:"))
        self.name_label = QLabel("")
        name_input_layout.addWidget(self.name_label)

        Score_input_layout = QHBoxLayout()
        self.main_layout.addLayout(Score_input_layout)

        Score_input_layout.addWidget(QLabel("Math Score:"))
        self.math_input = QSpinBox()
        self.math_input.setRange(0, 100)
        self.math_input.setValue(0)
        Score_input_layout.addWidget(self.math_input)

        Score_input_layout.addWidget(QLabel("Science Score:"))
        self.sci_input = QSpinBox()
        self.sci_input.setRange(0, 100)
        self.sci_input.setValue(0)
        Score_input_layout.addWidget(self.sci_input,)

        Score_input_layout.addWidget(QLabel("English Score:"))
        self.eng_input = QSpinBox()
        self.eng_input.setRange(0, 100)
        self.eng_input.setValue(0)
        Score_input_layout.addWidget(self.eng_input)

    def clear_table(self):
        self.table.setRowCount(0)

    def reset_inputs(self):
        self.id_combobox.setCurrentIndex(-1)
        self.math_input.clear()
        self.sci_input.clear()
        self.eng_input.clear()

    def calculate_grade(self, avg):
        if avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F"

    def add_student(self):
        try:
            student_id = self.id_combobox.currentText()
            name = self.name_label.text()
            if student_id == "Select Student ID" or not name:
                raise ValueError("Please select a valid student")

            math = float(self.math_input.text())
            sci = float(self.sci_input.text())
            eng = float(self.eng_input.text())

            for score in [math, sci, eng]:
                if score < 0 or score > 100:
                    raise ValueError("Score must be between 0-100")
                
            total = math + sci + eng
            average = total / 3
            grade = self.calculate_grade(average)
            
            self.insert_sort_row(
                student_id, name,
                math, sci, eng,
                total, round(average, 2), grade
            )

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except:
            QMessageBox.warning(self, "Input Error", "Please INPUT the value valid")

        grade_item = QTableWidgetItem(grade)
        grade_item.setTextAlignment(Qt.AlignCenter)

        self.sort_table()

    def button(self):
        btn_layout = QVBoxLayout()
        self.main_layout.addLayout(btn_layout)

        self.add_btn = QPushButton("Add Students")
        self.re_btn = QPushButton("Reset Input")
        self.clear_btn = QPushButton("Clear All")

        self.add_btn.clicked.connect(self.add_student)
        self.re_btn.clicked.connect(self.reset_inputs)
        self.clear_btn.clicked.connect(self.clear_table)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.re_btn)
        btn_layout.addWidget(self.clear_btn)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Student ID", "Name",
            "Math", "Science", "English",
            "Total", "Average", "Grade"
        ])
        self.main_layout.addWidget(self.table)

    def sort_table(self):
        self.table.sortItems(0, Qt.AscendingOrder)

    def insert_sort_row(self, *data):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for column, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            if column in [2, 3, 4]:
                score = float(value)
                if score < 50:
                    item.setBackground(QColor("#f28b82"))

            if column == 7:
                item.setTextAlignment(Qt.AlignCenter)
                
                if value == "A":
                    item.setBackground(QColor("#40d61b"))
                elif value == "B":
                    item.setBackground(QColor("#82d112"))
                elif value == "C":
                    item.setBackground(QColor("#ebd618"))
                elif value == "D":
                    item.setBackground(QColor("#f5820f"))
                elif value == "F":
                    item.setBackground(QColor("#a23030"))

            self.table.setItem(row_position, column, item)

        self.table.sortItems(0, Qt.AscendingOrder)

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6f8;
            }
            QLabel {
                font-size: 14px;
                color: Black;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                padding: 8px;
                background-color: #2ec1e6;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #357ABD
            }
            QTableWidget {
                backgrounf-color: white;
            }
            QMessageBox {
                background-color: white;
                color: black;}
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentGradeCalculatorUI()
    window.show()

    sys.exit(app.exec())