# Traductor de Voz a Voz 🎙️⇉️🗣️

Este proyecto convierte un archivo de voz en texto usando **Whisper** y **Pyannote**, traduce el texto a otro idioma y genera un nuevo archivo de audio.

### 🔥 Tecnologías utilizadas
- [Whisper](https://github.com/openai/whisper) - Transcripción automática
- [Pyannote.audio](https://github.com/pyannote/pyannote-audio) - Diarización de hablantes
- [OpenAI API](https://platform.openai.com/) - Traducción
- [Python](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/) - Procesamiento de audio

---

## 🚀 Instalación

1. **Clonar el repositorio**

```
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

2. **Crear entorno virtual**

```
python -m venv venv
```

3. **Activar entorno virtual**

- En Windows:

```
venv\Scripts\activate
```

- En Linux / Mac:

```
source venv/bin/activate
```

4. **Instalar dependencias**

```
pip install -r requirements.txt
```

5. **Configurar variables de entorno**

Crear un archivo `.env` en la raíz del proyecto y agregar tus credenciales:

```
OPENAI_API_KEY=tu_clave_de_openai
HUGGINGFACE_TOKEN=tu_clave_de_huggingface
```

> ⚠️ **Importante**: No compartas tu `.env` ni tus tokens.

6. **Instalar FFmpeg**

El proyecto requiere los binarios de **FFmpeg** para funcionar.

- Descargar FFmpeg desde [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Extraer el contenido.
- Asegurarse que el ejecutable esté disponible en el path `ffmpeg/bin` dentro del proyecto o que esté agregado al **PATH del sistema**.

---

## 🧐 Uso

Ejecutar el proyecto pasando la ruta del audio de entrada:

```
python main.py --audio_path "ruta/del/audio.wav"
```

Por ejemplo:

```
python main.py --audio_path "audio_input/input2.wav"
```

Esto realiza de manera automática:

1. **Diarización** (separación de hablantes).
2. **Transcripción** (genera `output_transcript.txt`).
3. **Traducción** y **generación de nuevas voces**.

---

## 📂 Estructura del Proyecto

```
voice-translator/
├── .env
├── audio_input/
│   └── input2.wav
├── output_transcript.txt
├── diarization_transcription.py
├── generate_voice.py
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚡ Notas adicionales
- **GPU recomendada** para mayor velocidad (Whisper y Pyannote son intensivos).
- FFmpeg debe estar instalado correctamente o el proyecto no podrá procesar los audios.
- Actualmente el proyecto traduce y genera voces sobre un único archivo de entrada por ejecución.

---

## 🛠️ Futuras mejoras
- Selección de idioma de traducción.
- Procesamiento por lotes de audios.
- Generación de reportes de transcripción y traducción.

