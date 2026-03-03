"""
Chatchana Chaenban
683040487-6
P2
"""

import sys
import random
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QComboBox, QLineEdit, QPushButton, QToolBar,
    QMessageBox, QFormLayout, QSlider, QFileDialog, QProgressBar, 
)
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize

MAX_TOTAL = 40
DEFAULT_STAT = 5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("BASE_DIR =", BASE_DIR)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def icon(filename):
    path = os.path.join(BASE_DIR, filename)
    return QIcon(path)

def pixmap_icon(filename):
    path = os.path.join(BASE_DIR, filename)
    return QPixmap(path)


class GameBuilderUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Build")
        self.setGeometry(100, 100, 950, 550)

        self.create_menu()
        self.create_toolbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)

        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)

        self.input_layout = QFormLayout()
        self.left_layout.addLayout(self.input_layout)

        self.input_character()

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        self.left_layout.addWidget(separator)

        self.stat_input()
        self.main_layout.addWidget(self.left_widget)

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        self.main_layout.addWidget(line)

        self.create_character_sheet()
        self.main_layout.addWidget(self.sheet_widget)

        self.statusBar().showMessage("Ready - create your character")

    def create_menu(self):
        menubar = self.menuBar()

        game_menu = menubar.addMenu("Game")
        edit_menu = menubar.addMenu("Edit")

        game_menu.addAction("New Character", self.new_character)
        game_menu.addAction("Generate Sheet", self.generate_character)
        game_menu.addAction("Save Sheet", self.save_sheet)
        game_menu.addSeparator()
        game_menu.addAction("Exit", self.close)

        edit_menu.addAction("Reset Stats", self.reset_stats)
        edit_menu.addAction("Randomize", self.randomize_character)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.setIconSize(QSize(24, 24))

        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2b2b3c;
                spacing: 10px;
            }
            QToolButton {
                color: white;
                font-weight: bold;
                padding: 5px 10px;
            }
            QToolButton:hover {
                background-color: #3c3c55;
                border-radius: 5px;
            }
        """)

        new_action = QAction(icon("book.png"), "New", self)
        new_action.triggered.connect(self.new_character)
        toolbar.addAction(new_action)

        generate_action = QAction(icon("sword.png"), "Generate", self)
        generate_action.triggered.connect(self.generate_character)
        toolbar.addAction(generate_action)

        random_action = QAction(icon("dice.png"), "Randomize", self)
        random_action.triggered.connect(self.randomize_character)
        toolbar.addAction(random_action)

        save_action = QAction(icon("file.png"), "Save", self)
        save_action.triggered.connect(self.save_sheet)
        toolbar.addAction(save_action)


    def input_character(self):
        self.Char_name = QLineEdit()
        self.Char_name.setPlaceholderText("Enter character name...")
        self.input_layout.addRow("Character name:", self.Char_name)

        self.race_class = QComboBox()
        self.race_class.setPlaceholderText("Choose race")
        self.race_class.addItems(
            ["Human", "Elf", "Dwarf", "Orc", "Undead"]
            )
        self.input_layout.addRow("Race:", self.race_class)

        self.class_input = QComboBox()
        self.class_input.setPlaceholderText("Choose class")
        self.class_input.addItems(
            ["Warrior", "Mage", "Rogue", "Paladin", "Ranger"]
            )
        self.input_layout.addRow("Class:", self.class_input)

        self.gender_input = QComboBox()
        self.gender_input.setPlaceholderText("Choose gender")
        self.gender_input.addItems(
            ["Male", "Female", "Other"]
            )
        self.input_layout.addRow("Gender:", self.gender_input)

    def stat_input(self):
        self.stats = {}

        stat_icons = {
            "STR": "sword.png",
            "DEX": "magic-boot.png",
            "INT": "book.png",
            "VIT": "heart.png"
        }

        for stat in ["STR", "DEX", "INT", "VIT"]:
            layout = QHBoxLayout()

            icon_label = QLabel()
            pix = pixmap_icon(stat_icons[stat])

            if not pix.isNull():
                icon_label.setPixmap(
                    pix.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )

            text_label = QLabel(stat)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(1, 20)
            slider.setValue(DEFAULT_STAT)
            slider.valueChanged.connect(self.update_total)

            value_label = QLabel(str(DEFAULT_STAT))
            value_label.setFixedWidth(30)

            slider.valueChanged.connect(
                lambda value, lbl=value_label: lbl.setText(str(value))
            )

            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            layout.addWidget(slider)
            layout.addWidget(value_label)

            self.left_layout.addLayout(layout)
            self.stats[stat] = slider

        self.total_label = QLabel()
        self.left_layout.addWidget(self.total_label)

        self.generate_btn = QPushButton("Generate Character Sheet")
        self.generate_btn.setIcon(icon("sword.png"))
        self.generate_btn.setIconSize(QSize(24, 24)) 
        self.generate_btn.clicked.connect(self.generate_character)
        self.left_layout.addWidget(self.generate_btn)

        self.update_total()

    def total_points(self):
        return sum(slider.value() for slider in self.stats.values())

    def update_total(self):
        total = self.total_points()
        self.total_label.setText(f"Points used: {total} / {MAX_TOTAL}")
        self.total_label.setStyleSheet(
            "color: red;" if total > MAX_TOTAL else "color: black;"
        )

    def create_character_sheet(self):
        self.sheet_widget = QWidget()
        self.sheet_widget.setFixedWidth(280)
        self.sheet_widget.setStyleSheet("""
            background-color: #1e1e2f;
            color: white;
            border-radius: 15px;
        """)

        layout = QVBoxLayout(self.sheet_widget)

        self.sheet_name = QLabel("-- Character Name --")
        self.sheet_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sheet_name)

        self.sheet_info = QLabel("Race • Class")
        self.sheet_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sheet_info)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)

        self.progress_bars = {}

        for stat in ["STR", "DEX", "INT", "VIT"]:
            layout.addWidget(QLabel(stat))
            bar = QProgressBar()
            bar.setRange(0, 20)
            bar.setValue(DEFAULT_STAT)
            bar.setTextVisible(False)
            layout.addWidget(bar)
            self.progress_bars[stat] = bar

        layout.addStretch()

    def generate_character(self):
        if self.total_points() > MAX_TOTAL:
            QMessageBox.warning(self, "ERROR", "Total points exceed 40!")
            return

        name = self.Char_name.text() or "Unnamed Hero"
        race = self.race_class.currentText()
        char_class = self.class_input.currentText()

        self.sheet_name.setText(name)
        self.sheet_info.setText(f"{race} • {char_class}")

        for stat, slider in self.stats.items():
            self.progress_bars[stat].setValue(slider.value())

        self.statusBar().showMessage("Character generated!")

    def reset_stats(self):
        for slider in self.stats.values():
            slider.setValue(DEFAULT_STAT)
        self.statusBar().showMessage("Stats reset.")

    def randomize_character(self):
        remaining = MAX_TOTAL
        sliders = list(self.stats.values())

        for i, slider in enumerate(sliders):
            if i == len(sliders) - 1:
                slider.setValue(min(20, remaining))
            else:
                max_value = min(20, remaining - (len(sliders) - i - 1))
                value = random.randint(1, max_value)
                slider.setValue(value)
                remaining -= value

        self.statusBar().showMessage("Character randomized.")

    def save_sheet(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Character Sheet", "", "Text Files (*.txt)"
        )
        if not file_path:
            return

        with open(file_path, "w") as f:
            f.write(f"Name: {self.sheet_name.text()}\n")
            f.write(f"{self.sheet_info.text()}\n\n")
            for stat, slider in self.stats.items():
                f.write(f"{stat}: {slider.value()}\n")

        self.statusBar().showMessage("Character sheet saved.")

    def new_character(self):
        self.Char_name.clear()
        self.reset_stats()
        self.sheet_name.setText("-- Character Name --")
        self.sheet_info.setText("Race • Class")
        self.statusBar().showMessage("New character created.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameBuilderUI()
    window.show()
    sys.exit(app.exec())