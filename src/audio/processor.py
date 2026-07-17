import numpy as np
from scipy import signal

import librosa
import pyrubberband as pyrb

class AudioProcessor:
    def __init__(self):
        self.enabled_filters = {
            "noise_reduction": False,
            "compressor": False,
            "equalizer": False,
            "bass_boost": False,
            "clarity": False,
            "limiter": False,
            "normalization": False,
            "autotune": False
        }
        self.params = {
            "noise_reduction_level": 0.5,
            "gain": 1.0,
            "bass": 1.0,
            "mid": 1.0,
            "treble": 1.0,
            "pitch_shift": 0.0, # em semitons
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

    def _apply_equalizer(self, data, fs=44100):
        processed = data.copy()
        
        # Bass (Graves)
        if self.params["bass"] != 1.0:
            b, a = signal.butter(2, 250, 'low', fs=fs)
            bass_part = signal.lfilter(b, a, processed, axis=0)
            processed = processed + bass_part * (self.params["bass"] - 1.0)

        # Treble (Agudos)
        if self.params["treble"] != 1.0:
            b, a = signal.butter(2, 4000, 'high', fs=fs)
            treble_part = signal.lfilter(b, a, processed, axis=0)
            processed = processed + treble_part * (self.params["treble"] - 1.0)
            
        return processed

    def apply_pitch_shift(self, data, sr, n_steps):
        if n_steps == 0:
            return data
        return librosa.effects.pitch_shift(y=data, sr=sr, n_steps=n_steps)

    def apply_autotune(self, data, sr):
        # Implementação simplificada de correção de tom (Auto-tune)
        # Em um cenário real, isso requer detecção de pitch e correção para a nota mais próxima
        # Aqui usaremos um efeito de "vibrato" ou correção leve se habilitado
        return data # Placeholder para lógica complexa de autotune

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
