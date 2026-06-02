"""Frame analysis workspace."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QFrame, QGroupBox, QLabel, QPlainTextEdit, QVBoxLayout, QWidget, QHBoxLayout

from core.models.packet import Packet
from ui.widgets.frame_viewer_widget import FrameViewerWidget


class FrameAnalysisTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        viewer_card = QFrame()
        viewer_card.setProperty("panel", True)
        viewer_layout = QVBoxLayout(viewer_card)
        viewer_title = QLabel("Binary Frame Inspector")
        viewer_title.setProperty("section", True)
        viewer_layout.addWidget(viewer_title)
        self.viewer = FrameViewerWidget()
        viewer_layout.addWidget(self.viewer)
        layout.addWidget(viewer_card, 5)

        sidebar = QVBoxLayout()
        self.meta_box = QGroupBox("Frame Metadata")
        meta_layout = QFormLayout(self.meta_box)
        self.packet_id = QLabel("-")
        self.mode = QLabel("-")
        self.length = QLabel("-")
        self.modified_count = QLabel("-")
        self.status_summary = QLabel("-")
        self.status_summary.setWordWrap(True)
        meta_layout.addRow("Packet ID", self.packet_id)
        meta_layout.addRow("Modes", self.mode)
        meta_layout.addRow("Frame Length", self.length)
        meta_layout.addRow("Bit Modifications", self.modified_count)
        meta_layout.addRow("Receiver Status", self.status_summary)

        self.detail_box = QGroupBox("Validation Detail")
        detail_layout = QVBoxLayout(self.detail_box)
        self.syndrome_view = QPlainTextEdit()
        self.syndrome_view.setReadOnly(True)
        self.syndrome_view.setProperty("mono", True)
        self.syndrome_view.setMinimumHeight(90)
        self.syndrome_view.setMaximumHeight(110)
        self.crc_label = QLabel("-")
        self.crc_label.setWordWrap(True)
        detail_layout.addWidget(QLabel("Hamming Syndrome"))
        detail_layout.addWidget(self.syndrome_view)
        detail_layout.addWidget(QLabel("CRC Remainder"))
        detail_layout.addWidget(self.crc_label)

        legend = QFrame()
        legend.setProperty("panel", True)
        legend_layout = QVBoxLayout(legend)
        legend_title = QLabel("Highlight Legend")
        legend_title.setProperty("section", True)
        legend_layout.addWidget(legend_title)
        for text, color in (
            ("Parity positions", "#6ca8ff"),
            ("Bits altered by channel", "#ff5573"),
            ("Bits corrected at receiver", "#ffd166"),
        ):
            item = QLabel(text)
            item.setStyleSheet(f"color: {color}; font-weight: 700;")
            legend_layout.addWidget(item)
        legend_layout.addStretch()

        sidebar.addWidget(self.meta_box)
        sidebar.addWidget(self.detail_box)
        sidebar.addWidget(legend)
        sidebar.addStretch()
        layout.addLayout(sidebar, 3)
        self.update_analysis_dummy()

    def update_analysis(
        self,
        packet: Packet,
        analysis: dict,
        corrupted_indexes: list[int] | None = None,
        corrected_indexes: list[int] | None = None,
    ) -> None:
        corrupted_indexes = corrupted_indexes or []
        corrected_indexes = corrected_indexes or []
        self.viewer.set_frame(
            packet.noisy_frame_bits or packet.encoded_frame_bits,
            parity_indexes=analysis.get("parity_indexes", []),
            corrupted_indexes=corrupted_indexes,
            corrected_indexes=corrected_indexes,
        )
        self.packet_id.setText(packet.packet_id)
        self.mode.setText(f"{packet.encryption_mode} + {packet.coding_mode}")
        self.length.setText(str(analysis.get("frame_length", len(packet.encoded_frame_bits))))
        self.modified_count.setText(str(len(analysis.get("modified_indexes", corrupted_indexes))))
        self.status_summary.setText(analysis.get("status_summary", "-") or "-")
        self.syndrome_view.setPlainText(analysis.get("syndrome", "-") or "-")
        self.crc_label.setText(analysis.get("crc_remainder", "-") or "-")

    def update_analysis_dummy(self) -> None:
        self.viewer.setPlainText("")
        self.packet_id.setText("-")
        self.mode.setText("-")
        self.length.setText("-")
        self.modified_count.setText("-")
        self.status_summary.setText("Awaiting frame data.")
        self.syndrome_view.setPlainText("-")
        self.crc_label.setText("-")
