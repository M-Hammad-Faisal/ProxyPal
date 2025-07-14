from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox


class AddServerDialog(QDialog):
    """Dialog for adding a new server via access key."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AddServerDialog")
        self.setFixedSize(450, 300)
        self.setWindowTitle("Add Access Key")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("Add access key")
        title.setStyleSheet("font-size: 22px; font-weight: 500;")
        subtitle = QLabel(
            'Need a new access key? <a href="[https://outline.com](https://outline.com)" style="color: #009688;">Create one here.</a>')
        subtitle.setOpenExternalLinks(True)

        self.key_input = QTextEdit()
        self.key_input.setPlaceholderText("ss://...")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        cancel_button = QPushButton("CANCEL")
        confirm_button = QPushButton("CONFIRM")
        confirm_button.setObjectName("ConfirmButton")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.key_input, 1)
        layout.addLayout(button_layout)

        cancel_button.clicked.connect(self.reject)
        confirm_button.clicked.connect(self.accept)

    def get_key(self):
        return self.key_input.toPlainText().strip()


class FeedbackDialog(QMessageBox):
    """A custom dialog for submitting feedback."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FeedbackDialog")
        self.setWindowTitle("Submit Feedback")
        self.setIcon(QMessageBox.Icon.NoIcon)

        grid = self.layout()
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Your feedback helps us improve...")
        grid.addWidget(self.text_edit, 1, 0, 1, grid.columnCount())

        ok_button = self.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setText("Submit")
        ok_button.setObjectName("OkButton")
        self.addButton(QMessageBox.StandardButton.Cancel)

    def get_feedback(self):
        return self.text_edit.toPlainText().strip()
