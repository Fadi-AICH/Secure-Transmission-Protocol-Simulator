"""About dialog."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("About Secure Transmission Protocol Simulator")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>Secure Transmission Protocol Simulator</h2>"))
        layout.addWidget(QLabel("A desktop engineering simulator for encrypted, coded, noisy transmission experiments."))
        layout.addWidget(QLabel("Built with PySide6, PyCryptodome, matplotlib, and pytest."))
