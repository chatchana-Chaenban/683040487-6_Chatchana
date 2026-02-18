"""
Chatchana Chaenban
683040487-6
P2
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QWidget, QGridLayout,
                             QPushButton, QLineEdit, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import math

class CalculatorUILayout(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        title = QLabel("Standard")
        title.setStyleSheet("color: black;")
        title.setFont(QFont("Segoe UI", 12))
        main_layout.addWidget(title)

        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Segoe UI", 32))
        self.display.setReadOnly(True)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet("""
            QLineEdit {
                background: white;
                border: none;
                padding: 10px;
                color: black;
            }
        """)
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        grid.setSpacing(8)
        main_layout.addLayout(grid)

        buttons = [
            ["%", "CE", "C", "<-"],
            ["1/x", "x^2", "sqrt(x)", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="],
        ]

        for row, row_values in enumerate(buttons):
            for col, text in enumerate(row_values):
                button = QPushButton(text)
                button.setFixedSize(70, 55)
                button.setFont(QFont("Segoe UI", 11))
                button.clicked.connect(self.handle_button)

                if text in ["+", "-", "*", "/", "="]:
                    button.setStyleSheet(self.operator_style())
                elif text in ["C", "CE", "<-"]:
                    button.setStyleSheet(self.clear_style())
                else:
                    button.setStyleSheet(self.normal_style())

                grid.addWidget(button, row, col)

    def normal_style(self):
        return """
        QPushButton {
            background-color: #ffffff;
            border-radius: 8px;
            color: black;
        }
        QPushButton:hover {
            background-color: #e6e6e6;
        }
        """
    def operator_style(self):
        return """
        QPushButton {
            background-color: #d9d9d9;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #cfcfcf;
        }
        """

    def clear_style(self):
        return """
        QPushButton {
            background-color: #ffdddd;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #ffcccc;
        }
        """

    def handle_button(self):
        button = self.sender()
        text = button.text()
        current = self.display.text()

        if text == "C" or text == "CE":
            self.display.setText("0")
            return

        
        if text == "<-":
            self.display.setText(current[:-1] if current[:-1] else "0")
            return

        if current == "0" and text not in [".", "+/-"]:
            current = ""

        if text == "=":
            try:
                result = eval(current)
                self.display.setText(str(result))
            except:
                self.display.setText("Error")
            return


        elif text == "%":
            try:
                self.display.setText(str(float(current) / 100))
            except:
                self.display.setText("Error")
            return

        elif text == "1/x":
            try:
                self.display.setText(str(1 / float(current)))
            except:
                self.display.setText("Error")
            return

        elif text == "x^2":
            try:
                self.display.setText(str(float(current) ** 2))
            except:
                self.display.setText("Error")
            return

        elif text == "sqrt(x)":
            try:
                self.display.setText(str(math.sqrt(float(current))))
            except:
                self.display.setText("Error")
            return

        elif text == "+/-":
            try:
                self.display.setText(str(-float(current)))
            except:
                self.display.setText("Error")
            return

        else:
            self.display.setText(current + text)
            return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setCentralWidget(CalculatorUILayout())
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("Background-color: #f2f2f2;")

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

        