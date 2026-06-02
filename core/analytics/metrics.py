"""Session metrics aggregation."""

from __future__ import annotations

from dataclasses import dataclass

from core.models.simulation_result import ExperimentResult, SimulationResult


@dataclass(slots=True)
class MetricsSnapshot:
    total_packets_sent: int = 0
    packets_received_successfully: int = 0
    retransmissions_count: int = 0
    detected_errors: int = 0
    corrected_errors: int = 0
    dropped_packets: int = 0
    success_rate: float = 0.0
    error_rate: float = 0.0
    average_retries_per_packet: float = 0.0


class MetricsCalculator:
    """Maintain aggregate metrics across sessions."""

    def __init__(self) -> None:
        self.simulations: list[SimulationResult] = []
        self.experiments: list[ExperimentResult] = []

    def add_simulation(self, result: SimulationResult) -> None:
        self.simulations.append(result)

    def set_experiments(self, results: list[ExperimentResult]) -> None:
        self.experiments = results

    def snapshot(self) -> MetricsSnapshot:
        total = len(self.simulations)
        if total == 0:
            return MetricsSnapshot()
        successes = sum(1 for item in self.simulations if item.success)
        retransmissions = sum(item.packet.retries for item in self.simulations)
        detected_errors = sum(item.packet.detected_errors for item in self.simulations)
        corrected_errors = sum(item.packet.corrected_errors for item in self.simulations)
        dropped = sum(1 for item in self.simulations if item.packet.dropped)
        return MetricsSnapshot(
            total_packets_sent=total,
            packets_received_successfully=successes,
            retransmissions_count=retransmissions,
            detected_errors=detected_errors,
            corrected_errors=corrected_errors,
            dropped_packets=dropped,
            success_rate=successes / total,
            error_rate=detected_errors / total,
            average_retries_per_packet=retransmissions / total,
        )

    def to_rows(self) -> list[dict]:
        snapshot = self.snapshot()
        return [snapshot.__dict__]
