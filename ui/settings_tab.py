"""Application settings tab."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QDoubleSpinBox, QFormLayout, QGroupBox, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget

from app.config import AppSettings


class SettingsTab(QWidget):
    save_requested = Signal(AppSettings)

    def __init__(self, settings: AppSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        title = QLabel("Environment Defaults")
        title.setProperty("title", True)
        subtitle = QLabel("Persist the simulator defaults used for new sessions in VS Code and direct local runs.")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        box = QGroupBox("Default Simulator Settings")
        form = QFormLayout(box)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark"])
        self.theme_combo.setCurrentText(settings.theme)
        self.encryption_combo = QComboBox()
        self.encryption_combo.addItems(["AES", "Substitution"])
        self.coding_combo = QComboBox()
        self.coding_combo.addItems(["Hamming(7,4)", "CRC"])
        self.retry_input = QSpinBox()
        self.retry_input.setRange(0, 10)
        self.error_combo = QComboBox()
        self.error_combo.addItems(["No Error", "Random Single-Bit", "Random Multi-Bit", "Burst Error"])
        self.probability = QDoubleSpinBox()
        self.probability.setRange(0.0, 1.0)
        self.probability.setSingleStep(0.01)
        self.retry_input.setValue(settings.max_retries)
        self.encryption_combo.setCurrentText(settings.encryption_mode)
        self.coding_combo.setCurrentText(settings.coding_mode)
        self.error_combo.setCurrentText(settings.error_mode)
        self.probability.setValue(settings.error_probability)
        form.addRow("Theme", self.theme_combo)
        form.addRow("Encryption Mode", self.encryption_combo)
        form.addRow("Coding Mode", self.coding_combo)
        form.addRow("Default Retry Limit", self.retry_input)
        form.addRow("Default Error Model", self.error_combo)
        form.addRow("Default Error Probability", self.probability)
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self._emit_save)
        form.addRow(self.save_button)
        layout.addWidget(box)
        layout.addStretch()

    def _emit_save(self) -> None:
        self.save_requested.emit(
            AppSettings(
                theme=self.theme_combo.currentText(),
                encryption_mode=self.encryption_combo.currentText(),
                coding_mode=self.coding_combo.currentText(),
                error_mode=self.error_combo.currentText(),
                error_probability=self.probability.value(),
                max_retries=self.retry_input.value(),
            )
        )
