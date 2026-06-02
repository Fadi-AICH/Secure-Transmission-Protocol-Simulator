from core.protocol.transmission_controller import TransmissionConfig, TransmissionController
from core.services.logger_service import LoggerService


def test_full_end_to_end_hamming_aes_transmission() -> None:
    controller = TransmissionController(LoggerService())
    result, _, analysis = controller.run(
        TransmissionConfig(
            plaintext="Integration payload",
            encryption_mode="AES",
            coding_mode="Hamming(7,4)",
            error_mode="Random Single-Bit",
            error_probability=1.0,
            random_seed=4,
            max_retries=2,
        )
    )
    assert result.success is True
    assert result.packet.decrypted_message == "Integration payload"
    assert analysis["syndrome"] != ""
