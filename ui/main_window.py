"""Main application window."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog, QFileDialog, QMainWindow, QMessageBox, QTabWidget

from app.config import APP_NAME, AppSettings
from core.analytics.experiment_runner import ExperimentRunner
from core.analytics.metrics import MetricsCalculator
from core.protocol.transmission_controller import TransmissionConfig, TransmissionController
from core.services.export_service import ExportService
from core.services.logger_service import LoggerService
from core.services.session_service import SessionService
from ui.comparison_tab import ComparisonTab
from ui.dialogs.about_dialog import AboutDialog
from ui.dialogs.export_dialog import ExportDialog
from ui.frame_analysis_tab import FrameAnalysisTab
from ui.logs_tab import LogsTab
from ui.settings_tab import SettingsTab
from ui.simulation_tab import SimulationTab
from ui.statistics_tab import StatisticsTab


class MainWindow(QMainWindow):
    """Top-level desktop window."""

    def __init__(self, settings: AppSettings) -> None:
        super().__init__()
        self.settings = settings
        self.logger = LoggerService()
        self.controller = TransmissionController(self.logger)
        self.metrics = MetricsCalculator()
        self.exporter = ExportService()
        self.sessions = SessionService()
        self.experiments = ExperimentRunner()
        self.last_simulation = None
        self.last_experiment_results = []

        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1180, 760)
        self._build_menu()
        self._build_tabs()

    def _build_menu(self) -> None:
        help_menu = self.menuBar().addMenu("Help")
        about = QAction("About", self)
        about.triggered.connect(lambda: AboutDialog(self).exec())
        help_menu.addAction(about)

    def _build_tabs(self) -> None:
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        defaults = asdict(self.settings)
        self.simulation_tab = SimulationTab(defaults)
        self.analysis_tab = FrameAnalysisTab()
        self.logs_tab = LogsTab()
        self.statistics_tab = StatisticsTab()
        self.comparison_tab = ComparisonTab()
        self.settings_tab = SettingsTab(self.settings)
        tabs.addTab(self.simulation_tab, "Simulation")
        tabs.addTab(self.analysis_tab, "Frame Analysis")
        tabs.addTab(self.logs_tab, "Logs")
        tabs.addTab(self.statistics_tab, "Statistics")
        tabs.addTab(self.comparison_tab, "Comparison")
        tabs.addTab(self.settings_tab, "Settings")
        self.simulation_tab.simulate_requested.connect(self.run_simulation)
        self.simulation_tab.reset_requested.connect(self.reset_simulation)
        self.logs_tab.clear_requested.connect(self.clear_logs)
        self.logs_tab.export_requested.connect(self.export_data)
        self.comparison_tab.run_requested.connect(self.run_comparison)
        self.settings_tab.save_requested.connect(self.save_settings)

    def run_simulation(self, payload: dict) -> None:
        if not payload["plaintext"]:
            QMessageBox.warning(self, "Missing Message", "Please enter a plaintext message before sending.")
            return
        config = TransmissionConfig(**payload)
        result, state, analysis = self.controller.run(config)
        self.last_simulation = result
        self.metrics.add_simulation(result)
        self.simulation_tab.update_result(result.packet, state)
        noisy_indexes = result.attempts[-1].noisy_indexes if result.attempts else []
        corrected_indexes = next(
            (stage.highlighted_indexes for stage in result.packet.stages if stage.name == "Validated Frame"),
            [],
        )
        self.analysis_tab.update_analysis(result.packet, analysis, noisy_indexes, corrected_indexes)
        self.logs_tab.set_logs(result.logs)
        self.statistics_tab.update_statistics(self.metrics.snapshot(), self.metrics.simulations, self.last_experiment_results)

    def reset_simulation(self) -> None:
        self.last_simulation = None
        self.simulation_tab.reset()
        self.analysis_tab.update_analysis_dummy()

    def clear_logs(self) -> None:
        self.logger.clear()
        self.logs_tab.set_logs([])

    def run_comparison(self, payload: dict) -> None:
        self.last_experiment_results = self.experiments.run(**payload)
        self.metrics.set_experiments(self.last_experiment_results)
        self.comparison_tab.set_results(self.last_experiment_results)
        self.statistics_tab.update_statistics(self.metrics.snapshot(), self.metrics.simulations, self.last_experiment_results)

    def save_settings(self, settings: AppSettings) -> None:
        settings.demo_message = self.settings.demo_message
        settings.random_seed = self.settings.random_seed
        settings.save()
        self.settings = settings
        QMessageBox.information(self, "Settings Saved", "Default simulator settings were saved to app_settings.json.")

    def export_data(self) -> None:
        dialog = ExportDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        target, _ = QFileDialog.getSaveFileName(self, "Export Data", str(Path.cwd()))
        if not target:
            return
        export_type = dialog.export_type.currentText()
        logs = [] if self.last_simulation is None else self.last_simulation.logs
        if export_type == "Logs (.txt)":
            self.exporter.export_text_logs(logs, target)
        elif export_type == "Logs (.json)":
            self.exporter.export_json(logs, target)
        elif export_type == "Statistics (.csv)":
            self.exporter.export_csv(self.metrics.to_rows(), target)
        else:
            self.sessions.save_session(self.last_simulation, self.last_experiment_results, target)
        QMessageBox.information(self, "Export Complete", f"Data exported to {target}.")
