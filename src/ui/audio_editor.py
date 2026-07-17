from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
import pyqtgraph as pg
import numpy as np
import soundfile as sf
from src.utils.constants import *

class AudioEditor(QWidget):
    def __init__(self, audio_path=None):
        super().__init__()
        self.audio_path = audio_path
        self.data = None
        self.samplerate = None
        self.setup_ui()
        if audio_path:
            self.load_audio(audio_path)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.label = QLabel("EDITOR DE ÁUDIO")
        layout.addWidget(self.label)

        # Visualização da Forma de Onda
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(COLOR_BACKGROUND)
        self.curve = self.plot_widget.plot(pen=pg.mkPen(COLOR_EMERALD, width=1))
        layout.addWidget(self.plot_widget)

        # Controles do Editor
        controls = QHBoxLayout()
        self.play_btn = QPushButton("Ouvir Gravado")
        self.play_btn.clicked.connect(self.play_audio)
        self.normalize_btn = QPushButton("Normalizar Volume")
        self.normalize_btn.clicked.connect(self.normalize_audio)
        self.export_btn = QPushButton("Exportar MP3")
        self.export_btn.clicked.connect(self.export_audio)
        self.close_btn = QPushButton("Fechar Editor")
        self.close_btn.setStyleSheet("background-color: #555;")
        
        controls.addWidget(self.play_btn)
        controls.addWidget(self.normalize_btn)
        controls.addWidget(self.export_btn)
        controls.addWidget(self.close_btn)
        layout.addLayout(controls)

    def play_audio(self):
        import sounddevice as sd
        if self.data is not None:
            sd.play(self.data, self.samplerate)

    def normalize_audio(self):
        if self.data is not None:
            max_val = np.max(np.abs(self.data))
            if max_val > 0:
                self.data = self.data / max_val * 0.9
                self.curve.setData(self.data[::max(1, len(self.data)//5000)])

    def export_audio(self):
        from pydub import AudioSegment
        import os
        if self.audio_path:
            # Converte WAV para MP3 usando pydub
            sound = AudioSegment.from_wav(self.audio_path)
            export_path = self.audio_path.replace(".wav", ".mp3")
            sound.export(export_path, format="mp3")
            self.label.setText(f"Exportado: {os.path.basename(export_path)}")

    def load_audio(self, path):
        self.audio_path = path
        self.data, self.samplerate = sf.read(path)
        if len(self.data.shape) > 1:
            self.data = self.data[:, 0] # Mono para visualização
        
        # Downsample para visualização rápida se o arquivo for longo
        step = max(1, len(self.data) // 5000)
        view_data = self.data[::step]
        self.curve.setData(view_data)
        self.label.setText(f"EDITOR: {path}")
