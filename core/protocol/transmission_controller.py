"""Orchestrate end-to-end transmission."""

from __future__ import annotations

from dataclasses import dataclass

from core.channel.error_models import ErrorMode
from core.channel.noisy_channel import NoisyChannel
from core.models.packet import FrameStage
from core.models.protocol_state import ProtocolState, ProtocolStatus
from core.models.simulation_result import SimulationResult, TransmissionAttemptResult
from core.protocol.receiver import Receiver
from core.protocol.retransmission import should_retry
from core.protocol.sender import Sender
from core.services.logger_service import LoggerService


@dataclass(slots=True)
class TransmissionConfig:
    plaintext: str
    encryption_mode: str
    coding_mode: str
    error_mode: str
    error_probability: float
    random_seed: int | None
    max_retries: int


class TransmissionController:
    """Main simulator controller."""

    def __init__(self, logger: LoggerService | None = None) -> None:
        self.sender = Sender()
        self.receiver = Receiver()
        self.logger = logger or LoggerService()

    def run(self, config: TransmissionConfig) -> tuple[SimulationResult, ProtocolState, dict]:
        self.logger.clear()
        sender_output = self.sender.build_packet(config.plaintext, config.encryption_mode, config.coding_mode)
        packet = sender_output.packet
        state = ProtocolState(
            packet_id=packet.packet_id,
            status=ProtocolStatus.PREPARING,
            attempt=0,
            max_retries=config.max_retries,
            sender_state="Frame ready",
            channel_state="Waiting",
            receiver_state="Waiting",
            badges=[],
        )
        self.logger.log(packet.packet_id, "prepare", "Packet prepared", encryption=config.encryption_mode, coding=config.coding_mode)
        attempt_results: list[TransmissionAttemptResult] = []
        analysis = {
            "syndrome": "",
            "crc_remainder": "",
            "padding": sender_output.padding,
            "parity_indexes": [],
            "frame_length": len(packet.encoded_frame_bits),
            "modified_indexes": [],
            "status_summary": "",
        }

        for attempt in range(config.max_retries + 1):
            state.attempt = attempt + 1
            state.status = ProtocolStatus.SENT
            state.sender_state = f"Attempt {attempt + 1}"
            state.channel_state = "Transmitting"
            packet.retries = attempt
            self.logger.log(packet.packet_id, "send", "Frame sent into channel", attempt=attempt + 1)

            channel = NoisyChannel(config.random_seed + attempt if config.random_seed is not None else None)
            channel_result = channel.transmit(
                packet.encoded_frame_bits,
                ErrorMode(config.error_mode),
                config.error_probability,
            )
            packet.noisy_frame_bits = channel_result.transmitted_bits
            packet.stages.append(
                FrameStage("Noisy Frame", channel_result.transmitted_bits, "Channel output", channel_result.modified_indexes)
            )
            state.channel_state = "Noise injected" if channel_result.modified_indexes else "Clean"
            self.logger.log(packet.packet_id, "channel", "Frame propagated through noisy channel", modified_indexes=channel_result.modified_indexes)

            receiver_output = self.receiver.receive(packet, channel_result.transmitted_bits, sender_output.padding)
            analysis["syndrome"] = receiver_output.syndrome
            analysis["crc_remainder"] = receiver_output.crc_remainder
            analysis["parity_indexes"] = [0, 1, 3] if config.coding_mode == "Hamming(7,4)" else []
            analysis["modified_indexes"] = channel_result.modified_indexes
            state.receiver_state = receiver_output.response.reason
            accepted = receiver_output.response.accepted
            state.status = ProtocolStatus.ACK if accepted else ProtocolStatus.NACK
            state.badges = ["SENT", "RECEIVED"]
            if receiver_output.corrected_indexes:
                state.badges.append("CORRECTED")
            state.badges.append(receiver_output.response.code)
            analysis["status_summary"] = receiver_output.response.reason
            if not accepted:
                self.logger.log(packet.packet_id, "nack", receiver_output.response.reason, attempt=attempt + 1)
            else:
                self.logger.log(packet.packet_id, "ack", receiver_output.response.reason, attempt=attempt + 1)

            attempt_results.append(
                TransmissionAttemptResult(
                    attempt_number=attempt + 1,
                    success=accepted,
                    ack=accepted,
                    detected_errors=packet.detected_errors,
                    corrected_errors=packet.corrected_errors,
                    noisy_indexes=channel_result.modified_indexes,
                    notes=receiver_output.response.reason,
                )
            )

            if accepted:
                packet.ack = True
                state.status = ProtocolStatus.ACK
                break
            if should_retry(accepted, attempt, config.max_retries):
                state.status = ProtocolStatus.RETRANSMITTED
                state.badges.append("RETRANSMITTED")
                self.logger.log(packet.packet_id, "retry", "Retransmission scheduled", next_attempt=attempt + 2)
                continue
            packet.dropped = True
            state.status = ProtocolStatus.DROPPED
            state.badges.append("DROPPED")
            self.logger.log(packet.packet_id, "drop", "Packet dropped after retry exhaustion", attempts=attempt + 1)

        success = packet.ack and not packet.dropped
        summary = "Transmission completed successfully" if success else "Transmission failed after retries"
        result = SimulationResult(packet=packet, success=success, protocol_summary=summary, attempts=attempt_results, logs=self.logger.serialize())
        return result, state, analysis
