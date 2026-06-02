"""AES encryption wrapper."""

from __future__ import annotations

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from core.crypto.crypto_utils import from_b64, to_b64


class AESCipher:
    """Symmetric AES-CBC helper."""

    def __init__(self, key: bytes | None = None) -> None:
        self.key = key or b"SecureProtoKey16"
        if len(self.key) not in (16, 24, 32):
            raise ValueError("AES key must be 16, 24, or 32 bytes long.")

    def encrypt(self, plaintext: str) -> str:
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
        return to_b64(iv + ciphertext)

    def decrypt(self, payload: str) -> str:
        raw = from_b64(payload)
        iv, ciphertext = raw[:16], raw[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode("utf-8")
