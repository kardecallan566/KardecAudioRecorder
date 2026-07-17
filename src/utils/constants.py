# Cores da Identidade Visual
COLOR_DARK_GREEN = "#0A2F1F"
COLOR_EMERALD = "#2ECC71"
COLOR_NEON_GREEN = "#39FF14"
COLOR_SOFT_GREEN = "#A8E6CF"
COLOR_BACKGROUND = "#051610"
COLOR_TEXT = "#E0F2F1"

# Configurações de Áudio Padrão
DEFAULT_SAMPLERATE = 44100
DEFAULT_CHANNELS = 1
DEFAULT_FORMAT = "wav"

# Perfis de Voz
VOICE_PROFILES = {
    "Podcast": {"noise_reduction": 0.8, "compressor": True, "bass_boost": True, "clarity": True},
    "Narração": {"noise_reduction": 0.9, "compressor": True, "bass_boost": False, "clarity": True},
    "Streaming": {"noise_reduction": 0.7, "compressor": True, "bass_boost": True, "clarity": False},
    "YouTube": {"noise_reduction": 0.6, "compressor": True, "bass_boost": False, "clarity": True},
    "Reunião Online": {"noise_reduction": 1.0, "compressor": False, "bass_boost": False, "clarity": True},
    "Rádio": {"noise_reduction": 0.5, "compressor": True, "bass_boost": True, "clarity": True},
    "Voz Limpa": {"noise_reduction": 0.4, "compressor": False, "bass_boost": False, "clarity": True},
}
