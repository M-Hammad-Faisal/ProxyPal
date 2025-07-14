from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer


def create_icon(svg_path: str, color: str) -> QIcon:
    """
    Creates a QIcon from an SVG path string, allowing it to be recolored.

    Args:
        svg_path: A string containing the SVG path data (the 'd' attribute).
        color: The desired color for the icon (e.g., "#000000").

    Returns:
        A QIcon object.
    """
    svg_data = f"""
    <svg width="24" height="24" viewBox="0 0 24 24" xmlns="[http://www.w3.org/2000/svg](http://www.w3.org/2000/svg)">
      <path d='{svg_path}' fill='{color}'/>
    </svg>
    """
    renderer = QSvgRenderer(svg_data.encode('utf-8'))
    pixmap = QPixmap(renderer.defaultSize())
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


# Icon paths
ADD_ICON_PATH = "M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"
MORE_VERT_ICON_PATH = "M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
FEEDBACK_ICON_PATH = "M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"
CONTACT_ICON_PATH = "M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"
