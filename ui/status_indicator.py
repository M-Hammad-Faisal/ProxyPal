from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import QPropertyAnimation, pyqtProperty, QEasingCurve


class PieStatusIndicator(QWidget):
    """A custom widget to draw a large, animated pie chart for connection status."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._connected = False
        self.setMinimumSize(200, 200)
        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setDuration(1200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360 * 16)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = min(self.width(), self.height())
        rect = self.rect().adjusted(
            int((self.width() - side) / 2),
            int((self.height() - side) / 2),
            int(-(self.width() - side) / 2),
            int(-(self.height() - side) / 2)
        ).adjusted(20, 20, -20, -20)

        if self._connected:
            color = QColor("#00BFA5")
        else:
            color = QColor("#BDBDBD")

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color, 2))
        painter.drawPie(rect, 90 * 16, -self._angle)

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()

    def set_connected(self, connected):
        self._connected = connected
        self.animation.setDirection(
            QPropertyAnimation.Direction.Forward if connected else QPropertyAnimation.Direction.Backward
        )
        if self.animation.state() != QPropertyAnimation.State.Running:
            self.animation.start()
