def run_diarization_transcription(audio_path):
    import whisper
    from pyannote.audio import Pipeline
    from collections import defaultdict
    import datetime
    import os
    import sys
    
    # todo tu código actual que genera output_transcript.txt
    print("✅ Diarization + Transcripción completa.")

    # Detectar si estamos en Colab (opcional, por prolijidad)
    in_colab = "COLAB_GPU" in os.environ

    # Cargar el Token de HuggingFace
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    
    if not HUGGINGFACE_TOKEN:
        raise ValueError("❌ No se encontró el HUGGINGFACE_TOKEN en las variables de entorno.")

    # Agregar FFmpeg al PATH
    ffmpeg_path = os.path.abspath("ffmpeg/bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path

    # === CONFIGURACIÓN ===
    AUDIO_PATH = audio_path # r"C:\Users\ignac\voice-translate\audio_input\input2.wav"
    MODEL_SIZE = "small"  # podés cambiarlo por "small", "medium", etc.

    # === FUNCIONES ===
    def format_time(seconds):
        return str(datetime.timedelta(seconds=int(seconds)))

    # === TRANSCRIPCIÓN ===
    print("📝 Transcribiendo con Whisper...")
    model = whisper.load_model(MODEL_SIZE)
    result = model.transcribe(AUDIO_PATH)

    # === DIARIZACIÓN ===
    print("🎙️ Aplicando diarización con pyannote...")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=HUGGINGFACE_TOKEN)
    diarization = pipeline(AUDIO_PATH)

    # === COMBINAR SPEAKERS CON TEXTO ===
    print("🧠 Combinando texto con locutores...\n")
    lines = []

    for segment in result['segments']:
        start, end, text = segment['start'], segment['end'], segment['text']
        
        speaker_durations = defaultdict(float)

        for turn, _, speaker_label in diarization.itertracks(yield_label=True):
            overlap_start = max(start, turn.start)
            overlap_end = min(end, turn.end)
            overlap = max(0, overlap_end - overlap_start)
            speaker_durations[speaker_label] += overlap

        speaker = max(speaker_durations, key=speaker_durations.get, default="Unknown")
        line = f"{speaker} [{format_time(start)} - {format_time(end)}]: {text}"
        lines.append(line)
        print(line)

    # === GUARDAR A TXT ===
    with open("output_transcript.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n✅ Transcripción con locutores guardada en 'output_transcript_complete.txt'")
