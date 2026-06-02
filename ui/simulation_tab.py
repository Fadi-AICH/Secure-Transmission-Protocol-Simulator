"""Simulation control dashboard."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.models.packet import Packet
from core.models.protocol_state import ProtocolState
from ui.widgets.pipeline_widget import PipelineWidget
from ui.widgets.state_panel_widget import StatePanelWidget


class SimulationTab(QWidget):
    simulate_requested = Signal(dict)
    reset_requested = Signal()

    def __init__(self, defaults: dict, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        root = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(12, 12, 12, 12)
        self.content_layout.setSpacing(12)
        scroll.setWidget(content)
        root.addWidget(scroll)

        hero = QFrame()
        hero.setProperty("hero", True)
        hero_layout = QVBoxLayout(hero)
        title = QLabel("Secure Transmission Control Room")
        title.setProperty("title", True)
        subtitle = QLabel("Model encrypted message delivery, channel corruption, receiver behavior, and retransmission outcomes.")
        subtitle.setProperty("subtitle", True)
        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        self.content_layout.addWidget(hero)

        top = QHBoxLayout()
        top.setSpacing(12)
        top.addWidget(self._build_controls(defaults), 3)
        top.addWidget(self._build_overview(), 4)
        self.content_layout.addLayout(top)
        self.content_layout.addWidget(self._build_stages())

    def _build_controls(self, defaults: dict) -> QGroupBox:
        box = QGroupBox("Simulation Controls")
        layout = QFormLayout(box)
        layout.setSpacing(10)
        self.plaintext_input = QTextEdit()
        self.plaintext_input.setPlainText(defaults["demo_message"])
        self.plaintext_input.setMinimumHeight(72)
        self.encryption_combo = QComboBox()
        self.encryption_combo.addItems(["AES", "Substitution"])
        self.encryption_combo.setCurrentText(defaults["encryption_mode"])
        self.coding_combo = QComboBox()
        self.coding_combo.addItems(["Hamming(7,4)", "CRC"])
        self.coding_combo.setCurrentText(defaults["coding_mode"])
        self.error_combo = QComboBox()
        self.error_combo.addItems(["No Error", "Random Single-Bit", "Random Multi-Bit", "Burst Error"])
        self.error_combo.setCurrentText(defaults["error_mode"])
        self.error_probability = QDoubleSpinBox()
        self.error_probability.setRange(0.0, 1.0)
        self.error_probability.setDecimals(3)
        self.error_probability.setSingleStep(0.01)
        self.error_probability.setValue(defaults["error_probability"])
        self.seed_input = QLineEdit("" if defaults["random_seed"] is None else str(defaults["random_seed"]))
        self.seed_input.setValidator(QIntValidator(0, 999999999, self))
        self.seed_input.setPlaceholderText("Optional deterministic seed")
        self.retry_input = QSpinBox()
        self.retry_input.setRange(0, 10)
        self.retry_input.setValue(defaults["max_retries"])
        layout.addRow("Plaintext Message", self.plaintext_input)
        layout.addRow("Encryption Mode", self.encryption_combo)
        layout.addRow("Coding Mode", self.coding_combo)
        layout.addRow("Channel Error Mode", self.error_combo)
        layout.addRow("Error Probability", self.error_probability)
        layout.addRow("Random Seed", self.seed_input)
        layout.addRow("Max Retransmissions", self.retry_input)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        self.send_button = QPushButton("Send")
        self.step_button = QPushButton("Step-by-Step")
        self.auto_button = QPushButton("Auto-Run")
        self.reset_button = QPushButton("Reset")
        self.reset_button.setProperty("secondary", True)
        for button in (self.send_button, self.step_button, self.auto_button, self.reset_button):
            buttons.addWidget(button)
        layout.addRow(buttons)

        self.send_button.clicked.connect(self._emit_request)
        self.step_button.clicked.connect(self._emit_request)
        self.auto_button.clicked.connect(self._emit_request)
        self.reset_button.clicked.connect(self.reset_requested.emit)
        return box

    def _build_overview(self) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)
        self.state_panel = StatePanelWidget()
        status_card = QFrame()
        status_card.setProperty("panel", True)
        status_layout = QVBoxLayout(status_card)
        status_title = QLabel("Protocol Status")
        status_title.setProperty("section", True)
        self.summary_label = QLabel("Awaiting first transmission.")
        self.summary_label.setProperty("subtitle", True)
        status_layout.addWidget(status_title)
        status_layout.addWidget(self.state_panel)
        status_layout.addWidget(self.summary_label)
        self.pipeline = PipelineWidget()
        layout.addWidget(status_card)
        layout.addWidget(self.pipeline)
        return container

    def _build_stages(self) -> QGroupBox:
        box = QGroupBox("Transmission Stages")
        layout = QGridLayout(box)
        layout.setSpacing(12)
        self.original_view = self._build_mono_view(False)
        self.encrypted_view = self._build_mono_view(True)
        self.encoded_view = self._build_mono_view(True)
        self.noisy_view = self._build_mono_view(True)
        self.validated_view = self._build_mono_view(True)
        self.final_view = self._build_mono_view(False)
        labels = [
            ("Original Plaintext", self.original_view),
            ("Encrypted Payload", self.encrypted_view),
            ("Encoded Frame", self.encoded_view),
            ("Noisy Frame", self.noisy_view),
            ("Corrected / Validated Frame", self.validated_view),
            ("Final Decrypted Message", self.final_view),
        ]
        for index, (label, widget) in enumerate(labels):
            row, column = divmod(index, 2)
            group = QGroupBox(label)
            group_layout = QVBoxLayout(group)
            group_layout.addWidget(widget)
            layout.addWidget(group, row, column)
        return box

    def _build_mono_view(self, mono: bool) -> QTextEdit:
        widget = QTextEdit()
        widget.setReadOnly(True)
        widget.setMinimumHeight(92)
        if mono:
            widget.setProperty("mono", True)
        return widget

    def _emit_request(self) -> None:
        seed_text = self.seed_input.text().strip()
        payload = {
            "plaintext": self.plaintext_input.toPlainText().strip(),
            "encryption_mode": self.encryption_combo.currentText(),
            "coding_mode": self.coding_combo.currentText(),
            "error_mode": self.error_combo.currentText(),
            "error_probability": self.error_probability.value(),
            "random_seed": int(seed_text) if seed_text else None,
            "max_retries": self.retry_input.value(),
        }
        self.simulate_requested.emit(payload)

    def update_result(self, packet: Packet, state: ProtocolState) -> None:
        self.original_view.setPlainText(packet.plaintext)
        self.encrypted_view.setPlainText(packet.encrypted_payload_hex)
        self.encoded_view.setPlainText(packet.encoded_frame_bits)
        self.noisy_view.setPlainText(packet.noisy_frame_bits)
        self.validated_view.setPlainText(packet.validated_frame_bits)
        self.final_view.setPlainText(packet.decrypted_message or packet.failure_reason)
        self.pipeline.update_states(state.sender_state, state.channel_state, state.receiver_state)
        self.state_panel.set_badges(state.badges)
        self.summary_label.setText(
            f"Packet {packet.packet_id} | Retries {packet.retries} | "
            f"Detected {packet.detected_errors} | Corrected {packet.corrected_errors}"
        )

    def reset(self) -> None:
        for widget in (
            self.original_view,
            self.encrypted_view,
            self.encoded_view,
            self.noisy_view,
            self.validated_view,
            self.final_view,
        ):
            widget.clear()
        self.summary_label.setText("Awaiting first transmission.")
        self.pipeline.update_states("Idle", "Idle", "Idle")
        self.state_panel.set_badges([])
