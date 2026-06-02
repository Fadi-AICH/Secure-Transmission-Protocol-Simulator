"""Hamming (7,4) encoder and decoder."""

from __future__ import annotations

from dataclasses import dataclass

from core.coding.bit_utils import chunk_bits, pad_bits


@dataclass(slots=True)
class HammingDecodeResult:
    data_bits: str
    corrected_frame: str
    syndrome: str
    error_position: int | None
    corrected: bool
    detected: bool
    corrected_indexes: list[int]


class Hamming74Codec:
    """Encode and decode data using Hamming(7,4)."""

    parity_indexes = {0, 1, 3}

    def encode_nibble(self, nibble: str) -> str:
        d1, d2, d3, d4 = (int(bit) for bit in nibble)
        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p3 = d2 ^ d3 ^ d4
        return f"{p1}{p2}{d1}{p3}{d2}{d3}{d4}"

    def encode(self, bits: str) -> tuple[str, int]:
        padded_bits, padding = pad_bits(bits, 4)
        encoded = "".join(self.encode_nibble(chunk) for chunk in chunk_bits(padded_bits, 4))
        return encoded, padding

    def syndrome(self, frame: str) -> str:
        b = [int(bit) for bit in frame]
        s1 = b[0] ^ b[2] ^ b[4] ^ b[6]
        s2 = b[1] ^ b[2] ^ b[5] ^ b[6]
        s3 = b[3] ^ b[4] ^ b[5] ^ b[6]
        return f"{s3}{s2}{s1}"

    def decode_block(self, frame: str) -> HammingDecodeResult:
        syndrome = self.syndrome(frame)
        position = int(syndrome, 2)
        detected = position != 0
        bits = list(frame)
        corrected_indexes: list[int] = []
        corrected = False
        error_position: int | None = None
        if detected:
            error_position = position - 1
            if 0 <= error_position < 7:
                bits[error_position] = "0" if bits[error_position] == "1" else "1"
                corrected_indexes.append(error_position)
                corrected = True
        corrected_frame = "".join(bits)
        data_bits = "".join(corrected_frame[index] for index in (2, 4, 5, 6))
        return HammingDecodeResult(
            data_bits=data_bits,
            corrected_frame=corrected_frame,
            syndrome=syndrome,
            error_position=error_position,
            corrected=corrected,
            detected=detected,
            corrected_indexes=corrected_indexes,
        )

    def decode(self, bits: str, padding: int = 0) -> HammingDecodeResult:
        blocks = chunk_bits(bits, 7)
        decoded: list[str] = []
        corrected_frames: list[str] = []
        syndromes: list[str] = []
        corrected_indexes: list[int] = []
        detected = False
        corrected = False
        for block_index, block in enumerate(blocks):
            if len(block) != 7:
                continue
            result = self.decode_block(block)
            decoded.append(result.data_bits)
            corrected_frames.append(result.corrected_frame)
            syndromes.append(result.syndrome)
            detected = detected or result.detected
            corrected = corrected or result.corrected
            corrected_indexes.extend(index + block_index * 7 for index in result.corrected_indexes)
        decoded_bits = "".join(decoded)
        if padding:
            decoded_bits = decoded_bits[:-padding]
        return HammingDecodeResult(
            data_bits=decoded_bits,
            corrected_frame="".join(corrected_frames),
            syndrome=" ".join(syndromes),
            error_position=corrected_indexes[0] if corrected_indexes else None,
            corrected=corrected,
            detected=detected,
            corrected_indexes=corrected_indexes,
        )
