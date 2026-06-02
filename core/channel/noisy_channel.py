"""Configurable noisy channel."""

from __future__ import annotations

from dataclasses import dataclass
import random

from core.channel.error_models import ErrorMode


@dataclass(slots=True)
class ChannelResult:
    transmitted_bits: str
    modified_indexes: list[int]


class NoisyChannel:
    """Inject transmission errors into bitstrings."""

    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)

    def transmit(self, bits: str, mode: ErrorMode, probability: float) -> ChannelResult:
        if not bits or mode == ErrorMode.NONE or probability <= 0:
            return ChannelResult(bits, [])
        changed: set[int] = set()
        output = list(bits)

        def flip(index: int) -> None:
            output[index] = "0" if output[index] == "1" else "1"
            changed.add(index)

        if mode == ErrorMode.SINGLE:
            if self.random.random() < probability:
                flip(self.random.randrange(len(bits)))
        elif mode == ErrorMode.MULTI:
            for index in range(len(bits)):
                if self.random.random() < probability:
                    flip(index)
        elif mode == ErrorMode.BURST:
            if self.random.random() < probability:
                start = self.random.randrange(len(bits))
                burst_len = min(len(bits) - start, max(2, int(len(bits) * max(probability, 0.1))))
                for index in range(start, start + burst_len):
                    flip(index)
        return ChannelResult("".join(output), sorted(changed))
