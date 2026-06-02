"""Statistics and charts."""

from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from core.analytics.charts import ChartFactory
from core.analytics.metrics import MetricsSnapshot
from core.models.simulation_result import ExperimentResult, SimulationResult
from ui.widgets.metric_cards_widget import MetricCardsWidget


class StatisticsTab(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.chart_factory = ChartFactory()
        layout = QVBoxLayout(self)
        title = QLabel("Network Reliability Dashboard")
        title.setProperty("title", True)
        subtitle = QLabel("Packet outcomes, recovery behavior, and experiment trends across the active session.")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.metrics_widget = MetricCardsWidget()
        layout.addWidget(self.metrics_widget)
        self.chart_grid = QGridLayout()
        self.chart_grid.setSpacing(12)
        layout.addLayout(self.chart_grid)
        self._canvases: list[FigureCanvasQTAgg] = []

    def update_statistics(self, snapshot: MetricsSnapshot, simulations: list[SimulationResult], experiments: list[ExperimentResult]) -> None:
        self.metrics_widget.update_metrics(snapshot)
        for canvas in self._canvases:
            canvas.setParent(None)
        self._canvases.clear()
        figures = [
            self.chart_factory.retransmissions_chart(simulations),
            self.chart_factory.error_correction_chart(snapshot),
            self.chart_factory.success_noise_chart(simulations),
            self.chart_factory.comparison_chart(experiments if experiments else []),
        ]
        for index, figure in enumerate(figures):
            canvas = FigureCanvasQTAgg(figure)
            self._canvases.append(canvas)
            card = QFrame()
            card.setProperty("chartCard", True)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(8, 8, 8, 8)
            card_layout.addWidget(canvas)
            row, column = divmod(index, 2)
            self.chart_grid.addWidget(card, row, column)
