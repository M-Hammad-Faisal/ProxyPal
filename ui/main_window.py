import platform
import requests
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QMessageBox, QApplication, QSystemTrayIcon, QMenu,
                             QScrollArea, QSpacerItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from .dialogs import AddServerDialog, FeedbackDialog
from .server_widget import ServerWidget
from .onboarding_widget import OnboardingWidget
from .icons import (create_filled_icon, create_outlined_icon, FEEDBACK_ICON_PATH,
                    CONTACT_ICON_PATH, ADD_ICON_PATH, APP_ICON_PATH, TRAY_ICON_CONNECTED, TRAY_ICON_DISCONNECTED)
from core.parser import parse_access_key
from core.connection import ConnectionManager
from core.storage import load_servers, add_server as save_new_server, delete_server as remove_server, save_servers


class ProxyPalWindow(QMainWindow):
    """The main application window, with all features and fixes."""

    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("ProxyPal")
        self.setMinimumSize(450, 650)
        self.resize(450, 650)

        self.setWindowIcon(create_filled_icon(APP_ICON_PATH, "#263238", size=128))

        self.server_widgets = []
        self.connection_manager = ConnectionManager()
        self.active_connection_id = None

        self.init_ui()
        self.create_tray_icon()
        self.setup_initial_state()

        self.show()

    def init_ui(self):
        self.create_menu_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.onboarding_widget = OnboardingWidget()
        self.onboarding_widget.add_server_requested.connect(self.show_add_server_dialog)
        main_layout.addWidget(self.onboarding_widget)
        self.onboarding_widget.hide()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(self.scroll_area)
        self.scroll_area.hide()
        self.scroll_content_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_content_widget)
        self.card_container_layout = QVBoxLayout(self.scroll_content_widget)
        self.card_container_layout.setSpacing(15)
        self.card_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def setup_initial_state(self):
        self.clear_all_servers_from_ui()
        all_servers = load_servers()
        if not all_servers:
            self.show_onboarding_screen()
        else:
            self.scroll_area.show()
            self.onboarding_widget.hide()
            for config in all_servers:
                self._add_server_widget_to_ui(config)
            self._update_layout()

    def _add_server_widget_to_ui(self, config: dict):
        server_widget = ServerWidget(config)
        server_widget.connect_request.connect(self.handle_connection_request)
        server_widget.delete_request.connect(self.handle_delete_server)
        server_widget.rename_request.connect(self.handle_rename_server)
        self.card_container_layout.addWidget(server_widget)
        self.server_widgets.append(server_widget)

    def _update_layout(self):
        for i in reversed(range(self.card_container_layout.count())):
            item = self.card_container_layout.itemAt(i)
            if isinstance(item, QSpacerItem):
                self.card_container_layout.removeItem(item)
                break
        if len(self.server_widgets) == 1:
            self.card_container_layout.insertStretch(0, 1)
            self.card_container_layout.addStretch(1)
        else:
            self.card_container_layout.addStretch(1)

    def add_server(self, key):
        try:
            config = parse_access_key(key)
            if any(s['id'] == config['id'] for s in load_servers()):
                self.show_message("Server Exists", "This server has already been added.", informative=True)
                return
            save_new_server(config)
            if not self.server_widgets:
                self.onboarding_widget.hide()
                self.scroll_area.show()
            self._add_server_widget_to_ui(config)
            self._update_layout()
        except Exception as e:
            self.show_message("Invalid Key", f"Could not parse access key.\n\n<i style='color:#78909C'>{e}</i>")

    def handle_delete_server(self, server_id):
        widget_to_remove = next((w for w in self.server_widgets if w.server_config['id'] == server_id), None)
        if widget_to_remove:
            if self.active_connection_id == server_id:
                self.connection_manager.disconnect()
                self.active_connection_id = None
                self.update_global_ui_state()
            widget_to_remove.deleteLater()
            self.server_widgets.remove(widget_to_remove)
            remove_server(server_id)
            self._update_layout()
        if not self.server_widgets:
            self.show_onboarding_screen()

    def show_onboarding_screen(self):
        self.scroll_area.hide()
        self.onboarding_widget.show()

    def handle_rename_server(self, server_id, new_name):
        all_servers = load_servers()
        for server in all_servers:
            if server['id'] == server_id:
                server['name'] = new_name
                break
        save_servers(all_servers)

    def clear_all_servers_from_ui(self):
        for widget in self.server_widgets:
            widget.deleteLater()
        self.server_widgets.clear()

    def handle_connection_request(self, server_config, connect_flag):
        self.connection_manager.disconnect()
        if connect_flag:
            widget_to_connect = next((w for w in self.server_widgets if w.server_config['id'] == server_config['id']),
                                     None)
            if widget_to_connect:
                widget_to_connect.set_is_connecting()
            self.connection_manager.connect(server_config, self.on_connection_result)
        else:
            self.on_connection_result(False, "Disconnected", 0, server_config['id'])

    def on_connection_result(self, success, message, port, server_id):
        if success:
            old_active_id = self.active_connection_id
            self.active_connection_id = server_id
            if old_active_id and old_active_id != server_id:
                old_widget = next((w for w in self.server_widgets if w.server_config['id'] == old_active_id), None)
                if old_widget:
                    old_widget.set_connection_state(False)
            new_widget = next((w for w in self.server_widgets if w.server_config['id'] == server_id), None)
            if new_widget:
                new_widget.set_connection_state(True)
        else:
            if self.active_connection_id == server_id:
                self.active_connection_id = None
            widget = next((w for w in self.server_widgets if w.server_config['id'] == server_id), None)
            if widget:
                widget.set_connection_state(False)
            if "Connection Failed" in message or "refused" in message:
                self.show_message("Connection Failed", message)
            elif "Disconnected" not in message:
                self.show_message("Connection Error", message)
        self.update_global_ui_state()

    def update_global_ui_state(self):
        is_any_server_connected = self.active_connection_id is not None
        self.update_tray_icon(connected=is_any_server_connected)
        if is_any_server_connected:
            self.status_action.setText("Connected")
        else:
            self.status_action.setText("Disconnected")

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.update_tray_icon(connected=False)
        tray_menu = QMenu()
        open_action = QAction("Open\t⌘O", self)
        open_action.triggered.connect(self.show_window)
        self.status_action = QAction("Disconnected", self)
        self.status_action.setEnabled(False)
        quit_action = QAction("Quit\t⌘Q", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(open_action)
        tray_menu.addAction(self.status_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_window(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def update_tray_icon(self, connected: bool):
        if connected:
            icon = create_filled_icon(TRAY_ICON_CONNECTED, "#000000", size=48)
        else:
            icon = create_outlined_icon(TRAY_ICON_DISCONNECTED, "#000000", size=48)
        icon.setIsMask(True)
        self.tray_icon.setIcon(icon)

    def quit_application(self):
        self.connection_manager.disconnect()
        self.tray_icon.hide()
        QApplication.instance().quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        add_action = QAction(create_filled_icon(ADD_ICON_PATH, "#263238"), "Add Server", self)
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

    def show_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        if dialog.exec():
            feedback_message = dialog.get_feedback()
            if feedback_message:
                formspree_url = "https://formspree.io/f/mvgqopya"
                payload = {
                    "message": feedback_message,
                    "os": platform.system(),
                    "os_version": platform.mac_ver()[0],
                    "app_version": "1.0"
                }
                try:
                    response = requests.post(formspree_url, data=payload)
                    response.raise_for_status()
                    self.show_message("Feedback Sent", "Thank you! Your feedback has been successfully sent.",
                                      informative=True)
                except requests.exceptions.RequestException as e:
                    print(f"Error sending feedback: {e}")
                    self.show_message("Submission Failed",
                                      "Could not send feedback. Please check your internet connection and try again.")

    def show_message(self, title, text, informative=False):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Information if informative else QMessageBox.Icon.Warning)
        msg.exec()
