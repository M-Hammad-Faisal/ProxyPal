STYLESHEET_TEMPLATE = """
#MainWindow, QDialog {{
    background-color: {BACKGROUND};
    font-family: 'Inter', 'SF Pro Text', 'Roboto', sans-serif;
}}

/* Menu Bar Styling */
QMenuBar {{
    background-color: {MENU_BACKGROUND};
    border-bottom: 1px solid {BORDER};
}}
QMenuBar::item {{
    padding: 6px 12px;
    background: transparent;
    color: {MENU_TEXT};
}}
QMenuBar::item:selected {{
    background-color: {HOVER_BACKGROUND};
}}

/* Dropdown Menu Styling */
QMenu {{
    background-color: {CARD_BACKGROUND};
    color: {PRIMARY_TEXT};
    border: 1px solid {MENU_BORDER};
    padding: 5px;
}}
QMenu::item {{
    padding: 8px 20px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background-color: {HOVER_BACKGROUND};
}}
QMenu::separator {{
    height: 1px;
    background: {BACKGROUND};
    margin: 5px 0px;
}}

/* Main Server Card */
#ServerCard {{
    background-color: {CARD_BACKGROUND};
    border-radius: 8px;
    border: 1px solid {BORDER};
    max-width: 450px;
    min-width: 350px;
}}

QLabel {{
    color: {PRIMARY_TEXT};
}}

QLabel#ServerNameLabel {{
    font-size: 20px;
    font-weight: 500;
}}

QLabel#ServerIpLabel {{
    font-size: 14px;
    color: {SECONDARY_TEXT};
}}

QLabel#StatusTextLabel {{
    font-size: 16px;
    color: {SECONDARY_TEXT};
    font-weight: 500;
}}

QLabel#StatusTextLabel[connected="true"] {{
    color: {ACCENT_PRIMARY};
}}

QPushButton#ConnectButton {{
    background-color: transparent;
    color: {ACCENT_PRIMARY};
    border: none;
    padding: 20px;
    border-top: 1px solid {BORDER};
    font-size: 16px;
    font-weight: 600;
}}

QPushButton#ConnectButton:hover {{
    background-color: {HOVER_BACKGROUND};
}}
QPushButton#ConnectButton:disabled {{
    color: {DISABLED_TEXT};
}}

QPushButton#CardMenuButton {{
    background-color: transparent;
    border: none;
    padding: 8px;
}}

/* Dialog Styling */
#AddServerDialog, #FeedbackDialog, QMessageBox {{
    background-color: {DIALOG_BACKGROUND};
}}
#AddServerDialog QLabel, #FeedbackDialog QLabel, QMessageBox QLabel {{
    color: {PRIMARY_TEXT};
}}
#AddServerDialog QPushButton, #FeedbackDialog QPushButton, QMessageBox QPushButton {{
    background-color: {HOVER_BACKGROUND};
    color: {PRIMARY_TEXT};
    border: 1px solid {BORDER};
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
}}
#AddServerDialog QPushButton:hover, #FeedbackDialog QPushButton:hover, QMessageBox QPushButton:hover {{
    background-color: {DIALOG_HOVER_BACKGROUND};
}}

#AddServerDialog QPushButton#ConfirmButton, #FeedbackDialog QPushButton#OkButton {{
    background-color: {ACCENT_PRIMARY};
    color: {ACCENT_TEXT};
    border: none;
}}
#AddServerDialog QPushButton#ConfirmButton:hover, #FeedbackDialog QPushButton#OkButton:hover {{
    background-color: {ACCENT_PRIMARY_HOVER};
}}

#AddServerDialog QTextEdit, #FeedbackDialog QTextEdit {{
    background-color: {INPUT_BACKGROUND};
    border: 1px solid {BORDER};
    border-radius: 4px;
    color: {PRIMARY_TEXT};
    padding: 8px;
}}
#AddServerDialog QTextEdit:focus, #FeedbackDialog QTextEdit:focus {{
    border: 1px solid {ACCENT_PRIMARY};
}}

QMessageBox QCheckBox {{
    color: {MENU_TEXT};
    font-size: 13px;
    padding-top: 10px;
}}
"""


def get_stylesheet(theme: dict) -> str:
    """
    Generates the full stylesheet by formatting the template with the given theme's colors.
    """
    return STYLESHEET_TEMPLATE.format(**theme)
