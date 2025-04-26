import argparse
import os
from diarization_transcription import run_diarization_transcription
from generate_voice_coqui import run_generate_voice_coqui


def main():

    # Agregar FFmpeg al PATH
    ffmpeg_path = os.path.abspath("ffmpeg/bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path
    
    # Leer argumentos de consola
    parser = argparse.ArgumentParser(description="Traductor Voz a Voz - Whisper + Pyannote")
    parser.add_argument("--audio_path", type=str, required=True, help="Ruta del archivo de audio de entrada")
    args = parser.parse_args()

    audio_path = args.audio_path

    print(f"🎙️ Procesando audio: {audio_path}")
    
    # 1. Diarizar y transcribir
    # run_diarization_transcription(audio_path)

    # 2. Traducir y generar voz
    run_generate_voice_coqui()

if __name__ == "__main__":
    main()