"""
Chatchana Chaenban
683040487-6
P1
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LoginUIwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("login")
        self.setFixedSize(380, 560)

        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(340, 500)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        title = QLabel("LOGIN")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignLeft)
        card_layout.addWidget(title)
        card_layout.addSpacing(10)

        card_layout.addWidget(QLabel("Email")) # Email
        email = QLineEdit()
        email.setPlaceholderText("")
        card_layout.addWidget(email)

        card_layout.addWidget(QLabel("Password")) # Password
        password = QLineEdit()
        password.setPlaceholderText("")
        password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(password)

        remember = QCheckBox("Remember me?") # Check box remember
        card_layout.addWidget(remember)

        login_b = QPushButton("LOGIN") # Login Button
        login_b.setObjectName("loginBtn")
        card_layout.addWidget(login_b)

        forgot = QLabel("Forgot Password?") # Forgot Password
        forgot.setAlignment(Qt.AlignRight)
        forgot.setObjectName("forgot")
        card_layout.addWidget(forgot)

        or_container = QWidget() # Or Label
        or_layout = QHBoxLayout(or_container)
        or_layout.setContentsMargins(0, 10, 0, 10)

        line_left = QFrame()
        line_left.setFrameShape(QFrame.HLine)
        line_left.setStyleSheet("color: #ccc")

        line_right = QFrame()
        line_right.setFrameShape(QFrame.HLine)
        line_right.setStyleSheet("color: #ccc")

        or_label = QLabel("OR")
        or_label.setObjectName("orLabel")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setFixedSize(28, 28)

        or_layout.addWidget(line_left)
        or_layout.addWidget(or_label)
        or_layout.addWidget(line_right)

        card_layout.addWidget(or_container)

        social_layout = QHBoxLayout() # BOX G F IN

        socials = [
            ("G", "#DB4437"),    
            ("f", "#4267B2"),    
            ("in", "#0A66C2"),   
        ]
        for text, color in socials:
            btn = QPushButton(text)
            btn.setObjectName("socialBtn")
            btn.setFixedSize(42, 42)
            btn.setStyleSheet(f"""
                QPushButton {{
                    color: {color};
                    font-size: 16px;
                    font-weight: bold;
                }}
                 QPushButton:hover {{
                    background-color: #f5f5f5;
                }}
            """)
            social_layout.addWidget(btn)

        social_layout.setAlignment(Qt.AlignCenter)
        card_layout.addLayout(social_layout)

        signup = QLabel("Need an account? <b>SIGN UP<b>") # SIGN LABel
        signup.setAlignment(Qt.AlignCenter)
        card_layout.addSpacing(10)
        card_layout.addWidget(signup)

        main_layout = QVBoxLayout(self) # main layout
        main_layout.addWidget(card, alignment=Qt.AlignCenter)


        self.setStyleSheet("""
/* Window background */
QWidget {
    font-family: Arial;
}

/* Card */
#card {
    background-color: #ffffff;
    border-radius: 14px;
}

/* Title */
#title {
    font-size: 18px;
    font-weight: bold;
    color: #222;
}

/* Labels */
QLabel {
    font-size: 12px;
    color: #444;
}

/* Inputs */
QLineEdit {
    background-color: #ffffff;
    color: #222;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
}

QLineEdit:focus {
    border: 1px solid #f06292;
}

/* Checkbox */
QCheckBox {
    font-size: 12px;
    color: #444;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: #fff;
}

QCheckBox::indicator:checked {
    background-color: #f06292;
    border: 1px solid #f06292;
}

/* Login button */
#loginBtn {
    background-color: #f06292;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

#loginBtn:hover {
    background-color: #ec407a;
}

/* Forgot password */
#forgot {
    color: #888;
    font-size: 11px;
}

/* OR label */
#orLabel {
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 10px;
    font-weight: bold;
    color: #666;
}

/* Divider line */
QFrame[frameShape="4"] {
    color: #ddd;
}

/* Social buttons */
#socialBtn {
    background-color: #ffffff;
    border: 1px solid #ddd;
    border-radius: 21px;
}

#socialBtn:hover {
    background-color: #f5f5f5;
}
""")


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = LoginUIwindow()
    window.show()
    sys.exit(app.exec())
