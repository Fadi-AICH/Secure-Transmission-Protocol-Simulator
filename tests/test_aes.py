from core.crypto.aes_cipher import AESCipher
from core.crypto.substitution_cipher import SubstitutionCipher


def test_aes_encrypt_decrypt_round_trip() -> None:
    cipher = AESCipher()
    payload = cipher.encrypt("secure message")
    assert cipher.decrypt(payload) == "secure message"


def test_substitution_round_trip() -> None:
    cipher = SubstitutionCipher()
    payload = cipher.encrypt("hello protocol")
    assert cipher.decrypt(payload) == "hello protocol"
