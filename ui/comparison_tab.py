"""Experiment mode tab."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHeaderView,
    QLabel,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.models.simulation_result import ExperimentResult


class ComparisonTab(QWidget):
    run_requested = Signal(dict)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        title = QLabel("Experiment Matrix")
        title.setProperty("title", True)
        subtitle = QLabel("Compare encryption and coding combinations under controlled noise and retry limits.")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        controls = QGroupBox("Experiment Controls")
        form = QFormLayout(controls)
        self.message_input = QTextEdit("Comparison experiment payload")
        self.message_input.setMinimumHeight(80)
        self.error_probability = QDoubleSpinBox()
        self.error_probability.setRange(0.0, 1.0)
        self.error_probability.setDecimals(3)
        self.error_probability.setValue(0.08)
        self.runs_input = QSpinBox()
        self.runs_input.setRange(1, 500)
        self.runs_input.setValue(20)
        self.retries_input = QSpinBox()
        self.retries_input.setRange(0, 10)
        self.retries_input.setValue(3)
        self.seed_input = QSpinBox()
        self.seed_input.setRange(0, 999999)
        self.seed_input.setValue(42)
        self.mode_button = QPushButton("Run Comparison")
        self.mode_button.clicked.connect(self._emit_request)
        form.addRow("Message", self.message_input)
        form.addRow("Noise Probability", self.error_probability)
        form.addRow("Runs per Combo", self.runs_input)
        form.addRow("Max Retries", self.retries_input)
        form.addRow("Base Seed", self.seed_input)
        form.addRow(self.mode_button)
        layout.addWidget(controls)

        self.summary_strip = QLabel("Awaiting experiment run.")
        self.summary_strip.setProperty("subtitle", True)
        layout.addWidget(self.summary_strip)

        table_card = QFrame()
        table_card.setProperty("panel", True)
        table_layout = QVBoxLayout(table_card)
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels(
            ["Encryption", "Coding", "Runs", "Successes", "Dropped", "Retransmissions", "Detected", "Corrected", "Avg Retries"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        table_layout.addWidget(self.table)
        layout.addWidget(table_card)

    def _emit_request(self) -> None:
        self.run_requested.emit(
            {
                "message": self.message_input.toPlainText().strip(),
                "error_mode": "Random Multi-Bit",
                "error_probability": self.error_probability.value(),
                "max_retries": self.retries_input.value(),
                "runs": self.runs_input.value(),
                "seed": self.seed_input.value(),
            }
        )

    def set_results(self, results: list[ExperimentResult]) -> None:
        self.table.setRowCount(0)
        if not results:
            self.summary_strip.setText("No experiment data available yet.")
            return
        best = max(results, key=lambda item: item.successes)
        self.summary_strip.setText(
            f"Best reliability: {best.encryption_mode} + {best.coding_mode} with {best.successes}/{best.runs} successful deliveries."
        )
        for item in results:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [
                item.encryption_mode,
                item.coding_mode,
                item.runs,
                item.successes,
                item.dropped,
                item.retransmissions,
                item.detected_errors,
                item.corrected_errors,
                f"{item.average_retries:.2f}",
            ]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))
