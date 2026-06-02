"""Qt stylesheet helpers."""

from __future__ import annotations


def build_stylesheet() -> str:
    """Return a polished dark engineering dashboard theme."""
    return """
    QWidget {
        background: #0b1118;
        color: #e8eef5;
        font-family: "Segoe UI", "Arial";
        font-size: 10pt;
    }
    QMainWindow, QMenuBar, QMenu, QStatusBar {
        background: #0b1118;
        color: #e8eef5;
    }
    QMenuBar {
        border-bottom: 1px solid #1c2a3c;
    }
    QMenuBar::item:selected, QMenu::item:selected {
        background: #172233;
    }
    QTabWidget::pane {
        border-top: 1px solid #1c2a3c;
        margin-top: -1px;
    }
    QTabBar::tab {
        background: #101924;
        border: 1px solid #26384f;
        border-bottom: none;
        padding: 12px 20px;
        min-width: 96px;
        margin-right: 6px;
        color: #c6d3e1;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    QTabBar::tab:selected {
        background: #162233;
        color: #7bb6ff;
    }
    QFrame[panel="true"], QFrame[chartCard="true"], QFrame[metricCard="true"], QFrame[node="true"], QFrame[hero="true"] {
        background: #0f1722;
        border: 1px solid #203044;
        border-radius: 14px;
    }
    QFrame[hero="true"] {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #111d2d, stop:1 #0d1520);
    }
    QLabel[title="true"] {
        font-size: 24pt;
        font-weight: 800;
        color: #f8fbff;
    }
    QLabel[subtitle="true"] {
        font-size: 10pt;
        color: #90a6bd;
    }
    QLabel[section="true"] {
        font-size: 11pt;
        font-weight: 700;
        color: #87b4ff;
    }
    QLabel[metricLabel="true"] {
        color: #90a6bd;
        font-size: 9pt;
        letter-spacing: 0.5px;
    }
    QLabel[metricValue="true"] {
        color: #f7fbff;
        font-size: 21pt;
        font-weight: 800;
    }
    QLabel[badge="sent"] { background: #173756; color: #8bc6ff; border: 1px solid #2b6ca3; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QLabel[badge="received"] { background: #123a3d; color: #68e0d0; border: 1px solid #22867e; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QLabel[badge="corrected"] { background: #4a3910; color: #ffd773; border: 1px solid #c79a2b; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QLabel[badge="ack"] { background: #15391f; color: #7eed9f; border: 1px solid #2c9f53; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QLabel[badge="nack"] { background: #45131b; color: #ff7c8a; border: 1px solid #d1485f; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QLabel[badge="retransmitted"] { background: #4c2712; color: #ffb469; border: 1px solid #d87b36; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QLabel[badge="dropped"] { background: #2f3640; color: #c7d0da; border: 1px solid #697380; border-radius: 15px; padding: 6px 12px; font-weight: 700; }
    QGroupBox {
        border: 1px solid #223246;
        border-radius: 14px;
        margin-top: 14px;
        padding-top: 16px;
        font-weight: 700;
        color: #d6e2ee;
        background: #0e151f;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 8px;
    }
    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget {
        background: #16212f;
        border: 1px solid #2a3c53;
        border-radius: 10px;
        padding: 8px;
        selection-background-color: #245998;
        selection-color: #f7fbff;
    }
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTableWidget:focus {
        border: 1px solid #4d8dd9;
    }
    QTextEdit[mono="true"], QPlainTextEdit[mono="true"] {
        font-family: "Cascadia Code", "Consolas";
        font-size: 9pt;
    }
    QPushButton {
        background: #2d72e0;
        border: 1px solid #3b83f0;
        border-radius: 10px;
        padding: 10px 16px;
        color: white;
        font-weight: 700;
    }
    QPushButton:hover { background: #367cef; }
    QPushButton:pressed { background: #255fbe; }
    QPushButton[secondary="true"] {
        background: #1b2532;
        border: 1px solid #33465d;
        color: #d1deeb;
    }
    QPushButton[secondary="true"]:hover { background: #243143; }
    QHeaderView::section {
        background: #192433;
        color: #e3edf8;
        padding: 8px;
        border: none;
        border-right: 1px solid #2b3d55;
        font-weight: 700;
    }
    QTableWidget {
        gridline-color: #223349;
        alternate-background-color: #121b27;
    }
    QTableCornerButton::section {
        background: #192433;
        border: none;
    }
    QScrollBar:vertical {
        background: transparent;
        width: 12px;
    }
    QScrollBar::handle:vertical {
        background: #34475e;
        min-height: 24px;
        border-radius: 6px;
    }
    QScrollBar:horizontal {
        background: transparent;
        height: 12px;
    }
    QScrollBar::handle:horizontal {
        background: #34475e;
        min-width: 24px;
        border-radius: 6px;
    }
    """
