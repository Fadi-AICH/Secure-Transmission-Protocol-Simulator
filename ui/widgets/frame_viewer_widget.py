"""Rich frame viewer with bit highlighting."""

from __future__ import annotations

from html import escape

from PySide6.QtWidgets import QTextEdit, QWidget


class FrameViewerWidget(QTextEdit):
    """Shows binary frames with grouped highlighting and offsets."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setReadOnly(True)
        self.setProperty("mono", True)

    def set_frame(
        self,
        bits: str,
        parity_indexes: list[int] | None = None,
        corrupted_indexes: list[int] | None = None,
        corrected_indexes: list[int] | None = None,
    ) -> None:
        parity_indexes = parity_indexes or []
        corrupted_indexes = corrupted_indexes or []
        corrected_indexes = corrected_indexes or []
        highlight_map: dict[int, str] = {}
        for index in parity_indexes:
            highlight_map[index] = "#6ca8ff"
        for index in corrupted_indexes:
            highlight_map[index] = "#ff5573"
        for index in corrected_indexes:
            highlight_map[index] = "#ffd166"

        groups: list[str] = []
        group_size = 8
        groups_per_line = 6
        for start in range(0, len(bits), group_size):
            group = bits[start:start + group_size]
            rendered = []
            for offset, bit in enumerate(group):
                bit_index = start + offset
                color = highlight_map.get(bit_index, "#edf3fa")
                rendered.append(f'<span style="color:{color}; font-weight:700;">{escape(bit)}</span>')
            groups.append("".join(rendered))

        if not groups:
            self.setPlainText("")
            return

        lines: list[str] = []
        for line_index in range(0, len(groups), groups_per_line):
            offset = line_index * group_size
            chunk = groups[line_index:line_index + groups_per_line]
            lines.append(f'<span style="color:#7b92aa;">{offset:04d}</span>  ' + " ".join(chunk))

        legend = (
            '<div style="margin-bottom:8px; color:#93a8bd;">'
            '<span style="color:#6ca8ff;">Parity</span>  |  '
            '<span style="color:#ff5573;">Corrupted</span>  |  '
            '<span style="color:#ffd166;">Corrected</span>'
            "</div>"
        )
        self.setHtml(
            '<div style="font-family:Cascadia Code, Consolas; font-size:10pt; line-height:1.6;">'
            + legend
            + "<br>".join(lines)
            + "</div>"
        )
