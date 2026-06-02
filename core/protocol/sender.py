"""Sender-side frame preparation."""

from __future__ import annotations

from dataclasses import dataclass
import uuid

from core.coding.bit_utils import bytes_to_bits
from core.coding.crc_codec import CRCCodec
from core.coding.hamming74 import Hamming74Codec
from core.crypto.aes_cipher import AESCipher
from core.crypto.substitution_cipher import SubstitutionCipher
from core.models.packet import FrameStage, Packet


@dataclass(slots=True)
class SenderOutput:
    packet: Packet
    payload_text: str
    payload_bits: str
    padding: int


class Sender:
    """Prepare packets for transmission."""

    def __init__(self) -> None:
        self.aes = AESCipher()
        self.substitution = SubstitutionCipher()
        self.hamming = Hamming74Codec()
        self.crc = CRCCodec()

    def build_packet(self, plaintext: str, encryption_mode: str, coding_mode: str) -> SenderOutput:
        packet = Packet(
            packet_id=str(uuid.uuid4())[:8],
            plaintext=plaintext,
            encryption_mode=encryption_mode,
            coding_mode=coding_mode,
        )
        payload_text = self._encrypt(plaintext, encryption_mode)
        packet.encrypted_payload_hex = payload_text
        payload_bits = bytes_to_bits(payload_text.encode("ascii"))
        if coding_mode == "Hamming(7,4)":
            encoded, padding = self.hamming.encode(payload_bits)
        else:
            encoded = self.crc.encode(payload_bits)
            padding = 0
        packet.encoded_frame_bits = encoded
        packet.stages.extend([
            FrameStage("Plaintext", plaintext, "User payload"),
            FrameStage("Encrypted Payload", payload_text, f"{encryption_mode} output"),
            FrameStage("Encoded Frame", encoded, f"{coding_mode} protected frame"),
        ])
        return SenderOutput(packet=packet, payload_text=payload_text, payload_bits=payload_bits, padding=padding)

    def _encrypt(self, plaintext: str, mode: str) -> str:
        if mode == "AES":
            return self.aes.encrypt(plaintext)
        return self.substitution.encrypt(plaintext)
