"""Protocol state definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ProtocolStatus(str, Enum):
    IDLE = "IDLE"
    PREPARING = "PREPARING"
    SENT = "SENT"
    RECEIVED = "RECEIVED"
    CORRECTED = "CORRECTED"
    ACK = "ACK"
    NACK = "NACK"
    RETRANSMITTED = "RETRANSMITTED"
    DROPPED = "DROPPED"


@dataclass(slots=True)
class ProtocolState:
    """Runtime state of one simulated transmission."""

    packet_id: str = ""
    status: ProtocolStatus = ProtocolStatus.IDLE
    attempt: int = 0
    max_retries: int = 3
    sender_state: str = "Idle"
    channel_state: str = "Idle"
    receiver_state: str = "Idle"
    badges: list[str] = field(default_factory=list)
