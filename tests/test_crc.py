from core.coding.crc_codec import CRCCodec


def test_crc_validates_clean_frame() -> None:
    codec = CRCCodec()
    frame = codec.encode("10101010")
    result = codec.validate(frame)
    assert result.valid is True
    assert result.data_bits == "10101010"


def test_crc_detects_corruption() -> None:
    codec = CRCCodec()
    frame = list(codec.encode("10101010"))
    frame[3] = "0" if frame[3] == "1" else "1"
    result = codec.validate("".join(frame))
    assert result.valid is False
