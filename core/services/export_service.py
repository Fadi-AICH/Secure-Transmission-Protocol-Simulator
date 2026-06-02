"""Export logs and statistics."""

from __future__ import annotations

import csv
import json
from pathlib import Path


class ExportService:
    """Export structured simulator data."""

    def export_json(self, data: object, path: str | Path) -> None:
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def export_text_logs(self, logs: list[dict], path: str | Path) -> None:
        lines = [
            f"[{entry['timestamp']}] [{entry['packet_id']}] {entry['event_type']}: {entry['message']}"
            for entry in logs
        ]
        Path(path).write_text("\n".join(lines), encoding="utf-8")

    def export_csv(self, rows: list[dict], path: str | Path) -> None:
        if not rows:
            Path(path).write_text("", encoding="utf-8")
            return
        with Path(path).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
