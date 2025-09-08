from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QWheelEvent
from PyQt5.QtCore import Qt


class GraphView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        # Scrolling
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Panning
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # Zoom by pinch
        self.grabGesture(Qt.PinchGesture)

        # Defining Zoom Limits
        self.min_zoom = 0.5  # 50% zoom
        self.max_zoom = 3.0  # 300% zoom
        self.current_zoom = 1.0  # Default zoom level

    def wheelEvent(self, event: QWheelEvent):
        zoom_factor = 1.2 if event.angleDelta().y() > 0 else 1/1.2
        self.apply_zoom(zoom_factor)

    def event(self, event):
        if event.type() == 197:
            return self.gestureEvent(event)
        return super().event(event)

    def gestureEvent(self, event):
        gesture = event.gesture(Qt.PinchGesture)
        if gesture:
            scale_factor = gesture.scaleFactor()
            self.apply_zoom(scale_factor)
            return True
        return False

    def apply_zoom(self, factor):
        new_zoom = self.current_zoom * factor
        if self.min_zoom <= new_zoom <= self.max_zoom:
            self.scale(factor, factor)
            self.current_zoom = new_zoom


