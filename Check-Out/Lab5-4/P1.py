"""
Chatchana Chaenban
683040487-6
P1
"""

import sys
import os
import pyperclip
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton,
    QFrame, QSpinBox, QColorDialog, QFileDialog, QToolBar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap


default_color = "#B0E0E6"


class PersonalCard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(100, 100, 420, 520)

        self.fav_color = QColor(default_color)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Form
        self.input_layout = QFormLayout()
        self.create_form()
        self.main_layout.addLayout(self.input_layout)

        # Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        # Display
        self.bg_widget = QWidget()
        self.main_layout.addWidget(self.bg_widget)
        self.create_display()

        # Bar 
        self.create_menu()
        self.create_toolbar()

        self.statusBar().showMessage("Fill in your details and click Generate")


    def create_form(self):
        self.name = QLineEdit()
        self.name.setPlaceholderText("First name and Last name")
        self.input_layout.addRow("Full name:", self.name)

        self.age = QSpinBox()
        self.age.setRange(1, 100)
        self.age.setValue(25)
        self.input_layout.addRow("Age:", self.age)

        self.email = QLineEdit()
        self.email.setPlaceholderText("username@gmail.com")
        self.input_layout.addRow("Email:", self.email)

        self.position = QComboBox()
        self.position.setPlaceholderText("Choose your position")
        self.position.addItems(
            ["Teaching Staff", "Supporting Staff", "Student", "Visitor"]
        )
        self.input_layout.addRow("Position:", self.position)

        # Color picker row
        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)

        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(22, 22)
        self.color_swatch.setStyleSheet(
            f"background-color: {self.fav_color.name()}; border: 1px solid black;"
        )

        color_button = QPushButton("Pick New Color")
        color_button.clicked.connect(self.pick_color)

        color_layout.addWidget(self.color_swatch)
        color_layout.addWidget(color_button)

        self.input_layout.addRow("Favorite color:", color_row)


    def create_display(self):
        self.output_layout = QVBoxLayout(self.bg_widget)
        self.output_layout.setSpacing(8)

        # Initial card style
        self.bg_widget.setStyleSheet(
            f"background-color: {default_color}; padding: 15px; border-radius: 10px;"
        )

        self.name_label = QLabel("Your name here")
        self.name_label.setStyleSheet(
            "font-size: 18pt; font-weight: bold; color: black;"
        )

        self.age_label = QLabel("(Age)")
        self.age_label.setStyleSheet("color: black;")

        self.position_label = QLabel("Your position here")
        self.position_label.setStyleSheet("font-size: 14pt; color: black;")

        # Email Row (icon + text)
        email_layout = QHBoxLayout()
        email_layout.setSpacing(6)

        self.email_icon = QLabel()
        self.email_icon.setPixmap(
            QPixmap("gmail.png").scaled(
                18, 18,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        self.email_label = QLabel("your_username@domain.name")
        self.email_label.setStyleSheet("color: black;")

        email_layout.addWidget(self.email_icon)
        email_layout.addWidget(self.email_label)
        email_layout.addStretch()

        # Add widgets to card
        self.output_layout.addWidget(self.name_label)
        self.output_layout.addWidget(self.age_label)
        self.output_layout.addWidget(self.position_label)
        self.output_layout.addLayout(email_layout)
        self.output_layout.addStretch()


    def pick_color(self):
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color

            # Only update preview box
            self.color_swatch.setStyleSheet(
                f"background-color: {self.fav_color.name()}; border: 1px solid black;"
            )

            self.statusBar().showMessage(
                "Color selected (Click Generate to apply)"
            )

    def update_display(self):
        self.name_label.setText(self.name.text())
        self.age_label.setText(f"({self.age.value()})")
        self.position_label.setText(self.position.currentText())
        self.email_label.setText(self.email.text())

        # Apply color ONLY when Generate clicked
        self.bg_widget.setStyleSheet(
            f"background-color: {self.fav_color.name()}; "
            "padding: 15px; border-radius: 10px;"
        )

        self.statusBar().showMessage("Card generated successfully!")

    def clear_form(self):
        self.name.clear()
        self.age.setValue(25)
        self.position.setCurrentIndex(-1)
        self.position.setPlaceholderText("Choose your position")
        self.email.clear()
        self.color_swatch.setStyleSheet(
            f"background-color: {default_color}; border: 1px solid black;"
        )
        self.statusBar().showMessage("Form cleared")

    def clear_display(self):
        self.name_label.setText("Your name here")
        self.age_label.setText("(Age)")
        self.position_label.setText("Your position here")
        self.email_label.setText("your_username@domain.name")
        self.bg_widget.setStyleSheet(
            f"background-color: {default_color}; padding: 15px; border-radius: 10px;"
        )
        self.statusBar().showMessage("Display cleared")

    def save_card(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Card",
            "my_card.txt",
            "Text Files (*.txt);;All Files (*)",
        )

        if filename:
            with open(filename, "w") as f:
                f.write(self.get_card_text())
            self.statusBar().showMessage(f"Card saved: {filename}")

    def copy_card(self):
        pyperclip.copy(self.get_card_text())
        self.statusBar().showMessage("Card copied to clipboard")

    def get_card_text(self):
        return (
            f"{self.name_label.text()}\n"
            f"{self.age_label.text()}\n"
            f"{self.position_label.text()}\n"
            f"{self.email_label.text()}"
        )


    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")

        generate_action = QAction("Generate Card", self)
        generate_action.triggered.connect(self.update_display)

        save_action = QAction("Save Card", self)
        save_action.triggered.connect(self.save_card)

        clear_action = QAction("Clear Display", self)
        clear_action.triggered.connect(self.clear_display)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addActions(
            [generate_action, save_action, clear_action, exit_action]
        )

        copy_action = QAction("Copy Card", self)
        copy_action.triggered.connect(self.copy_card)

        clear_form_action = QAction("Clear Form", self)
        clear_form_action.triggered.connect(self.clear_form)

        edit_menu.addActions([copy_action, clear_form_action])


    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        base = os.path.dirname(os.path.abspath(__file__))

        generate_action = QAction(QIcon(os.path.join(base, "plus.png")),"Generate",self)
        generate_action.triggered.connect(self.update_display)

        save_action = QAction(QIcon(os.path.join(base, "diskette.png")),"Save",self)
        save_action.triggered.connect(self.save_card)

        clear_action = QAction(QIcon(os.path.join(base, "delete.png")),"Clear",self)
        clear_action.triggered.connect(self.clear_display)

        toolbar.addAction(generate_action)
        toolbar.addAction(save_action)
        toolbar.addAction(clear_action)



def main():
    app = QApplication(sys.argv)

    window = PersonalCard()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()