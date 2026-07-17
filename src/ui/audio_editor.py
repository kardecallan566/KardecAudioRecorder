from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QHBoxLayout, 
                             QLabel, QSlider, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import soundfile as sf
from src.utils.constants import *
from src.audio.processor import AudioProcessor

class AudioEditor(QWidget):
    def __init__(self, audio_path=None):
        super().__init__()
        self.audio_path = audio_path
        self.data = None
        self.original_data = None
        self.samplerate = None
        self.processor = AudioProcessor()
        self.setup_ui()
        if audio_path:
            self.load_audio(audio_path)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        self.label = QLabel("EDITOR DE ÁUDIO AVANÇADO")
        self.label.setStyleSheet("font-size: 18px; color: #39FF14;")
        header.addWidget(self.label)
        layout.addLayout(header)

        # Waveform View
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(COLOR_BACKGROUND)
        self.curve = self.plot_widget.plot(pen=pg.mkPen(COLOR_EMERALD, width=1))
        self.plot_widget.setFixedHeight(200)
        layout.addWidget(self.plot_widget)

        # Effects Panel
        effects_frame = QFrame()
        effects_frame.setStyleSheet(f"background-color: {COLOR_DARK_GREEN}; border-radius: 10px;")
        effects_layout = QGridLayout(effects_frame)

        # Pitch Control (Voz Fina/Grossa)
        effects_layout.addWidget(QLabel("Pitch (Fina/Grossa):"), 0, 0)
        self.pitch_slider = QSlider(Qt.Orientation.Horizontal)
        self.pitch_slider.setRange(-12, 12) # -1 oitava a +1 oitava
        self.pitch_slider.setValue(0)
        effects_layout.addWidget(self.pitch_slider, 0, 1)

        # Bass Control
        effects_layout.addWidget(QLabel("Grave:"), 1, 0)
        self.bass_slider = QSlider(Qt.Orientation.Horizontal)
        self.bass_slider.setRange(0, 200)
        self.bass_slider.setValue(100)
        effects_layout.addWidget(self.bass_slider, 1, 1)

        # Treble Control
        effects_layout.addWidget(QLabel("Agudo:"), 2, 0)
        self.treble_slider = QSlider(Qt.Orientation.Horizontal)
        self.treble_slider.setRange(0, 200)
        self.treble_slider.setValue(100)
        effects_layout.addWidget(self.treble_slider, 2, 1)

        # Auto-tune Button
        self.autotune_btn = QPushButton("Auto-tune (On/Off)")
        self.autotune_btn.setCheckable(True)
        effects_layout.addWidget(self.autotune_btn, 3, 0, 1, 2)

        # Apply Effects Button
        self.apply_btn = QPushButton("Processar Efeitos")
        self.apply_btn.setStyleSheet("background-color: #39FF14; color: black;")
        self.apply_btn.clicked.connect(self.apply_effects)
        effects_layout.addWidget(self.apply_btn, 4, 0, 1, 2)

        layout.addWidget(effects_frame)

        # Footer Controls
        controls = QHBoxLayout()
        self.play_btn = QPushButton("Ouvir")
        self.play_btn.clicked.connect(self.play_audio)
        self.reset_btn = QPushButton("Resetar")
        self.reset_btn.clicked.connect(self.reset_audio)
        self.export_btn = QPushButton("Exportar MP3")
        self.export_btn.clicked.connect(self.export_audio)
        self.close_btn = QPushButton("Fechar")
        self.close_btn.setStyleSheet("background-color: #555;")
        
        controls.addWidget(self.play_btn)
        controls.addWidget(self.reset_btn)
        controls.addWidget(self.export_btn)
        controls.addWidget(self.close_btn)
        layout.addLayout(controls)

    def load_audio(self, path):
        self.audio_path = path
        self.data, self.samplerate = sf.read(path)
        if len(self.data.shape) > 1:
            self.data = self.data[:, 0]
        self.original_data = self.data.copy()
        self.update_waveform()

    def update_waveform(self):
        step = max(1, len(self.data) // 5000)
        self.curve.setData(self.data[::step])

    def reset_audio(self):
        self.data = self.original_data.copy()
        self.update_waveform()
        self.pitch_slider.setValue(0)
        self.bass_slider.setValue(100)
        self.treble_slider.setValue(100)

    def apply_effects(self):
        self.apply_btn.setText("Processando...")
        self.apply_btn.setEnabled(False)
        
        # Inicia com o original para não acumular
        processed = self.original_data.copy()
        
        # 1. Pitch Shift
        pitch_steps = self.pitch_slider.value()
        if pitch_steps != 0:
            processed = self.processor.apply_pitch_shift(processed, self.samplerate, pitch_steps)
            
        # 2. EQ (Bass/Treble)
        self.processor.params["bass"] = self.bass_slider.value() / 100.0
        self.processor.params["treble"] = self.treble_slider.value() / 100.0
        processed = self.processor._apply_equalizer(processed, self.samplerate)
        
        self.data = processed
        self.update_waveform()
        self.apply_btn.setText("Processar Efeitos")
        self.apply_btn.setEnabled(True)

    def play_audio(self):
        import sounddevice as sd
        if self.data is not None:
            sd.play(self.data, self.samplerate)

    def export_audio(self):
        from pydub import AudioSegment
        import os
        if self.data is not None:
            # Salva temporário para converter
            temp_wav = "temp_export.wav"
            sf.write(temp_wav, self.data, self.samplerate)
            sound = AudioSegment.from_wav(temp_wav)
            export_path = self.audio_path.replace(".wav", "_editado.mp3")
            sound.export(export_path, format="mp3")
            os.remove(temp_wav)
            self.label.setText(f"Exportado: {os.path.basename(export_path)}")
