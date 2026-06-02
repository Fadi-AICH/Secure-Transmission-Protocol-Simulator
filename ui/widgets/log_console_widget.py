"""Table-backed log console."""

from __future__ import annotations

from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem, QWidget


class LogConsoleWidget(QTableWidget):
    """Display structured logs."""

    columns = ["Timestamp", "Packet", "Type", "Message"]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(0, len(self.columns), parent)
        self.setHorizontalHeaderLabels(self.columns)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setWordWrap(False)

    def set_logs(self, logs: list[dict], filter_text: str = "") -> None:
        self.setRowCount(0)
        filter_text = filter_text.lower().strip()
        for entry in logs:
            haystack = f"{entry['packet_id']} {entry['event_type']} {entry['message']}".lower()
            if filter_text and filter_text not in haystack:
                continue
            row = self.rowCount()
            self.insertRow(row)
            values = [entry["timestamp"], entry["packet_id"], entry["event_type"], entry["message"]]
            for column, value in enumerate(values):
                self.setItem(row, column, QTableWidgetItem(str(value)))
