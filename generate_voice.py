def run_generate_voice():
    import os
    import sys
    import openai
    from pydub import AudioSegment
    from tempfile import NamedTemporaryFile
    from dotenv import load_dotenv

    # todo tu código actual que traduce y genera voces
    print("✅ Traducción + Generación de voz completa.")
    # Cargar las variables de entorno
    load_dotenv()

    # Agregar FFmpeg al PATH
    ffmpeg_path = os.path.abspath("ffmpeg/bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path

    # === Configuración ===
    openai.api_key = os.getenv("OPENAI_API_KEY")

    output_folder = "audio_openai_grouped"
    os.makedirs(output_folder, exist_ok=True)

    # Voz asignada por speaker
    voice_map = {
        "SPEAKER_00": "echo",     # Masculina
        "SPEAKER_01": "nova"      # Femenina
    }

    # === Leer transcripción ===
    with open("output_transcript.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    grouped_blocks = []
    current_speaker = None
    current_text = []

    # Agrupar por speaker continuo
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

    # Agregar el último bloque
    if current_speaker and current_text:
        grouped_blocks.append((current_speaker, " ".join(current_text)))

    # === Generar audios y armar el podcast ===
    audio_segments = []
    translated_texts = []  # Para guardar el texto traducido

    for i, (speaker, full_text) in enumerate(grouped_blocks):
        try:
            print(f"🔤 Traduciendo bloque {i} de {speaker}...")

            # Traducción con GPT-3.5
            chat_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sos un traductor profesional. Respondé solo con la traducción al español."},
                    {"role": "user", "content": full_text}
                ]
            )
            translated = chat_response.choices[0].message.content.strip()
            print(f"🗣️ Traducción: {translated}")

            translated_texts.append(f"{speaker}: {translated}")

            # Elegir voz para el speaker
            voice = voice_map.get(speaker, "shimmer")

            # Generar voz con TTS
            speech_response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=translated,
                response_format="mp3"
            )

            temp_audio = NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_audio.write(speech_response.content)
            temp_audio.close()

            segment = AudioSegment.from_mp3(temp_audio.name)
            full_block = segment + AudioSegment.silent(duration=700)
            audio_segments.append(full_block)

            os.remove(temp_audio.name)

        except Exception as e:
            print(f"❌ Error en el bloque {i}: {e}")
            continue

    # === Guardar traducciones en archivo txt ===
    with open(os.path.join(output_folder, "traduccion_completa.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_texts))

    # === Combinar todos los segmentos en un solo mp3 ===
    if audio_segments:
        podcast = sum(audio_segments[1:], audio_segments[0]) if len(audio_segments) > 1 else audio_segments[0]
        final_path = os.path.join(output_folder, "podcast_completo.mp3")
        podcast.export(final_path, format="mp3")
        print(f"\n✅ Podcast completo generado en: {final_path}")
    else:
        print("⚠️ No se generó ningún audio.")
