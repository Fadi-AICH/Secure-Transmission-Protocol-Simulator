"""Retransmission helpers."""

from __future__ import annotations


def should_retry(accepted: bool, attempt: int, max_retries: int) -> bool:
    return (not accepted) and attempt < max_retries
