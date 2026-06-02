"""Receiver-side validation, correction, and decryption."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.coding.bit_utils import bits_to_text
from core.coding.crc_codec import CRCCodec, CRCValidationResult
from core.coding.hamming74 import Hamming74Codec, HammingDecodeResult
from core.crypto.aes_cipher import AESCipher
from core.crypto.substitution_cipher import SubstitutionCipher
from core.models.packet import FrameStage, Packet
from core.protocol.ack_nack import AckNackResponse, ack, nack


@dataclass(slots=True)
class ReceiverOutput:
    response: AckNackResponse
    packet: Packet
    syndrome: str = ""
    crc_remainder: str = ""
    corrected_indexes: list[int] = field(default_factory=list)


class Receiver:
    """Validate received frames and recover messages."""

    def __init__(self) -> None:
        self.aes = AESCipher()
        self.substitution = SubstitutionCipher()
        self.hamming = Hamming74Codec()
        self.crc = CRCCodec()

    def receive(self, packet: Packet, frame_bits: str, padding: int) -> ReceiverOutput:
        corrected_indexes: list[int] = []
        if packet.coding_mode == "Hamming(7,4)":
            result: HammingDecodeResult = self.hamming.decode(frame_bits, padding=padding)
            packet.validated_frame_bits = result.corrected_frame
            packet.detected_errors += int(result.detected)
            packet.corrected_errors += int(result.corrected)
            corrected_indexes = result.corrected_indexes
            packet.stages.append(FrameStage("Validated Frame", result.corrected_frame, "Hamming-decoded frame", corrected_indexes))
            try:
                payload_text = bits_to_text(result.data_bits, encoding="ascii", errors="strict")
            except UnicodeDecodeError:
                packet.failure_reason = "Recovered payload is not valid transport ASCII after Hamming correction."
                return ReceiverOutput(
                    response=nack(packet.failure_reason),
                    packet=packet,
                    syndrome=result.syndrome,
                    corrected_indexes=corrected_indexes,
                )
            response = ack("Hamming corrected or accepted frame")
            syndrome = result.syndrome
            crc_remainder = ""
        else:
            result_crc: CRCValidationResult = self.crc.validate(frame_bits)
            packet.validated_frame_bits = frame_bits
            packet.detected_errors += int(not result_crc.valid)
            packet.stages.append(FrameStage("Validated Frame", frame_bits, "CRC validation frame"))
            if not result_crc.valid:
                packet.failure_reason = "CRC detected corrupted frame."
                return ReceiverOutput(response=nack(packet.failure_reason), packet=packet, crc_remainder=result_crc.remainder)
            try:
                payload_text = bits_to_text(result_crc.data_bits, encoding="ascii", errors="strict")
            except UnicodeDecodeError:
                packet.failure_reason = "Recovered payload is not valid transport ASCII after CRC validation."
                return ReceiverOutput(response=nack(packet.failure_reason), packet=packet, crc_remainder=result_crc.remainder)
            response = ack("CRC accepted frame")
            syndrome = ""
            crc_remainder = result_crc.remainder

        if response.accepted:
            try:
                packet.decrypted_message = self._decrypt(payload_text, packet.encryption_mode)
                packet.stages.append(FrameStage("Decrypted Message", packet.decrypted_message, "Receiver output"))
            except Exception as exc:
                packet.failure_reason = f"Decryption failed: {exc}"
                return ReceiverOutput(
                    response=nack(packet.failure_reason),
                    packet=packet,
                    syndrome=syndrome,
                    crc_remainder=crc_remainder,
                    corrected_indexes=corrected_indexes,
                )
        return ReceiverOutput(response=response, packet=packet, syndrome=syndrome, crc_remainder=crc_remainder, corrected_indexes=corrected_indexes)

    def _decrypt(self, payload: str, mode: str) -> str:
        if mode == "AES":
            return self.aes.decrypt(payload)
        return self.substitution.decrypt(payload)
