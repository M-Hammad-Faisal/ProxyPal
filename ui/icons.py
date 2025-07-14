from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QSize


def create_icon(svg_data: str, size: int = 24):
    renderer = QSvgRenderer(svg_data.encode('utf-8'))
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(QColor("transparent"))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


def create_filled_icon(svg_path: str, color: str, size: int = 24) -> QIcon:
    """
    Creates a standard, solid-filled QIcon from an SVG path.

    Args:
        svg_path: The SVG path data.
        color: The color for the icon's fill.
        size: The desired width and height of the icon.
    """
    svg_data = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d='{svg_path}' fill='{color}'/>
    </svg>
    """
    return create_icon(svg_data, size)


def create_outlined_icon(svg_path: str, color: str, size: int = 24) -> QIcon:
    """
    Creates a bold, outlined QIcon from an SVG path using a thick stroke.

    Args:
        svg_path: The SVG path data.
        color: The color for the icon's outline.
        size: The desired width and height of the icon.
    """
    stroke_width = 2.0
    svg_data = f"""
    <svg width="{size}" height="{size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d='{svg_path}' fill='none' stroke='{color}' stroke-width='{stroke_width}' stroke-linecap='round' stroke-linejoin='round'/>
    </svg>
    """
    return create_icon(svg_data, size)


# Icon paths
APP_ICON_PATH = "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"
TRAY_ICON_CONNECTED = "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"
TRAY_ICON_DISCONNECTED = "M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.29L19 6.3v4.7c0 4.52-2.98 8.69-7 9.93-4.02-1.24-7-5.41-7-9.93V6.3l7-3.01z"
ADD_ICON_PATH = "M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"
MORE_VERT_ICON_PATH = "M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
FEEDBACK_ICON_PATH = "M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"
CONTACT_ICON_PATH = "M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"
ONBOARDING_ICON_PATH = "M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"
