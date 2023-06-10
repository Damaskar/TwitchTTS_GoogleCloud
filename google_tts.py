import os
from typing import List
from io import BytesIO
from pydub import AudioSegment
from pydub import playback
from google.cloud import texttospeech


def list_voices(client) -> List[str]:
    """Convert voices to list"""

    return [voice.name for voice in client.list_voices().voices]


def google_list(json):
    """Return available voices from google api"""

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json
    client = texttospeech.TextToSpeechClient()
    available_voices = list_voices(client=client)
    try:
        return available_voices
    except Exception as e:
        print('\nError:', e)


def google_tts(json, text, voice, speaking_rate, pitch):
    """TTS function"""

    global play_obj

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)

    try:
        fp = BytesIO()
        fp.write(response.audio_content)
        fp.seek(0)
        audio = AudioSegment.from_mp3(fp)
        playback.play(audio)
    except Exception as e:
        print('\nError:', e)

def stop_tts():
    """Stop current playback"""

    play_obj.stop()