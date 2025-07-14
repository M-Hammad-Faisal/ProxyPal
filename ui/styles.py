# --- STYLESHEET (QSS) ---
# Version 1.6: Single-card UI, stable connection logic, refined menu bar.
STYLESHEET = """
#MainWindow, QDialog {
    background-color: #ECEFF1;
    font-family: 'Inter', 'SF Pro Text', 'Roboto', sans-serif;
}

/* Menu Bar Styling */
QMenuBar {
    background-color: #ECEFF1;
    border-bottom: 1px solid #CFD8DC;
}
QMenuBar::item {
    padding: 6px 12px;
    background: transparent;
    color: #37474F;
}
QMenuBar::item:selected {
    background-color: #CFD8DC;
}

/* Dropdown Menu Styling */
QMenu {
    background-color: #FFFFFF;
    color: #263238;
    border: 1px solid #B0BEC5;
    padding: 5px;
}
QMenu::item {
    padding: 8px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #F5F5F5;
}
QMenu::separator {
    height: 1px;
    background: #ECEFF1;
    margin: 5px 0px;
}

/* Main Server Card */
#ServerCard {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #CFD8DC;
    max-width: 450px; /* Constrain width for better look */
    min-width: 350px;
}

QLabel {
    color: #263238;
}

QLabel#ServerNameLabel {
    font-size: 20px;
    font-weight: 500;
}

QLabel#ServerIpLabel {
    font-size: 14px;
    color: #546E7A;
}

QLabel#StatusTextLabel {
    font-size: 16px;
    color: #546E7A;
    font-weight: 500;
}

QLabel#StatusTextLabel[connected="true"] {
    color: #009688;
}

QPushButton#ConnectButton {
    background-color: transparent;
    color: #009688;
    border: none;
    padding: 20px;
    border-top: 1px solid #CFD8DC;
    font-size: 16px;
    font-weight: 600;
}

QPushButton#ConnectButton:hover {
    background-color: #F5F5F5;
}
QPushButton#ConnectButton:disabled {
    color: #BDBDBD;
}

QPushButton#CardMenuButton {
    background-color: transparent;
    border: none;
    padding: 8px;
}

/* Dialog Styling */
#AddServerDialog, #FeedbackDialog, QMessageBox {
    background-color: #FFFFFF;
}
#AddServerDialog QLabel, #FeedbackDialog QLabel, QMessageBox QLabel {
    color: #263238;
}
#AddServerDialog QPushButton, #FeedbackDialog QPushButton, QMessageBox QPushButton {
    background-color: #F5F5F5;
    color: #263238;
    border: 1px solid #CFD8DC;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
}
#AddServerDialog QPushButton:hover, #FeedbackDialog QPushButton:hover, QMessageBox QPushButton:hover {
    background-color: #E0E0E0;
}

#AddServerDialog QPushButton#ConfirmButton, #FeedbackDialog QPushButton#OkButton {
    background-color: #009688;
    color: #FFFFFF;
    border: none;
}
#AddServerDialog QPushButton#ConfirmButton:hover, #FeedbackDialog QPushButton#OkButton:hover {
    background-color: #00796B;
}

#AddServerDialog QTextEdit, #FeedbackDialog QTextEdit {
    background-color: #F5F5F5;
    border: 1px solid #CFD8DC;
    border-radius: 4px;
    color: #263238;
    padding: 8px;
}
#AddServerDialog QTextEdit:focus, #FeedbackDialog QTextEdit:focus {
    border: 1px solid #009688;
}

QMessageBox QCheckBox {
    color: #37474F;
    font-size: 13px;
    padding-top: 10px;
}
"""