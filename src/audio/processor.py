import numpy as np
from scipy import signal

class AudioProcessor:
    def __init__(self):
        self.enabled_filters = {
            "noise_reduction": False,
            "compressor": False,
            "equalizer": False,
            "bass_boost": False,
            "clarity": False,
            "limiter": False,
            "normalization": False
        }
        self.params = {
            "noise_reduction_level": 0.5,
            "gain": 1.0,
            "bass": 1.0,
            "mid": 1.0,
            "treble": 1.0
        }

    def process(self, data):
        """Processa o bloco de áudio (numpy array)"""
        if data.size == 0:
            return data
            
        processed_data = data.copy()

        # 1. Ganho/Amplificação
        processed_data *= self.params["gain"]

        # 2. Equalizador Simples (Filtros de prateleira/pico)
        if self.enabled_filters["equalizer"] or self.enabled_filters["bass_boost"] or self.enabled_filters["clarity"]:
            processed_data = self._apply_equalizer(processed_data)

        # 3. Compressor de Dinâmica (Simples)
        if self.enabled_filters["compressor"]:
            processed_data = self._apply_compressor(processed_data)

        # 4. Limitador (Hard Clipping Preventer)
        if self.enabled_filters["limiter"]:
            processed_data = np.clip(processed_data, -0.98, 0.98)

        return processed_data

    def _apply_equalizer(self, data):
        # Implementação de filtros de prateleira para graves e agudos
        fs = 44100
        processed = data.copy()
        
        if self.enabled_filters["bass_boost"]:
            # Filtro passa-baixa simples para reforço de graves
            b, a = signal.butter(2, 200, 'low', fs=fs)
            bass = signal.lfilter(b, a, processed, axis=0)
            processed += bass * 0.5
            
        if self.enabled_filters["clarity"]:
            # Filtro passa-alta para clareza (presença)
            b, a = signal.butter(2, 3000, 'high', fs=fs)
            treble = signal.lfilter(b, a, processed, axis=0)
            processed += treble * 0.3
            
        return processed

    def _apply_compressor(self, data, threshold=0.3, ratio=4.0):
        # Compressor básico: se acima do threshold, reduz o volume
        mask = np.abs(data) > threshold
        data[mask] = np.sign(data[mask]) * (threshold + (np.abs(data[mask]) - threshold) / ratio)
        return data

    def toggle_filter(self, filter_name, state):
        if filter_name in self.enabled_filters:
            self.enabled_filters[filter_name] = state

    def update_param(self, param_name, value):
        if param_name in self.params:
            self.params[param_name] = value
