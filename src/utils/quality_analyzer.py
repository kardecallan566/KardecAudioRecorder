import numpy as np
import librosa

class QualityAnalyzer:
    @staticmethod
    def analyze(audio_path):
        y, sr = librosa.load(audio_path)
        
        # 1. Nível Médio de Ruído (Estimado pelo silêncio)
        rms = librosa.feature.rms(y=y)
        avg_volume = np.mean(rms)
        
        # 2. Clipping
        clipping_count = np.sum(np.abs(y) >= 0.98)
        
        # 3. Sugestões
        suggestions = []
        if avg_volume < 0.05:
            suggestions.append("Aumente o ganho do microfone.")
        if clipping_count > 100:
            suggestions.append("Reduza o volume de entrada para evitar distorção.")
            
        return {
            "avg_volume": avg_volume,
            "clipping_detected": clipping_count > 0,
            "suggestions": suggestions
        }
