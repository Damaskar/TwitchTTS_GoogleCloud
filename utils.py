import random
from configs import FileConfigs as Fc
from google_tts import google_list


def list_voices():
    """Return list of voices"""
    return google_list('configs/gcp.json')


def default_voices():
    """Function to get random voice for unknown user"""

    if isinstance(Fc.voice_filter, str):
        return random.choice([voice for voice in list_voices() if Fc.voice_filter in voice])
    elif isinstance(Fc.voice_filter, list):
        v = random.choice(Fc.voice_filter)
        return random.choice([voice for voice in list_voices() if v in voice])
    else:
        return None


def user_voices(user_voice_filter):
    """Function to get random voice for user presented in users.yaml"""

    if isinstance(user_voice_filter, str):
        return random.choice([voice for voice in list_voices() if user_voice_filter in voice])
    elif isinstance(user_voice_filter, list):
        v = random.choice(user_voice_filter)
        return random.choice([voice for voice in list_voices() if v in voice])
    else:
        return None


def random_float(low, high):
    """Function to get random float from range"""

    return round(random.uniform(low, high), 2)


def exclude_from_message(message):
    """Remove words presented in exclude_words from message"""

    for word in Fc.exclude_words:
        message = message.replace(word, '').replace(Fc.tts_prefix, '')
    if message != '':
        return message
    else:
        return '*'
