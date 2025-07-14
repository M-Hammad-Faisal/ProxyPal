from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMenu, QGraphicsDropShadowEffect, \
    QInputDialog
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QSize

from .status_indicator import PieStatusIndicator
from .icons import create_icon, MORE_VERT_ICON_PATH


class ServerWidget(QFrame):
    """A widget card representing a single server, styled like Outline."""
    connect_request = pyqtSignal(dict, bool)
    delete_request = pyqtSignal(str)
    rename_request = pyqtSignal(str, str)

    def __init__(self, server_config, parent=None):
        super().__init__(parent)
        self.setObjectName("ServerCard")
        self.server_config = server_config
        self.is_connected = False
        self.init_ui()
        self.set_shadow()

    def set_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

    def init_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top part: Server details and menu
        top_frame = QFrame()
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(20, 20, 15, 10)
        details_layout = QVBoxLayout()
        details_layout.setSpacing(2)

        self.server_name_label = QLabel(self.server_config.get("name", "Unknown Server"))
        self.server_name_label.setObjectName("ServerNameLabel")
        self.server_ip_label = QLabel(f"{self.server_config.get('server')}:{self.server_config.get('server_port')}")
        self.server_ip_label.setObjectName("ServerIpLabel")
        details_layout.addWidget(self.server_name_label)
        details_layout.addWidget(self.server_ip_label)
        top_layout.addLayout(details_layout)
        top_layout.addStretch()

        self.card_menu_button = QPushButton()
        self.card_menu_button.setIcon(create_icon(MORE_VERT_ICON_PATH, "#546E7A"))
        self.card_menu_button.setObjectName("CardMenuButton")
        self.card_menu_button.setIconSize(QSize(24, 24))
        self.setup_card_menu()
        top_layout.addWidget(self.card_menu_button)
        main_layout.addWidget(top_frame)

        # Middle part: Status graphic and text
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(20, 20, 20, 20)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pie_indicator = PieStatusIndicator()
        self.status_text_label = QLabel("Disconnected")
        self.status_text_label.setObjectName("StatusTextLabel")
        self.status_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.pie_indicator, 1, Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.status_text_label)
        main_layout.addLayout(status_layout, 1)

        # Bottom part: Connect button
        self.connect_button = QPushButton("CONNECT")
        self.connect_button.setObjectName("ConnectButton")
        self.connect_button.clicked.connect(self.toggle_connection)
        main_layout.addWidget(self.connect_button)

    def setup_card_menu(self):
        menu = QMenu(self)
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(self.rename_server)
        forget_action = QAction("Forget", self)
        forget_action.triggered.connect(self.delete_server)
        menu.addAction(rename_action)
        menu.addAction(forget_action)
        self.card_menu_button.setMenu(menu)

    def rename_server(self):
        new_name, ok = QInputDialog.getText(self, 'Rename Server', 'Enter new name:',
                                            text=self.server_config.get("name"))
        if ok and new_name:
            self.server_config["name"] = new_name
            self.server_name_label.setText(new_name)
            self.rename_request.emit(self.server_config["id"], new_name)

    def delete_server(self):
        self.delete_request.emit(self.server_config["id"])

    def toggle_connection(self):
        self.connect_button.setDisabled(True)
        self.connect_request.emit(self.server_config, not self.is_connected)

    def set_connection_state(self, is_connected):
        self.is_connected = is_connected
        self.connect_button.setDisabled(False)  # Re-enable after operation
        self.pie_indicator.set_connected(self.is_connected)
        if self.is_connected:
            self.status_text_label.setText("Connected")
            self.status_text_label.setProperty("connected", True)
            self.connect_button.setText("DISCONNECT")
        else:
            self.status_text_label.setText("Disconnected")
            self.status_text_label.setProperty("connected", False)
            self.connect_button.setText("CONNECT")

        self.status_text_label.style().unpolish(self.status_text_label)
        self.status_text_label.style().polish(self.status_text_label)
