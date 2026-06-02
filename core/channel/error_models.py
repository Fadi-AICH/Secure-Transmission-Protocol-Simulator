"""Error mode enumeration."""

from __future__ import annotations

from enum import Enum


class ErrorMode(str, Enum):
    NONE = "No Error"
    SINGLE = "Random Single-Bit"
    MULTI = "Random Multi-Bit"
    BURST = "Burst Error"
