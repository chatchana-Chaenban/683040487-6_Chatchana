"""
Chatchana Chaenban
68304087-6
P2
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QSpinBox,
    QPushButton, QRadioButton, QButtonGroup,
    QCheckBox, QComboBox, QTextEdit, QDateEdit
)
from PySide6.QtCore import Qt, QDate, QLocale
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
 
class PersonalInfo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Full Name:"))
        name = QLineEdit()
        name.setMaxLength(50)
        name.setValidator(QRegularExpressionValidator(
            QRegularExpression("[A-Za-z ]+")
        ))
        layout.addWidget(name)
        

        layout.addWidget(QLabel("Email:"))
        email = QLineEdit()
        email.setMaxLength(50)
        layout.addWidget(email)
        
        layout.addWidget(QLabel("Phone:"))
        phone = QLineEdit()
        phone.setMaxLength(15)
        phone.setValidator(QRegularExpressionValidator(
            QRegularExpression("[0-9]+")
        ))
        layout.addWidget(phone)

class DateOfBirth(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)  # Shows calendar dropdown
        self.date_edit.setDisplayFormat("dd/MM/yyyy")  # Format like "01/01/2000"
        self.date_edit.setDate(QDate(2000, 1, 1))  # Set default date to January 1, 2000
        self.date_edit.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        layout.addWidget(self.date_edit, alignment= Qt.AlignLeft)
        self.date_edit.setFixedWidth(200)
        
class GenderInfo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.gender_group = QButtonGroup(self)
        
        radio_layout = QHBoxLayout()
        
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.nonbinary_radio = QRadioButton("Non-binary")
        self.prefer_not_radio = QRadioButton("Prefer not to say")
        
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.nonbinary_radio)
        self.gender_group.addButton(self.prefer_not_radio)
        
        radio_layout.addWidget(self.male_radio)
        radio_layout.addWidget(self.female_radio)
        radio_layout.addWidget(self.nonbinary_radio)
        radio_layout.addWidget(self.prefer_not_radio)
        
        layout.addLayout(radio_layout)

class StudentRegistration(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Student Registration Form")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(15)

        layout.addWidget(PersonalInfo())

        layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        layout.addWidget(DateOfBirth())
        layout.addSpacing(15)

        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(GenderInfo())
        layout.addSpacing(15)

        layout.addWidget(QLabel("Program:"))
        program = QComboBox()
        program.addItem("Select your program")
        program.addItems([
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electrical Engineering",
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Power Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ])
        layout.addWidget(program)
        layout.addSpacing(15)

        layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        about = QTextEdit()
        about.setMaximumHeight(100)
        layout.addWidget(about)
        layout.addSpacing(20)

        layout.addWidget(QCheckBox("I accept the terms and conditions."))
        layout.addSpacing(20)

        submit = QPushButton("Submit Registration")
        submit.setFixedWidth(160)
        layout.addWidget(submit, alignment=Qt.AlignCenter)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2: Student Registration")
        self.setGeometry(100, 100, 400, 600)  # Window size 400 x 600
        
        # Create central widget
        central_widget = StudentRegistration()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())