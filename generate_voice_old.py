import os
import openai
from dotenv import load_dotenv

# === Configuración ===
openai.api_key = os.getenv("OPENAI_API_KEY")
output_folder = "audio_openai_grouped"
os.makedirs(output_folder, exist_ok=True)

# === CARGAR EL ARCHIVO DE TRANSCRIPCIÓN ===
with open("output_transcript.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

grouped_blocks = []
current_speaker = None
current_text = []

for line in lines:
    if not line.strip():
        continue

    try:
        speaker_part, text = line.strip().split("]:", 1)
        speaker = speaker_part.split()[0]
        text = text.strip()

        if speaker != current_speaker:
            if current_speaker is not None:
                grouped_blocks.append((current_speaker, " ".join(current_text)))
            current_speaker = speaker
            current_text = [text]
        else:
            current_text.append(text)
    except Exception as e:
        print(f"❌ Error procesando línea: {line} — {e}")
        continue

# Agregar último bloque
if current_speaker and current_text:
    grouped_blocks.append((current_speaker, " ".join(current_text)))

# === USAR OPENAI GPT PARA TRADUCIR Y LUEGO OPENAI TTS PARA LEER ===
print("🔁 Traduciendo y generando audio con OpenAI...")

for i, (speaker, full_text) in enumerate(grouped_blocks):
    try:
        print(f"🔤 Traduciendo bloque {i} de {speaker}...")

        # Llamada a OpenAI GPT para traducir
        chat_completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sos un traductor profesional. Respondé solo con la traducción al español."},
                {"role": "user", "content": full_text}
            ]
        )
        translated = chat_completion.choices[0].message.content.strip()
        print(f"{speaker}: {translated}")

        # Generar voz en español
        print("🎙️ Generando voz...")
        speech_response = openai.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=translated,
            response_format="mp3"
        )

        filename = os.path.join(output_folder, f"{i:03d}_{speaker}.mp3")
        with open(filename, "wb") as f:
            f.write(speech_response.content)

    except Exception as e:
        print(f"❌ Error en el bloque {i}: {e}")
        continue

print(f"\n✅ Audios generados con OpenAI guardados en '{output_folder}'")
