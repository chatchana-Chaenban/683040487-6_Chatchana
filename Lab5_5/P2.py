"""
Chatchana Chaenban
683040487-6
P2
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard import StudentCard


#  Page 1 — Student List

class StudentListPage(QWidget): 
    # add signal for going to add student page
    go_to_add = Signal()

    def __init__(self):
        super().__init__()
        self._cards: list[StudentCard] = [] # recieve student cards in list
        self.setAcceptDrops(True)
        self._build() # create UI

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(
            f"color:{C['muted']};font-size:13px;")

        btn_add = QPushButton("+ Add Student")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        btn_add.clicked.connect(self.go_to_add.emit) # when clicked, emit signal to another page

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(btn_add)

        # scroll area
        self._scroll = QScrollArea()
        self._scroll.setStyleSheet(SCROLL_SS)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # container
        self._container = QWidget()
        self._container.setStyleSheet(f"background:{C['bg']};")
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setContentsMargins(24, 16, 24, 16)
        self._card_lay.setSpacing(10)
        self._card_lay.addStretch()
        self._scroll.setWidget(self._container)

        # empty state
        self._lbl_empty = QLabel("No students registered yet.\nClick \"+ Add Student\" to get started.")
        self._lbl_empty.setAlignment(Qt.AlignCenter)
        self._lbl_empty.setStyleSheet(f"color:{C['muted']};font-size:13px;")
        root.addWidget(bar)
        root.addWidget(self._lbl_empty, stretch=1)
        root.addWidget(self._scroll, stretch=1)
        self._refresh_empty()

    # public
    def add_student(self, data: dict):
        # create card and connect the delete signal
        card = StudentCard(data)
        card.delete_requested.connect(self._remove_card)

        # Add card to the list
        self._cards.append(card)

        # insert card to the card layout
        self._card_lay.insertWidget(self._card_lay.count() - 1, card)

        # update count and empty store
        self._refresh_count()
        self._refresh_empty()

    # private
    def _remove_card(self, card: StudentCard):
        # inline confirmation — no popup, just ask once
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['fullname']}?",
            QMessageBox.Yes | QMessageBox.No,)
        if reply == QMessageBox.Yes:
            # remove card from the list
            self._cards.remove(card)

            # remove card from layout
            self._card_lay.removeWidget(card)
            card.deleteLater()
            self._refresh_count()
            self._refresh_empty()

    def _refresh_count(self):
        # get number of card
        n = len(self._cards)
        # update number of student label
        self.lbl_count.setText(f"{n} enrolled")

    def _refresh_empty(self):
        has = bool(self._cards)
        self._lbl_empty.setVisible(not has)
        self._scroll.setVisible(has)

    # drag-drop reorder
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return
        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break
        src_idx = self._cards.index(src)
        if src_idx == target:
            return
        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        for card in self._cards:
            self._card_lay.removeWidget(card)
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)
        event.acceptProposedAction()

#  Page 2 — Add Student Form
class AddStudentPage(QWidget):
    # Add signals for going back and going forward
    go_back = Signal()
    go_review = Signal(dict)

    def __init__(self):
        super().__init__()
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(f"background:{C['bg']}; border-bottom:1px solid {C['border']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        # scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # personal info
        form.addWidget(section_label("Personal Information"))
        
        # Student ID (full width)
        row_id = QHBoxLayout()
        row_id.addWidget(field_label("Student ID *"))
        self.inp_id = self._inp("e.g. 65010001")
        row_id.addWidget(self.inp_id)
        form.addLayout(row_id)

        # First Name + Last Name (side by side)
        row_name = QHBoxLayout()
        row_name.setSpacing(12)
        row_name.addWidget(field_label("First Name *"))
        self.inp_first = self._inp("First name")
        row_name.addWidget(self.inp_first, stretch=1)
        row_name.addWidget(field_label("Last Name *"))
        self.inp_last = self._inp("Last name")
        row_name.addWidget(self.inp_last, stretch=1)
        form.addLayout(row_name)

        # Faculty + Major (side by side)
        row_dept = QHBoxLayout()
        row_dept.setSpacing(12)
        row_dept.addWidget(field_label("Faculty *"))
        self.inp_faculty = self._inp("e.g. Science & Technology")
        row_dept.addWidget(self.inp_faculty, stretch=1)
        row_dept.addWidget(field_label("Major *"))
        self.inp_major = self._inp("e.g. Computer Science")
        row_dept.addWidget(self.inp_major, stretch=1)
        form.addLayout(row_dept)  
        form.addWidget(divider())

        # course selection
        form.addWidget(section_label("Course Selection  (choose 1-3)"))

        # add combo box for course selection
        def make_combo() -> QComboBox:
            cb = QComboBox()
            cb.addItems(COURSES)
            cb.setMinimumHeight(38)
            cb.setStyleSheet(COMBO_SS)
            return cb
 
        row_c1 = QHBoxLayout()
        row_c1.addWidget(field_label("Course 1"))
        self.combo1 = make_combo()
        row_c1.addWidget(self.combo1)
        form.addLayout(row_c1)
 
        row_c2 = QHBoxLayout()
        row_c2.addWidget(field_label("Course 2"))
        self.combo2 = make_combo()
        row_c2.addWidget(self.combo2)
        form.addLayout(row_c2)
 
        row_c3 = QHBoxLayout()
        row_c3.addWidget(field_label("Course 3"))
        self.combo3 = make_combo()
        row_c3.addWidget(self.combo3)
        form.addLayout(row_c3)

        # error label
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']};font-size:13px;")
        form.addWidget(self.lbl_err)
        form.addStretch()

        # buttons
        btn_row = QHBoxLayout()
        bc = QPushButton("← Cancel")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}"))
        bc.clicked.connect(self._on_cancel) # when clicked, call the cancel method

        br = QPushButton("Review →")
        br.setCursor(QCursor(Qt.PointingHandCursor))
        br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        br.clicked.connect(self._on_review) # when clicked, call the review method

        btn_row.addWidget(bc)
        btn_row.addStretch()
        btn_row.addWidget(br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll, stretch=1)

    def _on_cancel(self):
        self.clear_form()
        self.go_back.emit() # emit signal to go back to the list page

    def _on_review(self):
        # check for field errors / incomplete
        missing = []
        if not self.inp_id.text().strip():
            missing.append("Student ID")
        if not self.inp_first.text().strip():
            missing.append("First Name")
        if not self.inp_last.text().strip():
            missing.append("Last Name")
        if not self.inp_faculty.text().strip():
            missing.append("Faculty")
        if not self.inp_major.text().strip():
            missing.append("Major")

        courses = [
            self.combo1.currentText(),
            self.combo2.currentText(),
            self.combo3.currentText(),
        ]
        selected = [c for c in courses if not c.startswith("—")]
        if not selected:
            missing.append("at least 1 course")
    
        # Warn the user if needed
        if missing:
            self.lbl_err.setText("Required: " + ",  ".join(missing))
            return
        
        # emit signals with data
        self.lbl_err.setText("")
        data = {
            "student_id": self.inp_id.text().strip(),
            "firstname":  self.inp_first.text().strip(),
            "lastname":   self.inp_last.text().strip(),
            "fullname":   f"{self.inp_first.text().strip()} {self.inp_last.text().strip()}",
            "faculty":    self.inp_faculty.text().strip(),
            "major":      self.inp_major.text().strip(),
            "course1":    self.combo1.currentText(),
            "course2":    self.combo2.currentText(),
            "course3":    self.combo3.currentText(),}
        self.go_review.emit(data)


    # For when coming back from the review page
    def load_data(self, d: dict):
        """Pre-fill form when user clicks Edit on Page 3."""
        self.inp_id.setText(d.get("student_id", ""))
        self.inp_first.setText(d.get("firstname", ""))
        self.inp_last.setText(d.get("lastname", ""))
        self.inp_faculty.setText(d.get("faculty", ""))
        self.inp_major.setText(d.get("major", ""))

        # set combo box selection based on course1, course2, course3 in data
        for combo, key in [(self.combo1, "course1"),
            (self.combo2, "course2"),
            (self.combo3, "course3"),
]:
            idx = combo.findText(d.get(key, ""))
            combo.setCurrentIndex(idx if idx >= 0 else 0)

    # For when going back to the home page
    def clear_form(self):
        for w in (self.inp_id, self.inp_first, self.inp_last,
                  self.inp_faculty, self.inp_major):
            w.clear()
        for cb in (self.combo1, self.combo2, self.combo3):
            cb.setCurrentIndex(0)
        self.lbl_err.setText("")

#  Page 3 — Review & Confirm
class ReviewPage(QWidget):
    # Emit signals for confirming and going back to edit
    confirmed = Signal(dict)
    go_edit = Signal(dict)

    def __init__(self):
        super().__init__()
        self._data: dict = {}
        self._build()

    def _row(self, layout: QVBoxLayout, label: str) -> QLabel:
        row = QHBoxLayout()
        row.setSpacing(0)
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']};font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']};font-size:13px;")
        val.setWordWrap(True)
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(f"background:{C['bg']}; border-bottom:1px solid {C['border']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)
        # summary section
        form.addWidget(section_label("Student Information"))

        # create row for each field
        self._val_id      = self._row(form, "Student ID")
        self._val_name    = self._row(form, "Full Name")
        self._val_faculty = self._row(form, "Faculty")
        self._val_major   = self._row(form, "Major")
 
        form.addWidget(divider())
        form.addWidget(section_label("Courses"))
        
        self._val_c1 = self._row(form, "Course 1")
        self._val_c2 = self._row(form, "Course 2")
        self._val_c3 = self._row(form, "Course 3")

        # buttons
        btn_row = QHBoxLayout()
        be = QPushButton("← Edit")
        be.setCursor(QCursor(Qt.PointingHandCursor))
        be.setStyleSheet(btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}"))
        be.clicked.connect(lambda: self.go_edit.emit(self._data))

        bc = QPushButton("Confirm Registration")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['green'], "#15803d"))
        bc.clicked.connect(lambda: self.confirmed.emit(self._data))

        btn_row.addWidget(be)
        btn_row.addStretch()
        btn_row.addWidget(bc)
        form.addLayout(btn_row)

        root.addWidget(bar)
        root.addWidget(body, stretch=1)

    def load_data(self, d: dict):
        # fill data into the review page
        self._data = d
        self._val_id.setText(d.get("student_id", "—"))
        self._val_name.setText(d.get("fullname", "—"))
        self._val_faculty.setText(d.get("faculty", "—"))
        self._val_major.setText(d.get("major", "—"))

        for val_lbl, key in [
            (self._val_c1, "course1"),
            (self._val_c2, "course2"),
            (self._val_c3, "course3"),
        ]:
            txt = d.get(key, "")
            val_lbl.setText(txt if txt and not txt.startswith("—") else "—")

#  Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()

    def _build(self):
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.setCentralWidget(central)

        # Add and Manage Stack
        self._page1 = StudentListPage()
        self._page2 = AddStudentPage()
        self._page3 = ReviewPage()

        self._stack = QStackedWidget()
        self._stack.addWidget(self._page1)   # index 0
        self._stack.addWidget(self._page2)   # index 1
        self._stack.addWidget(self._page3)   # index 2
        outer.addWidget(self._stack)

        # signals
        self._page1.go_to_add.connect(lambda: self._stack.setCurrentIndex(1))
        self._page2.go_back.connect(lambda: self._stack.setCurrentIndex(0))
        self._page2.go_review.connect(self._on_go_review)
        self._page3.go_edit.connect(self._on_go_edit)
        self._page3.confirmed.connect(self._on_confirmed)

    # Helper methods, if you need some
    def _on_go_review(self, data: dict):
        self._page3.load_data(data)
        self._stack.setCurrentIndex(2)

    def _on_go_edit(self, data: dict):
        self._page2.load_data(data)
        self._stack.setCurrentIndex(1)

    def _on_confirmed(self, data: dict):
        self._page1.add_student(data)
        self._page2.clear_form()
        self._stack.setCurrentIndex(0)
        QMessageBox.information(self, "Registration Successful",f"{data['fullname']} has been registered successfully!",)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())