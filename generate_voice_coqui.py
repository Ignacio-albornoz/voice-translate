def run_generate_voice_coqui():
    import os
    from pydub import AudioSegment
    from tempfile import NamedTemporaryFile
    from googletrans import Translator
    from TTS.api import TTS

    print("✅ Traducción + Generación de voz completa (Coqui TTS).")

    ffmpeg_path = os.path.abspath("ffmpeg/bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path

    output_folder = "audio_coqui_grouped"
    os.makedirs(output_folder, exist_ok=True)

    voice_map = {
        "SPEAKER_00": "tts_models/es/mai/tacotron2-DDC",  # Español voz 1
        "SPEAKER_01": "tts_models/es/css10/vits"  # Español voz 2
    }

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

    if current_speaker and current_text:
        grouped_blocks.append((current_speaker, " ".join(current_text)))

    audio_segments = []
    translated_texts = []
    translator = Translator()

    for i, (speaker, full_text) in enumerate(grouped_blocks):
        try:
            print(f"🔤 Traduciendo bloque {i} de {speaker}...")
            translation = translator.translate(full_text, dest="es")
            translated = translation.text.strip()
            print(f"🗣️ Traducción: {translated}")

            translated_texts.append(f"{speaker}: {translated}")

            model_name = voice_map.get(speaker, "tts_models/es/mai/tacotron2-DDC")
            tts = TTS(model_name)

            temp_audio = NamedTemporaryFile(delete=False, suffix=".wav")
            tts.tts_to_file(text=translated, file_path=temp_audio.name)

            segment = AudioSegment.from_wav(temp_audio.name)
            full_block = segment + AudioSegment.silent(duration=700)
            audio_segments.append(full_block)

            temp_audio.close()
            os.remove(temp_audio.name)

        except Exception as e:
            print(f"❌ Error en el bloque {i}: {e}")
            continue

    with open(os.path.join(output_folder, "traduccion_completa.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_texts))

    if audio_segments:
        podcast = sum(audio_segments[1:], audio_segments[0]) if len(audio_segments) > 1 else audio_segments[0]
        final_path = os.path.join(output_folder, "podcast_completo.wav")
        podcast.export(final_path, format="wav")
        print(f"\n✅ Podcast completo generado en: {final_path}")
    else:
        print("⚠️ No se generó ningún audio.")
