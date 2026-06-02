"""Utility helpers for cryptography modules."""

from __future__ import annotations

import base64


def to_b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def from_b64(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def bytes_to_bitstring(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)


def bitstring_to_bytes(bits: str) -> bytes:
    if len(bits) % 8 != 0:
        bits += "0" * (8 - len(bits) % 8)
    return bytes(int(bits[index:index + 8], 2) for index in range(0, len(bits), 8))
