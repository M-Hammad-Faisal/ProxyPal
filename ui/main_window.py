from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from .dialogs import AddServerDialog, FeedbackDialog
from .server_widget import ServerWidget
from .icons import create_icon, FEEDBACK_ICON_PATH, CONTACT_ICON_PATH, ADD_ICON_PATH
from core.parser import parse_access_key
from core.connection import ConnectionManager
from core.storage import load_servers, save_servers, save_feedback


class ProxyPalWindow(QMainWindow):
    """The main application window with a menu bar and single server view."""

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("ProxyPal")
        self.setMinimumSize(450, 650)
        self.resize(450, 650)

        self.server_widget = None
        self.connection_manager = ConnectionManager()

        self.init_ui()
        self.load_initial_server()

    def init_ui(self):
        self.create_menu_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_container_layout = QVBoxLayout()
        main_layout.addLayout(self.card_container_layout)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        add_action = QAction(create_icon(ADD_ICON_PATH, "#263238"), "Add/Replace Server", self)
        add_action.triggered.connect(self.show_add_server_dialog)
        file_menu.addAction(add_action)
        file_menu.addSeparator()
        quit_action = QAction("Quit ProxyPal", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = menu_bar.addMenu("Help")
        feedback_action = QAction(create_icon(FEEDBACK_ICON_PATH, "#263238"), "Submit Feedback", self)
        feedback_action.triggered.connect(self.show_feedback_dialog)
        help_menu.addAction(feedback_action)
        contact_action = QAction(create_icon(CONTACT_ICON_PATH, "#263238"), "Contact Us", self)
        contact_action.triggered.connect(
            lambda: self.show_message("Contact Us", "For support, please email:<br><b>hammadfaisal178@gmail.com</b>",
                                      informative=True))
        help_menu.addAction(contact_action)

    def show_add_server_dialog(self):
        dialog = AddServerDialog(self)
        if dialog.exec():
            key = dialog.get_key()
            if key:
                self.add_server(key)

    def add_server(self, key):
        """Adds or replaces the single server card."""
        try:
            config = parse_access_key(key)

            if self.server_widget:
                self.handle_delete_server(self.server_widget.server_config['id'])

            self.server_widget = ServerWidget(config)
            self.server_widget.connect_request.connect(self.handle_connection_request)
            self.server_widget.delete_request.connect(self.handle_delete_server)
            self.server_widget.rename_request.connect(self.handle_rename_server)

            self.card_container_layout.addWidget(self.server_widget)
            save_servers([config])
        except Exception as e:
            self.show_message("Invalid Key", f"Could not parse access key.\n\n<i style='color:#78909C'>{e}</i>")

    def handle_delete_server(self, server_id):
        if self.server_widget and self.server_widget.server_config['id'] == server_id:
            if self.server_widget.is_connected:
                self.handle_connection_request(self.server_widget.server_config, False)

            self.server_widget.deleteLater()
            self.server_widget = None
            save_servers([])

    def handle_rename_server(self, server_id, new_name):
        if self.server_widget and self.server_widget.server_config['id'] == server_id:
            save_servers([self.server_widget.server_config])

    def handle_connection_request(self, server_config, connect_flag):
        if connect_flag:
            self.connection_manager.connect(server_config, self.on_connection_result)
        else:
            self.connection_manager.disconnect()
            self.on_connection_result(False, "Disconnected", 0, server_config['id'])

    def on_connection_result(self, success, message, port, server_id):
        if not self.server_widget or self.server_widget.server_config['id'] != server_id:
            return

        if success:
            self.server_widget.set_connection_state(True)
        else:
            self.server_widget.set_connection_state(False)
            if "Connection Failed" in message or "refused" in message:
                self.show_message("Connection Failed", message)
            elif "Disconnected" not in message:
                self.show_message("Connection Error", message)

    def load_initial_server(self):
        all_configs = load_servers()
        if all_configs:
            self.add_server(all_configs[0]['id'])

    def show_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        if dialog.exec() and dialog.get_feedback():
            save_feedback(dialog.get_feedback())
            self.show_message("Feedback Received", "Thank you for your feedback!", informative=True)

    def show_message(self, title, text, informative=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Information if informative else QMessageBox.Icon.Warning)
        msg.exec()

    def closeEvent(self, event):
        self.connection_manager.disconnect()
        event.accept()
