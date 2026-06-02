"""Save and load simulator sessions."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from core.models.simulation_result import ExperimentResult, SimulationResult


class SessionService:
    """Serialize lightweight session snapshots."""

    def save_session(self, simulation: SimulationResult | None, experiments: list[ExperimentResult], path: str | Path) -> None:
        payload = {
            "simulation": None if simulation is None else {
                "packet_id": simulation.packet.packet_id,
                "plaintext": simulation.packet.plaintext,
                "decrypted_message": simulation.packet.decrypted_message,
                "success": simulation.success,
                "protocol_summary": simulation.protocol_summary,
                "attempts": [asdict(attempt) for attempt in simulation.attempts],
                "logs": simulation.logs,
            },
            "experiments": [asdict(result) for result in experiments],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_session(self, path: str | Path) -> dict:
        return json.loads(Path(path).read_text(encoding="utf-8"))
