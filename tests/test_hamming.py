from core.coding.hamming74 import Hamming74Codec


def test_hamming_encode_decode_round_trip() -> None:
    codec = Hamming74Codec()
    encoded, padding = codec.encode("10110011")
    decoded = codec.decode(encoded, padding)
    assert decoded.data_bits == "10110011"
    assert decoded.detected is False


def test_hamming_single_bit_correction() -> None:
    codec = Hamming74Codec()
    encoded, padding = codec.encode("1011")
    corrupted = list(encoded)
    corrupted[2] = "0" if corrupted[2] == "1" else "1"
    result = codec.decode("".join(corrupted), padding)
    assert result.data_bits == "1011"
    assert result.detected is True
    assert result.corrected is True
