from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QLabel, QComboBox, QSlider, QFrame, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette
import pyqtgraph as pg
from src.utils.constants import *
from src.audio.engine import AudioEngine
from src.ui.audio_editor import AudioEditor
import os
from datetime import datetime
import sounddevice as sd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kardec Audio Recorder")
        self.setMinimumSize(1200, 800)
        self.audio_engine = AudioEngine()
        
        self.setup_ui()
        self.apply_styles()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_visuals)
        self.timer.start(30)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Left Panel
        left_panel = QVBoxLayout()
        left_frame = QFrame()
        left_frame.setLayout(left_panel)
        left_frame.setFixedWidth(250)
        
        left_panel.addWidget(QLabel("CONFIGURAÇÕES"))
        self.device_combo = QComboBox()
        self.update_devices()
        left_panel.addWidget(QLabel("Microfone:"))
        left_panel.addWidget(self.device_combo)
        
        left_panel.addWidget(QLabel("Perfil de Voz:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(VOICE_PROFILES.keys())
        self.profile_combo.currentTextChanged.connect(self.on_profile_changed)
        left_panel.addWidget(self.profile_combo)

        left_panel.addWidget(QLabel("Volume de Entrada:"))
        self.gain_slider = QSlider(Qt.Orientation.Horizontal)
        self.gain_slider.setRange(0, 200)
        self.gain_slider.setValue(100)
        self.gain_slider.valueChanged.connect(self.on_gain_changed)
        left_panel.addWidget(self.gain_slider)
        
        left_panel.addStretch()
        
        # Center Panel
        center_panel = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(COLOR_BACKGROUND)
        self.curve = self.plot_widget.plot(pen=pg.mkPen(COLOR_NEON_GREEN, width=2))
        self.plot_widget.setYRange(-1, 1)
        center_panel.addWidget(self.plot_widget)
        
        self.volume_bar = QProgressBar()
        self.volume_bar.setRange(0, 100)
        self.volume_bar.setTextVisible(False)
        center_panel.addWidget(self.volume_bar)
        
        controls = QHBoxLayout()
        self.record_btn = QPushButton("Iniciar Gravação")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.test_btn = QPushButton("Modo de Teste")
        self.test_btn.clicked.connect(self.toggle_monitoring)
        controls.addWidget(self.test_btn)
        controls.addWidget(self.record_btn)
        center_panel.addLayout(controls)

        # Right Panel
        right_panel = QVBoxLayout()
        right_frame = QFrame()
        right_frame.setLayout(right_panel)
        right_frame.setFixedWidth(300)
        
        right_panel.addWidget(QLabel("PROCESSAMENTO"))
        self.filters = {}
        filter_list = ["Redução de Ruído", "Compressor", "Equalizador", "Limitador", "Normalização"]
        for f in filter_list:
            btn = QPushButton(f)
            btn.setCheckable(True)
            btn.toggled.connect(lambda state, name=f: self.on_filter_toggled(name, state))
            right_panel.addWidget(btn)
            self.filters[f] = btn
        right_panel.addStretch()

        layout.addWidget(left_frame)
        layout.addLayout(center_panel)
        layout.addWidget(right_frame)

        # Integrated Editor
        self.editor_widget = AudioEditor()
        self.editor_widget.hide()
        self.editor_widget.close_btn.clicked.connect(self.close_editor)
        center_panel.addWidget(self.editor_widget)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background-color: {COLOR_BACKGROUND}; color: {COLOR_TEXT}; font-family: 'Segoe UI', sans-serif; }}
            QFrame {{ background-color: {COLOR_DARK_GREEN}; border-radius: 10px; padding: 10px; }}
            QPushButton {{ background-color: {COLOR_EMERALD}; color: {COLOR_BACKGROUND}; border: none; padding: 10px; border-radius: 5px; font-weight: bold; }}
            QPushButton:checked {{ background-color: {COLOR_NEON_GREEN}; }}
            QPushButton:hover {{ background-color: {COLOR_SOFT_GREEN}; }}
            QLabel {{ font-size: 14px; font-weight: bold; margin-top: 10px; }}
            QProgressBar::chunk {{ background-color: {COLOR_NEON_GREEN}; }}
        """)

    def update_devices(self):
        devices = self.audio_engine.get_input_devices()
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                self.device_combo.addItem(dev['name'], i)

    def toggle_monitoring(self):
        if not self.audio_engine.is_monitoring:
            try:
                idx = self.device_combo.currentData()
                self.audio_engine.start_monitoring(device_index=idx)
                self.test_btn.setText("Parar Teste")
                self.test_btn.setStyleSheet(f"background-color: {COLOR_NEON_GREEN}; color: black;")
            except Exception as e:
                QMessageBox.critical(self, "Erro de Áudio", f"Erro ao iniciar monitoramento:\n{str(e)}")
                self.audio_engine.stop_monitoring()
        else:
            self.audio_engine.stop_monitoring()
            self.test_btn.setText("Modo de Teste")
            self.test_btn.setStyleSheet(f"background-color: {COLOR_EMERALD}; color: {COLOR_BACKGROUND};")

    def toggle_recording(self):
        if not self.audio_engine.is_recording:
            if not self.audio_engine.is_monitoring:
                self.toggle_monitoring()
            self.audio_engine.start_recording()
            self.record_btn.setText("Finalizar Gravação")
            self.record_btn.setStyleSheet("background-color: #FF4444; color: white;")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Gravacao_{timestamp}.wav"
            filepath = self.audio_engine.stop_recording(filename)
            self.record_btn.setText("Iniciar Gravação")
            self.record_btn.setStyleSheet(f"background-color: {COLOR_EMERALD}; color: {COLOR_BACKGROUND};")
            
            if filepath and os.path.exists(filepath):
                if self.audio_engine.is_monitoring:
                    self.toggle_monitoring()
                self.editor_widget.load_audio(filepath)
                self.editor_widget.show()
                self.plot_widget.hide()
                self.test_btn.setEnabled(False)
                self.record_btn.setEnabled(False)

    def close_editor(self):
        self.editor_widget.hide()
        self.plot_widget.show()
        self.test_btn.setEnabled(True)
        self.record_btn.setEnabled(True)
        sd.stop()

    def on_gain_changed(self, value):
        self.audio_engine.processor.update_param("gain", value / 100.0)

    def on_profile_changed(self, profile_name):
        profile = VOICE_PROFILES.get(profile_name)
        if profile:
            for f, state in [("noise_reduction", profile["noise_reduction"] > 0), ("compressor", profile["compressor"])]:
                self.audio_engine.processor.toggle_filter(f, state)
            self.filters["Redução de Ruído"].setChecked(profile["noise_reduction"] > 0)
            self.filters["Compressor"].setChecked(profile["compressor"])

    def on_filter_toggled(self, name, state):
        mapping = {"Redução de Ruído": "noise_reduction", "Compressor": "compressor", "Equalizador": "equalizer", "Limitador": "limiter", "Normalização": "normalization"}
        self.audio_engine.processor.toggle_filter(mapping[name], state)

    def update_visuals(self):
        if self.audio_engine.is_monitoring:
            data = self.audio_engine.get_latest_data()
            if len(data) > 0:
                if len(data.shape) > 1 and data.shape[1] == 1: data = data.flatten()
                self.curve.setData(data[-1000:])
            vol = int(self.audio_engine.current_volume * 500)
            self.volume_bar.setValue(min(vol, 100))
