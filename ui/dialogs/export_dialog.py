"""Export options dialog."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QWidget


class ExportDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export Data")
        layout = QFormLayout(self)
        self.export_type = QComboBox()
        self.export_type.addItems(["Logs (.txt)", "Logs (.json)", "Statistics (.csv)", "Session (.json)"])
        layout.addRow("Export Type", self.export_type)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
