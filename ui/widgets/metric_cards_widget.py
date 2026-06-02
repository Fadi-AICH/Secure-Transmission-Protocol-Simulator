"""Dashboard metric cards."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from core.analytics.metrics import MetricsSnapshot


class MetricCardsWidget(QWidget):
    """Responsive grid of metrics."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(12)
        self.cards: dict[str, QLabel] = {}
        labels = [
            "Total Packets",
            "Successful",
            "Retransmissions",
            "Detected Errors",
            "Corrected Errors",
            "Dropped",
            "Success Rate",
            "Average Retries",
        ]
        for index, label in enumerate(labels):
            card = QFrame()
            card.setProperty("metricCard", True)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(14, 14, 14, 14)
            title = QLabel(label)
            title.setProperty("metricLabel", True)
            value = QLabel("0")
            value.setProperty("metricValue", True)
            card_layout.addWidget(title)
            card_layout.addWidget(value)
            row, column = divmod(index, 4)
            self.layout.addWidget(card, row, column)
            self.cards[label] = value

    def update_metrics(self, snapshot: MetricsSnapshot) -> None:
        mapping = {
            "Total Packets": snapshot.total_packets_sent,
            "Successful": snapshot.packets_received_successfully,
            "Retransmissions": snapshot.retransmissions_count,
            "Detected Errors": snapshot.detected_errors,
            "Corrected Errors": snapshot.corrected_errors,
            "Dropped": snapshot.dropped_packets,
            "Success Rate": f"{snapshot.success_rate:.1%}",
            "Average Retries": f"{snapshot.average_retries_per_packet:.2f}",
        }
        for label, value in mapping.items():
            self.cards[label].setText(str(value))
