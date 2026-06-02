"""Helpers for bit and nibble conversions."""

from __future__ import annotations


def bytes_to_bits(data: bytes) -> str:
    return "".join(f"{byte:08b}" for byte in data)


def bits_to_bytes(bits: str) -> bytes:
    trimmed = bits[: len(bits) - len(bits) % 8]
    if not trimmed:
        return b""
    return bytes(int(trimmed[i:i + 8], 2) for i in range(0, len(trimmed), 8))


def text_to_bits(text: str, encoding: str = "utf-8") -> str:
    return bytes_to_bits(text.encode(encoding))


def bits_to_text(bits: str, encoding: str = "utf-8", errors: str = "strict") -> str:
    return bits_to_bytes(bits).decode(encoding, errors=errors)


def chunk_bits(bits: str, size: int) -> list[str]:
    return [bits[i:i + size] for i in range(0, len(bits), size)]


def xor_bit(a: str, b: str) -> str:
    return "1" if a != b else "0"


def pad_bits(bits: str, width: int) -> tuple[str, int]:
    padding = (width - (len(bits) % width)) % width
    return bits + ("0" * padding), padding
