"""Batch experiment runner for configuration comparisons."""

from __future__ import annotations

from itertools import product

from core.analytics.metrics import MetricsCalculator
from core.models.simulation_result import ExperimentResult
from core.protocol.transmission_controller import TransmissionConfig, TransmissionController
from core.services.logger_service import LoggerService


class ExperimentRunner:
    """Run repeated protocol experiments across mode combinations."""

    def __init__(self) -> None:
        self.controller = TransmissionController(LoggerService())

    def run(self, message: str, error_mode: str, error_probability: float, max_retries: int, runs: int, seed: int | None) -> list[ExperimentResult]:
        results: list[ExperimentResult] = []
        for encryption_mode, coding_mode in product(("AES", "Substitution"), ("Hamming(7,4)", "CRC")):
            metrics = MetricsCalculator()
            for index in range(runs):
                config = TransmissionConfig(
                    plaintext=message,
                    encryption_mode=encryption_mode,
                    coding_mode=coding_mode,
                    error_mode=error_mode,
                    error_probability=error_probability,
                    random_seed=None if seed is None else seed + index,
                    max_retries=max_retries,
                )
                simulation, _, _ = self.controller.run(config)
                metrics.add_simulation(simulation)
            snapshot = metrics.snapshot()
            results.append(
                ExperimentResult(
                    encryption_mode=encryption_mode,
                    coding_mode=coding_mode,
                    runs=runs,
                    successes=snapshot.packets_received_successfully,
                    dropped=snapshot.dropped_packets,
                    retransmissions=snapshot.retransmissions_count,
                    detected_errors=snapshot.detected_errors,
                    corrected_errors=snapshot.corrected_errors,
                    average_retries=snapshot.average_retries_per_packet,
                )
            )
        return results
