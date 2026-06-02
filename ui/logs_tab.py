"""Logs tab."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from ui.widgets.log_console_widget import LogConsoleWidget


class LogsTab(QWidget):
    clear_requested = Signal()
    export_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        title = QLabel("Protocol Event Log")
        title.setProperty("title", True)
        subtitle = QLabel("Search timestamped events across send, receive, error, correction, ACK, NACK, and retransmission transitions.")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        controls = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter logs by packet ID, event type, or message")
        self.clear_button = QPushButton("Clear Logs")
        self.clear_button.setProperty("secondary", True)
        self.export_button = QPushButton("Export Logs")
        controls.addWidget(self.search)
        controls.addWidget(self.clear_button)
        controls.addWidget(self.export_button)
        layout.addLayout(controls)
        self.console = LogConsoleWidget()
        layout.addWidget(self.console)
        self.search.textChanged.connect(lambda: self.console.set_logs(self._logs, self.search.text()))
        self.clear_button.clicked.connect(self.clear_requested.emit)
        self.export_button.clicked.connect(self.export_requested.emit)
        self._logs: list[dict] = []

    def set_logs(self, logs: list[dict]) -> None:
        self._logs = logs
        self.console.set_logs(logs, self.search.text())
