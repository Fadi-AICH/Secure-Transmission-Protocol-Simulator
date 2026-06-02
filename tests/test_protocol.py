from core.protocol.transmission_controller import TransmissionConfig, TransmissionController
from core.services.logger_service import LoggerService


def test_protocol_ack_flow_without_errors() -> None:
    controller = TransmissionController(LoggerService())
    result, state, _ = controller.run(
        TransmissionConfig(
            plaintext="protocol ok",
            encryption_mode="Substitution",
            coding_mode="CRC",
            error_mode="No Error",
            error_probability=0.0,
            random_seed=1,
            max_retries=2,
        )
    )
    assert result.success is True
    assert state.status.value == "ACK"
    assert result.packet.decrypted_message == "protocol ok"


def test_protocol_retransmits_and_drops_on_crc_failure() -> None:
    controller = TransmissionController(LoggerService())
    result, state, _ = controller.run(
        TransmissionConfig(
            plaintext="crc failure expected",
            encryption_mode="Substitution",
            coding_mode="CRC",
            error_mode="Burst Error",
            error_probability=1.0,
            random_seed=2,
            max_retries=1,
        )
    )
    assert result.success is False
    assert result.packet.dropped is True
    assert state.status.value == "DROPPED"


def test_protocol_reports_transport_corruption_cleanly() -> None:
    controller = TransmissionController(LoggerService())
    result, _, _ = controller.run(
        TransmissionConfig(
            plaintext="payload",
            encryption_mode="AES",
            coding_mode="CRC",
            error_mode="Random Multi-Bit",
            error_probability=1.0,
            random_seed=8,
            max_retries=0,
        )
    )
    assert result.success is False
    assert "transport" in result.packet.failure_reason.lower() or "crc" in result.packet.failure_reason.lower()
