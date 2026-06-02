"""Structured in-memory event logging."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(slots=True)
class LogEntry:
    timestamp: str
    packet_id: str
    event_type: str
    message: str
    details: dict


class LoggerService:
    """Collect timestamped protocol log entries."""

    def __init__(self) -> None:
        self._entries: list[LogEntry] = []

    def log(self, packet_id: str, event_type: str, message: str, **details: object) -> LogEntry:
        entry = LogEntry(
            timestamp=datetime.utcnow().isoformat(timespec="seconds"),
            packet_id=packet_id,
            event_type=event_type,
            message=message,
            details=details,
        )
        self._entries.append(entry)
        return entry

    def clear(self) -> None:
        self._entries.clear()

    def entries(self) -> list[LogEntry]:
        return list(self._entries)

    def serialize(self) -> list[dict]:
        return [asdict(entry) for entry in self._entries]
