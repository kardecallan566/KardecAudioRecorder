import sounddevice as sd
import numpy as np
import threading
import queue
import soundfile as sf
from src.audio.processor import AudioProcessor

class AudioEngine:
    def __init__(self, samplerate=44100, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.processor = AudioProcessor()
        self.input_queue = queue.Queue()
        self.is_recording = False
        self.is_monitoring = False
        self.stream = None
        self.recorded_data = []
        self.current_volume = 0
        
    def get_input_devices(self):
        return sd.query_devices()

    def start_monitoring(self, device_index=None):
        self.is_monitoring = True
        # Usamos Stream (In/Out) para permitir ouvir o áudio processado
        self.stream = sd.Stream(
            device=device_index,
            channels=self.channels,
            samplerate=self.samplerate,
            callback=self._audio_callback
        )
        self.stream.start()

    def stop_monitoring(self):
        self.is_monitoring = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def start_recording(self):
        self.recorded_data = []
        self.is_recording = True

    def stop_recording(self, filename):
        self.is_recording = False
        if self.recorded_data:
            # Concatenar todos os blocos gravados
            full_data = np.vstack(self.recorded_data)
            sf.write(filename, full_data, self.samplerate)
            self.recorded_data = [] # Limpa para a próxima
            return filename
        return None

    def _audio_callback(self, indata, outdata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        
        # Processamento em tempo real
        processed = self.processor.process(indata)
        
        # Copia para a saída (monitoramento audível)
        outdata[:] = processed
        
        # Calcula volume para o medidor
        self.current_volume = np.linalg.norm(processed) / np.sqrt(len(processed))
        
        # Envia para a fila de visualização
        self.input_queue.put(processed.copy())
        
        # Se estiver gravando, armazena
        if self.is_recording:
            self.recorded_data.append(processed.copy())

    def get_latest_data(self):
        data = []
        while not self.input_queue.empty():
            data.append(self.input_queue.get())
        return np.concatenate(data) if data else np.array([])
