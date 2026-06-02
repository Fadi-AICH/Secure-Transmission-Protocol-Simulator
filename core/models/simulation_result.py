"""Simulation and experiment result models."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.models.packet import Packet


@dataclass(slots=True)
class TransmissionAttemptResult:
    """Details for a single attempt."""

    attempt_number: int
    success: bool
    ack: bool
    detected_errors: int
    corrected_errors: int
    noisy_indexes: list[int] = field(default_factory=list)
    notes: str = ""


@dataclass(slots=True)
class SimulationResult:
    """Complete result for a transmission session."""

    packet: Packet
    success: bool
    protocol_summary: str
    attempts: list[TransmissionAttemptResult] = field(default_factory=list)
    logs: list[dict] = field(default_factory=list)


@dataclass(slots=True)
class ExperimentResult:
    """Aggregate results for experiment mode."""

    encryption_mode: str
    coding_mode: str
    runs: int
    successes: int
    dropped: int
    retransmissions: int
    detected_errors: int
    corrected_errors: int
    average_retries: float
