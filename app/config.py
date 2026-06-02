"""Application configuration and defaults."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json


APP_NAME = "Secure Transmission Protocol Simulator"
APP_ORG = "OpenAI Labs"
SETTINGS_FILE = Path("app_settings.json")


@dataclass(slots=True)
class AppSettings:
    """Persistent UI and simulator defaults."""

    theme: str = "dark"
    encryption_mode: str = "AES"
    coding_mode: str = "Hamming(7,4)"
    error_mode: str = "Random Single-Bit"
    error_probability: float = 0.05
    random_seed: int | None = 42
    max_retries: int = 3
    ack_timeout_ms: int = 500
    demo_message: str = "Launch window confirmed. Secure payload ready."

    @classmethod
    def load(cls, path: Path = SETTINGS_FILE) -> "AppSettings":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)

    def save(self, path: Path = SETTINGS_FILE) -> None:
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
