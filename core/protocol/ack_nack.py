"""ACK/NACK response models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AckNackResponse:
    accepted: bool
    code: str
    reason: str


def ack(reason: str = "Frame accepted") -> AckNackResponse:
    return AckNackResponse(True, "ACK", reason)


def nack(reason: str = "Frame rejected") -> AckNackResponse:
    return AckNackResponse(False, "NACK", reason)
