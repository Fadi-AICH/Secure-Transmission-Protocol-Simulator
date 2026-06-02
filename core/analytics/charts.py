"""Matplotlib chart builders."""

from __future__ import annotations

from matplotlib.figure import Figure

from core.analytics.metrics import MetricsSnapshot
from core.models.simulation_result import ExperimentResult, SimulationResult


class ChartFactory:
    """Generate matplotlib figures for the dashboard."""

    def retransmissions_chart(self, simulations: list[SimulationResult]) -> Figure:
        fig = Figure(figsize=(5, 3), facecolor="#121922")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#18212c")
        if not simulations:
            return self._empty_figure(fig, ax, "Retransmissions per Packet")
        ax.bar(range(1, len(simulations) + 1), [item.packet.retries for item in simulations], color="#f77f00")
        ax.set_title("Retransmissions per Packet", color="white")
        ax.set_xlabel("Packet", color="white")
        ax.set_ylabel("Retries", color="white")
        self._style_axes(ax)
        return fig

    def error_correction_chart(self, snapshot: MetricsSnapshot) -> Figure:
        fig = Figure(figsize=(5, 3), facecolor="#121922")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#18212c")
        if snapshot.total_packets_sent == 0:
            return self._empty_figure(fig, ax, "Detected vs Corrected Errors")
        ax.bar(["Detected", "Corrected"], [snapshot.detected_errors, snapshot.corrected_errors], color=["#d90429", "#e9c46a"])
        ax.set_title("Detected vs Corrected Errors", color="white")
        self._style_axes(ax)
        return fig

    def success_noise_chart(self, simulations: list[SimulationResult]) -> Figure:
        fig = Figure(figsize=(5, 3), facecolor="#121922")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#18212c")
        if not simulations:
            return self._empty_figure(fig, ax, "Success Trend")
        success_flags = [1 if item.success else 0 for item in simulations]
        ax.plot(range(1, len(simulations) + 1), success_flags, marker="o", color="#3fb950")
        ax.set_title("Success Trend", color="white")
        ax.set_xlabel("Simulation", color="white")
        ax.set_ylabel("Success", color="white")
        ax.set_ylim(-0.1, 1.1)
        self._style_axes(ax)
        return fig

    def comparison_chart(self, experiments: list[ExperimentResult]) -> Figure:
        fig = Figure(figsize=(6, 3), facecolor="#121922")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#18212c")
        if not experiments:
            return self._empty_figure(fig, ax, "Experiment Successes")
        labels = [f"{item.encryption_mode}\n{item.coding_mode}" for item in experiments]
        ax.bar(labels, [item.successes for item in experiments], color=["#1f6feb", "#2a9d8f", "#f77f00", "#e9c46a"])
        ax.set_title("Experiment Successes", color="white")
        ax.set_ylabel("Successful Runs", color="white")
        self._style_axes(ax)
        return fig

    def _style_axes(self, ax) -> None:
        ax.tick_params(colors="white")
        ax.grid(color="#243444", alpha=0.4, linestyle="--", linewidth=0.6, axis="y")
        for spine in ax.spines.values():
            spine.set_color("#5b708b")

    def _empty_figure(self, fig: Figure, ax, title: str) -> Figure:
        ax.set_title(title, color="white")
        ax.text(0.5, 0.5, "Run a simulation to populate this chart", ha="center", va="center", color="#8fa6bd")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#5b708b")
        return fig
