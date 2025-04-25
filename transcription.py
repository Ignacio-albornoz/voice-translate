import whisper

model = whisper.load_model("base")
result = model.transcribe(r"C:\Users\ignac\voice-translate\audio_input\input2.wav")

# Guardar solo el texto completo
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

# Guardar con timestamps por segmento
with open("segments.txt", "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        f.write(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}\n")

print("✅ Transcripción guardada como transcription.txt y segments.txt")
