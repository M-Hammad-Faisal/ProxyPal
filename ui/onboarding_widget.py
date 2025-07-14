from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from .icons import create_filled_icon, ONBOARDING_ICON_PATH


class OnboardingWidget(QWidget):
    """
    A welcome widget shown to new users when no servers are configured.
    """
    add_server_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("OnboardingWidget")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel()
        icon_label.setPixmap(create_filled_icon(ONBOARDING_ICON_PATH, "#90A4AE", size=80).pixmap(QSize(80, 80)))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Welcome to ProxyPal")
        title.setObjectName("OnboardingTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 500;")

        subtitle = QLabel("Add your first server to get started.")
        subtitle.setObjectName("OnboardingSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #546E7A;")

        self.add_server_button = QPushButton("Add Server Key")
        self.add_server_button.setObjectName("OnboardingButton")
        self.add_server_button.setMinimumHeight(50)
        self.add_server_button.setStyleSheet("""
            QPushButton#OnboardingButton {
                font-size: 16px;
                font-weight: 600;
                color: #FFFFFF;
                background-color: #009688;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton#OnboardingButton:hover {
                background-color: #00796B;
            }
        """)
        self.add_server_button.clicked.connect(self.add_server_requested.emit)

        main_layout.addStretch()
        main_layout.addWidget(icon_label)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.add_server_button)
        main_layout.addStretch()
