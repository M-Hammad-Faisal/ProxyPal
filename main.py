import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import ProxyPalWindow
from ui.styles import STYLESHEET


def main():
    """
    The main entry point for the ProxyPal application.
    Initializes the Qt Application, applies the stylesheet,
    creates and shows the main window, and starts the event loop.
    """
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    window = ProxyPalWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
