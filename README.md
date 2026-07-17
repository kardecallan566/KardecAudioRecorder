# 🎙️ Kardec Audio Recorder

O **Kardec Audio Recorder** é uma estação de trabalho de áudio digital (DAW) simplificada e poderosa, focada em capturar e processar voz com qualidade profissional. Desenvolvido em Python, o aplicativo oferece uma experiência intuitiva com processamento em tempo real e ferramentas de edição avançadas.

---

## ✨ Funcionalidades Principais

### 🎧 Monitoramento e Teste
- **Modo de Teste em Tempo Real:** Ouça sua voz processada pelos filtros antes mesmo de começar a gravar.
- **Visualização de Onda Dinâmica:** Gráfico de alta performance para monitorar a fidelidade do sinal.
- **Medidor de Volume (VU Meter):** Indicadores visuais para evitar distorções (clipping).

### 🎛️ Processamento Profissional
- **Redução de Ruído Inteligente:** Elimine ruídos de fundo e chiados constantes.
- **Compressor de Dinâmica:** Equilibre volumes baixos e altos para uma voz constante.
- **Equalizador de Prateleira:** Ajuste fino de Graves e Agudos.
- **Limitador e Normalização:** Garanta que seu áudio nunca distorça e tenha o volume ideal.

### ✂️ Editor de Áudio Avançado
- **Pitch Shift:** Altere o tom da voz (deixe mais fina ou mais grossa) sem perder a qualidade.
- **Pós-Processamento:** Aplique efeitos de EQ e Auto-tune em gravações já finalizadas.
- **Exportação Flexível:** Salve seus projetos em formato WAV ou exporte diretamente para **MP3**.

---

## 🎨 Identidade Visual
O aplicativo utiliza um tema **Modern Dark Green**, projetado para reduzir a fadiga ocular durante longas sessões de gravação, utilizando tons de:
- 🟢 **Verde Neon:** Para elementos ativos e indicadores.
- 🌿 **Verde Esmeralda:** Para botões de ação principal.
- 🌑 **Deep Dark Green:** Para o fundo e painéis de configuração.

---

## 🛠️ Tecnologias Utilizadas
- **Interface Gráfica:** [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- **Processamento Digital de Sinais (DSP):** [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [Librosa](https://librosa.org/)
- **Manipulação de Áudio:** [SoundDevice](https://python-sounddevice.readthedocs.io/), [PyDub](http://pydub.com/)
- **Visualização:** [PyQtGraph](https://www.pyqtgraph.org/)

---

## 🚀 Como Começar

### Pré-requisitos
Certifique-se de ter o Python 3.8+ instalado. Além disso, para exportação de MP3, é necessário o `ffmpeg` instalado no seu sistema.

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/kardecallan566/KardecAudioRecorder.git
   cd KardecAudioRecorder
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   python main.py
   ```

---

## 📂 Estrutura do Projeto
```text
KardecAudioRecorder/
├── main.py              # Ponto de entrada do aplicativo
├── requirements.txt     # Dependências do projeto
├── src/
│   ├── audio/           # Motores de captura e processamento
│   ├── ui/              # Janelas e componentes da interface
│   └── utils/           # Constantes e ferramentas de análise
└── README.md            # Documentação
```

---
Desenvolvido por **Manus AI** para **Kardec Allan**.
