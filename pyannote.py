from pyannote.audio import Pipeline
from dotenv import load_dotenv
import whisper

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

#Cargar modelos
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=HUGGINGFACE_TOKEN)
whisper_model = whisper.load_model("medium")  # Puedes usar 'base', 'small', etc.

#Procesar audio con ambos modelos
AUDIO_FILE = "./audio_input/input2.wav"
NUM_SPEAKERS = 2
diarization = diarization_pipeline(AUDIO_FILE, num_speakers=NUM_SPEAKERS)
whisper_result = whisper_model.transcribe(AUDIO_FILE, word_timestamps=True)

#Convertir los segmentos de diarización en lista para trabajar
diar_segments = []
for turn in diarization.itertracks(yield_label=True):
    start, end, speaker = turn[0].start, turn[0].end, turn[2]
    diar_segments.append({"start": start, "end": end, "speaker": speaker})

#Asignar texto transcrito a cada segmento de hablante
output = []

for seg in diar_segments:
    speaker = seg["speaker"]
    start_time = seg["start"]
    end_time = seg["end"]

    # Buscar palabras de Whisper que estén dentro del rango de este hablante
    words_in_segment = []
    for segment in whisper_result["segments"]:
        for word in segment.get("words", []):  # 'words' solo está si usas word_timestamps=True
            if word["start"] >= start_time and word["end"] <= end_time:
                words_in_segment.append(word["word"])

    if words_in_segment:
        text = " ".join(words_in_segment).strip()
        output.append(f"{speaker} [{start_time:.2f} → {end_time:.2f}]: {text}")

#Guardar o imprimir
with open("diarized_transcription.txt", "w", encoding="utf-8") as f:
    for line in output:
        print(line)
        f.write(line + "\n")