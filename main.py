import sys
import subprocess
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QEvent

from ui.main_window import ProxyPalWindow
from ui.theme import LIGHT_THEME, DARK_THEME
from ui.styles import get_stylesheet


def is_dark_mode_macos() -> bool:
    """
    Checks if macOS is in dark mode using a shell command.
    Returns True for dark mode, False for light mode.
    """
    try:
        cmd = 'defaults read -g AppleInterfaceStyle'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return p.communicate()[0].decode('utf-8').strip() == 'Dark'
    except Exception:
        return False


class ThemedApplication(QApplication):
    """
    A custom QApplication subclass that detects and applies themes dynamically.
    """

    def __init__(self, argv):
        super().__init__(argv)
        self.apply_theme()

    def event(self, e: QEvent) -> bool:
        """
        Overrides the default event handler to watch for theme changes.
        """
        if e.type() == QEvent.Type.ApplicationPaletteChange:
            self.apply_theme()

        return super().event(e)

    def apply_theme(self):
        """
        Detects the current system theme and applies the corresponding stylesheet.
        """
        theme = DARK_THEME if is_dark_mode_macos() else LIGHT_THEME

        stylesheet = get_stylesheet(theme)
        self.setStyleSheet(stylesheet)

        self.setProperty("connectedColor", theme["PIE_CONNECTED"])
        self.setProperty("disconnectedColor", theme["PIE_DISCONNECTED"])


def main():
    """
    The main entry point for the ProxyPal application.
    """
    app = ThemedApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    window = ProxyPalWindow()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
