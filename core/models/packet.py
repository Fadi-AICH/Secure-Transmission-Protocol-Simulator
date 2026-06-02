"""Packet and frame data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class FrameStage:
    """Named stage for packet data progression."""

    name: str
    bits: str
    description: str = ""
    highlighted_indexes: list[int] = field(default_factory=list)


@dataclass(slots=True)
class Packet:
    """Represents a protocol packet."""

    packet_id: str
    plaintext: str
    encryption_mode: str
    coding_mode: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    encrypted_payload_hex: str = ""
    encoded_frame_bits: str = ""
    noisy_frame_bits: str = ""
    validated_frame_bits: str = ""
    decrypted_message: str = ""
    failure_reason: str = ""
    ack: bool = False
    retries: int = 0
    detected_errors: int = 0
    corrected_errors: int = 0
    dropped: bool = False
    stages: list[FrameStage] = field(default_factory=list)
