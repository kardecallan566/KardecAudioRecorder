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
        
        if device_index is None:
            device_index = sd.default.device[0]
            
        device_info = sd.query_devices(device_index)
        
        # Usar samplerate do dispositivo se o padrão falhar
        samplerate = int(device_info.get('default_samplerate', self.samplerate))
        
        # Lógica de canais ultra-compatível
        max_in = device_info['max_input_channels']
        max_out = device_info['max_output_channels']
        
        # Se max_out for 0 (dispositivo só de entrada), usamos sd.InputStream
        if max_out == 0:
            self.stream = sd.InputStream(
                device=device_index,
                channels=min(self.channels, max_in),
                samplerate=samplerate,
                callback=self._input_only_callback
            )
        else:
            # Stream Duplex (In/Out)
            in_channels = min(self.channels, max_in)
            # Alguns drivers bugam se pedir mais canais do que o max_out
            out_channels = min(in_channels, max_out) if max_out < 2 else min(2, max_out)
            
            self.stream = sd.Stream(
                device=device_index,
                channels=(in_channels, out_channels),
                samplerate=samplerate,
                callback=self._audio_callback
            )
        
        self.stream.start()

    def _input_only_callback(self, indata, frames, time, status):
        """Fallback para quando não há saída disponível no dispositivo selecionado"""
        self._audio_callback(indata, None, frames, time, status)

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
        
        # Se tivermos outdata (Stream Duplex), copiamos o áudio processado
        if outdata is not None:
            if outdata.shape[1] > processed.shape[1]:
                outdata[:] = np.repeat(processed, outdata.shape[1], axis=1)
            else:
                outdata[:] = processed[:, :outdata.shape[1]]
        
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
