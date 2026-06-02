"""Status badges panel."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget


class StatePanelWidget(QWidget):
    """Badge row for protocol status."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignLeft)

    def set_badges(self, badges: list[str]) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        badge_map = {
            "SENT": "sent",
            "RECEIVED": "received",
            "CORRECTED": "corrected",
            "ACK": "ack",
            "NACK": "nack",
            "RETRANSMITTED": "retransmitted",
            "DROPPED": "dropped",
        }
        for badge in badges:
            container = QFrame()
            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            label = QLabel(badge)
            label.setProperty("badge", badge_map.get(badge, "sent"))
            container_layout.addWidget(label)
            self.layout.addWidget(container)
