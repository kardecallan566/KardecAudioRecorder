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
        self.cut_btn = QPushButton("Cortar Seleção")
        self.silence_btn = QPushButton("Remover Silêncio")
        self.normalize_btn = QPushButton("Normalizar")
        self.export_btn = QPushButton("Exportar")
        
        controls.addWidget(self.cut_btn)
        controls.addWidget(self.silence_btn)
        controls.addWidget(self.normalize_btn)
        controls.addWidget(self.export_btn)
        layout.addLayout(controls)

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
