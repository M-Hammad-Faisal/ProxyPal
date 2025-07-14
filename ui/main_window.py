from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QApplication, QSystemTrayIcon, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from .dialogs import AddServerDialog, FeedbackDialog
from .server_widget import ServerWidget
from .onboarding_widget import OnboardingWidget
from .icons import (create_filled_icon, create_outlined_icon, FEEDBACK_ICON_PATH,
                    CONTACT_ICON_PATH, ADD_ICON_PATH, APP_ICON_PATH, TRAY_ICON_CONNECTED, TRAY_ICON_DISCONNECTED)
from core.parser import parse_access_key
from core.connection import ConnectionManager
from core.storage import load_servers, save_servers, save_feedback


class ProxyPalWindow(QMainWindow):
    """The main application window, now managed by a system tray icon."""

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("ProxyPal")
        self.setMinimumSize(450, 650)
        self.resize(450, 650)

        self.setWindowIcon(create_filled_icon(APP_ICON_PATH, "#263238", size=128))

        self.server_widget = None
        self.onboarding_widget = None
        self.connection_manager = ConnectionManager()

        self.init_ui()
        self.create_tray_icon()
        self.setup_initial_state()

        self.show()

    def init_ui(self):
        self.create_menu_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_container_layout = QVBoxLayout()
        main_layout.addLayout(self.card_container_layout)

    def create_tray_icon(self):
        """Creates the system tray icon and its context menu."""
        self.tray_icon = QSystemTrayIcon(self)
        self.update_tray_icon(connected=False)

        tray_menu = QMenu()

        open_action = QAction("Open", self)
        open_action.setShortcut("Cmd+O")
        open_action.triggered.connect(self.show_window)

        self.status_action = QAction("Disconnected", self)
        self.status_action.setEnabled(False)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Cmd+Q")
        quit_action.triggered.connect(self.quit_application)

        tray_menu.addAction(open_action)
        tray_menu.addAction(self.status_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_window(self):
        """A dedicated method to show and raise the window."""
        self.show()
        self.activateWindow()
        self.raise_()

    def update_tray_icon(self, connected: bool):
        """Updates the tray icon image based on connection status."""
        if connected:
            icon = create_filled_icon(TRAY_ICON_CONNECTED, "#000000", size=48)
        else:
            icon = create_outlined_icon(TRAY_ICON_DISCONNECTED, "#000000", size=48)

        icon.setIsMask(True)
        self.tray_icon.setIcon(icon)

    def setup_initial_state(self):
        """Checks for saved servers and shows either the server card or the onboarding screen."""
        servers = load_servers()
        if not servers:
            self.show_onboarding_screen()
        else:
            self.add_server(servers[0]['id'])

    def show_onboarding_screen(self):
        """Creates and displays the onboarding widget."""
        if self.server_widget:
            self.server_widget.deleteLater()
            self.server_widget = None

        if not self.onboarding_widget:
            self.onboarding_widget = OnboardingWidget()
            self.onboarding_widget.add_server_requested.connect(self.show_add_server_dialog)
            self.card_container_layout.addWidget(self.onboarding_widget)

    def add_server(self, key):
        """Adds or replaces the single server card."""
        try:
            if self.onboarding_widget:
                self.onboarding_widget.deleteLater()
                self.onboarding_widget = None

            config = parse_access_key(key)

            if self.server_widget:
                if self.server_widget.is_connected:
                    self.server_widget.toggle_connection()
                self.server_widget.deleteLater()

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
            self.show_onboarding_screen()

    def on_connection_result(self, success, message, port, server_id):
        if not self.server_widget or self.server_widget.server_config['id'] != server_id:
            return

        self.server_widget.set_connection_state(success)
        self.update_tray_icon(connected=success)

        if success:
            self.status_action.setText("Connected")
        else:
            self.status_action.setText("Disconnected")

        if not success:
            if "Connection Failed" in message or "refused" in message:
                self.show_message("Connection Failed", message)
            elif "Disconnected" not in message:
                self.show_message("Connection Error", message)

    def quit_application(self):
        """Properly cleans up and quits the application."""
        self.connection_manager.disconnect()
        self.tray_icon.hide()
        QApplication.instance().quit()

    def closeEvent(self, event):
        """Overrides the close event to hide the window instead of quitting."""
        event.ignore()
        self.hide()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        add_action = QAction(create_filled_icon(ADD_ICON_PATH, "#263238"), "Add/Replace Server", self)
        add_action.triggered.connect(self.show_add_server_dialog)
        file_menu.addAction(add_action)
        file_menu.addSeparator()
        quit_action = QAction("Quit ProxyPal", self)
        quit_action.triggered.connect(self.hide)
        file_menu.addAction(quit_action)
        help_menu = menu_bar.addMenu("Help")
        feedback_action = QAction(create_filled_icon(FEEDBACK_ICON_PATH, "#263238"), "Submit Feedback", self)
        feedback_action.triggered.connect(self.show_feedback_dialog)
        help_menu.addAction(feedback_action)
        contact_action = QAction(create_filled_icon(CONTACT_ICON_PATH, "#263238"), "Contact Us", self)
        contact_action.triggered.connect(
            lambda: self.show_message("Contact Us", "For support, please email:<br><b>hammadfaisal178@gmail.com</b>",
                                      informative=True))
        help_menu.addAction(contact_action)

    def show_add_server_dialog(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text().strip()
        initial_key = ""
        if clipboard_text.startswith("ss://"):
            try:
                parse_access_key(clipboard_text)
                initial_key = clipboard_text
            except ValueError:
                pass
        dialog = AddServerDialog(self, initial_key=initial_key)
        if dialog.exec():
            key = dialog.get_key()
            if key:
                self.add_server(key)

    def handle_rename_server(self, server_id, new_name):
        if self.server_widget and self.server_widget.server_config['id'] == server_id:
            save_servers([self.server_widget.server_config])

    def handle_connection_request(self, server_config, connect_flag):
        if connect_flag:
            self.connection_manager.connect(server_config, self.on_connection_result)
        else:
            self.connection_manager.disconnect()
            self.on_connection_result(False, "Disconnected", 0, server_config['id'])

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
