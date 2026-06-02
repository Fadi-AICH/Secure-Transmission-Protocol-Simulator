"""Educational substitution cipher."""

from __future__ import annotations

import string


class SubstitutionCipher:
    """Monoalphabetic substitution cipher for comparison purposes."""

    _source = string.printable
    _target = _source[17:] + _source[:17]
    _enc = str.maketrans(_source, _target)
    _dec = str.maketrans(_target, _source)

    def encrypt(self, plaintext: str) -> str:
        return plaintext.translate(self._enc)

    def decrypt(self, payload: str) -> str:
        return payload.translate(self._dec)
