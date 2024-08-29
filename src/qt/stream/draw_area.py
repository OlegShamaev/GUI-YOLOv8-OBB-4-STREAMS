from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRect


class BoxArea(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.pixmap = None
        self.original_rect = None
        self.rect = None
        self.dragging = False
        self.resizing = False
        self.resize_corner = None
        self.shift_pressed = False
        self.margin = 10  # Отступ от границ изображения
        self.show_rect = False  # Управление видимостью прямоугольника

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.setPixmap(self.pixmap)
        if self.original_rect is None:
            self.original_rect = QRect(
                self.pixmap.width() // 4,
                self.pixmap.height() // 4,
                self.pixmap.width() // 2,
                self.pixmap.height() // 2,
            )
            self.rect = self.original_rect
        self.update()

    def toggle_rect(self, show):
        """Включает или выключает отображение прямоугольника."""
        self.show_rect = show
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.show_rect and self.rect:
            painter = QPainter(self)
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        if self.show_rect and event.button() == Qt.MouseButton.LeftButton:
            if self.rect.contains(event.pos()):
                self.dragging = True
                self.last_pos = event.pos()
            elif self.get_resize_corner(event.pos()):
                self.resizing = True
                self.resize_corner = self.get_resize_corner(event.pos())
                self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.show_rect:
            if self.dragging:
                delta = event.pos() - self.last_pos
                new_rect = self.rect.translated(delta)
                if self.is_valid_rect(new_rect):
                    self.rect = self.ensure_in_bounds(new_rect)
                    self.last_pos = event.pos()
                    self.update()
            elif self.resizing:
                delta = event.pos() - self.last_pos
                new_rect = self.rect
                if self.resize_corner == "top_left":
                    new_rect.setTopLeft(new_rect.topLeft() + delta)
                elif self.resize_corner == "top_right":
                    new_rect.setTopRight(new_rect.topRight() + delta)
                elif self.resize_corner == "bottom_left":
                    new_rect.setBottomLeft(new_rect.bottomLeft() + delta)
                elif self.resize_corner == "bottom_right":
                    new_rect.setBottomRight(new_rect.bottomRight() + delta)
                self.rect = self.ensure_in_bounds(new_rect)
                self.last_pos = event.pos()
                self.update()

    def mouseReleaseEvent(self, event):
        if self.show_rect and event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_corner = None

    def get_resize_corner(self, pos):
        corners = {
            "top_left": self.rect.topLeft(),
            "top_right": self.rect.topRight(),
            "bottom_left": self.rect.bottomLeft(),
            "bottom_right": self.rect.bottomRight(),
        }
        for corner, point in corners.items():
            if (point - pos).manhattanLength() < 10:
                return corner
        return None

    def is_valid_rect(self, rect):
        return rect.width() > 0 and rect.height() > 0

    def ensure_in_bounds(self, rect):
        rect.setLeft(max(self.margin, rect.left()))
        rect.setTop(max(self.margin, rect.top()))
        rect.setRight(min(self.pixmap.width() - self.margin, rect.right()))
        rect.setBottom(min(self.pixmap.height() - self.margin, rect.bottom()))
        return rect

    def get_relative_corners(self):
        if not self.show_rect:
            return None

        width = self.pixmap.width()
        height = self.pixmap.height()
        return {
            "top_left": (self.rect.left() / width, self.rect.top() / height),
            "top_right": (self.rect.right() / width, self.rect.top() / height),
            "bottom_right": (self.rect.right() / width, self.rect.bottom() / height),
            "bottom_left": (self.rect.left() / width, self.rect.bottom() / height),
        }

    def get_abs_corners(self):
        if not self.show_rect:
            return None

        return [
            (self.rect.left(), self.rect.top()),
            (self.rect.right(), self.rect.top()),
            (self.rect.right(), self.rect.bottom()),
            (self.rect.left(), self.rect.bottom()),
        ]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # Сброс прямоугольника в исходное положение
            self.rect = self.original_rect
            self.update()
        else:
            super().keyPressEvent(event)

    def reset_rect_to_original(self):
        # Возвращает прямоугольник в исходное положение
        self.rect = self.original_rect
        self.update()
