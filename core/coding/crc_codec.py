"""CRC frame generation and validation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CRCValidationResult:
    data_bits: str
    remainder: str
    valid: bool


class CRCCodec:
    """Bitwise CRC encoder/validator using a configurable polynomial."""

    def __init__(self, polynomial: str = "1101") -> None:
        self.polynomial = polynomial

    def _mod2div(self, dividend: str) -> str:
        pick = len(self.polynomial)
        tmp = list(dividend[:pick])
        divisor = list(self.polynomial)
        while pick < len(dividend):
            if tmp[0] == "1":
                tmp = [str(int(a != b)) for a, b in zip(tmp, divisor)]
            else:
                tmp = [str(int(a != b)) for a, b in zip(tmp, "0" * pick)]
            tmp.pop(0)
            tmp.append(dividend[pick])
            pick += 1
        if tmp[0] == "1":
            tmp = [str(int(a != b)) for a, b in zip(tmp, divisor)]
        else:
            tmp = [str(int(a != b)) for a, b in zip(tmp, "0" * pick)]
        return "".join(tmp[1:])

    def encode(self, data_bits: str) -> str:
        zeros = "0" * (len(self.polynomial) - 1)
        remainder = self._mod2div(data_bits + zeros)
        return data_bits + remainder

    def validate(self, frame_bits: str) -> CRCValidationResult:
        remainder = self._mod2div(frame_bits)
        valid = set(remainder) == {"0"} or remainder == ""
        data_bits = frame_bits[: -(len(self.polynomial) - 1)] if len(frame_bits) >= len(self.polynomial) - 1 else ""
        return CRCValidationResult(data_bits=data_bits, remainder=remainder, valid=valid)
