"""Visual sender-channel-receiver pipeline."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QWidget


class PipelineWidget(QFrame):
    """Engineering-style pipeline overview."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("panel", True)
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(10)
        self.sender_label = self._build_node(layout, 0, "Sender", "Idle")
        self.channel_label = self._build_node(layout, 1, "Channel", "Idle")
        self.receiver_label = self._build_node(layout, 2, "Receiver", "Idle")

    def _build_node(self, layout: QGridLayout, column: int, title: str, value: str) -> QLabel:
        title_label = QLabel(title)
        title_label.setProperty("section", True)
        value_box = QFrame()
        value_box.setProperty("node", True)
        box_layout = QGridLayout(value_box)
        box_layout.setContentsMargins(16, 14, 16, 14)
        value_label = QLabel(value)
        value_label.setWordWrap(True)
        value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        box_layout.addWidget(value_label, 0, 0)
        arrow = QLabel("->" if column < 2 else "")
        arrow.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, 0, column * 2)
        layout.addWidget(value_box, 1, column * 2)
        if column < 2:
            layout.addWidget(arrow, 1, column * 2 + 1)
        return value_label

    def update_states(self, sender: str, channel: str, receiver: str) -> None:
        self.sender_label.setText(sender)
        self.channel_label.setText(channel)
        self.receiver_label.setText(receiver)
