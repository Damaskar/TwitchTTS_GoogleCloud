# TwitchTTS with Google Cloud Text-to-Speech
TTS bot for Twitch chat for user messages and channel rewards, using Google Cloud Text-to-Speech API

## Features:

* Random Google Voice by filters
  - Test voices [Here](https://cloud.google.com/text-to-speech):
  - You can set voice filter for all users in `config.yaml`
  - Use `users.yaml` to set voice filter for individual users
  - Available options:
    - Exactly one voice - `voice_filter: en-US-Standart-A` 
    - By language - `voice_filter: en-US` 
    - By type - `voice_filter: Wavenet` 
    - By both type and language - `voice_filter: en-US-Wavenet` 
    - Set `''` if you want any available voice - `voice_filter: ''`
    - Also you can use list of filter options - `voice_filter: [en-US-Wavenet, nl-NL-Standart, ru-RU, ]`


* Random speaking rate and pitch for voice from range
  - Test voices [Here](https://cloud.google.com/text-to-speech):
  - You can set range for all users in `config.yaml`
  - Use `users.yaml` to set speaking rate and pitch for individual users
  - If you need flat speaking rate or pitch set same number for low and high options
  - Available pitch range: -20 to 20
  - Available speaking rate range: 0.25 to 4


* TTS for chat message with prefix
  - You can change tts_prefix in `config.yaml`
  - You have options to allow this function for different types of users^
    - List of users in `whitelist_users.yaml` if you enable it with use_whitelist option
    - Moderators
    - Subscribers
    - VIP users
    - ALL users


* List of excluded words - `exclude_words.yaml`
  - If TTS message have one of words from this list - they will be removed from TTS message.

* List of banned words - `banned_words.yaml`
  - If TTS message have one of words from this list - nothing will happen.
 
* Block users - `blocked_users.yaml`
  - If user in blocklist try to activate TTS - nothing will happen.
   

* Chat commands for moderators and broadcaster:
  - Enable chat commands in `config.yaml`
  - Available commands:
    - !stoptts - Stop current TTS playback
    - !blocktts - Add user to blacklist, no need to restart TTS. Example: `!blocktts nickname`
    - !unblocktts - Remove user from blacklist, no need to restart TTS. Example: `!unblocktts nickname`
    - !addwltts - Add user to whitelist, no need to restart TTS. Example: `!addwltts nickname`
    - !delwltts - Remove user from whitelist, no need to restart TTS. Example: `!delwltts nickname`
  - You can manually fill and edit this lists in `blocked_users.yaml` and `whitelist_users.yaml`

 


# Requirements: 
* You need [Google Cloud Account](https://cloud.google.com/free) to use [Text-To-Speech API](https://cloud.google.com/text-to-speech).
* Since for TTS playback was used [pydub](https://github.com/jiaaro/pydub) + [simpleaudio](https://github.com/hamiltron/py-simple-audio) libs, you'll need to install [ffmpeg](http://www.ffmpeg.org/) or [libav](http://libav.org/).

## Google Cloud Setup:

1. First you need google cloud account. Register free account [Here](https://cloud.google.com/free).
2. Create a project or use existing on in the [Cloud Console](https://console.cloud.google.com/).
3. Enable **billing** for your project, it's necessary to use Google API.
Google Cloud give you 4 million characters for Standard voices 
and 1 million characters for WaveNet voice for free per month.
It's more than enough for TTS in Twitch chat, 
but I suggest you to set up 0$ budget just in case.
4. Go to **APIs & Services**:
   - Press **ENABLE APIS AND SERVICES** button
   - Search for **Cloud Text-to-Speech API**
   - Enable API
5. In **APIs & Services**:
   - Go to **Credentials**
   - Press **CREATE CREDENTIALS** button and select **Service account**
   - Fill name and ID for service account
   - Select a role for service account, you can use **Project > Owner**
6. Select your new service account
   - Go to **KEYS**
   - Press **ADD KEY** and select **Create new key**
   - Select **JSON** key type
7. After creating json key your browser will automatically download
.json file, rename it to **gcp.json** and save it, we will need it later.
8. Don't share your service account key for obvious security purposes.

## Getting ffmpeg / libav set up:

### Windows:

ffmpeg:
1. Download and extract ffmpeg using [Windows builds from here](https://ffmpeg.org/download.html#build-windows).
2. Add the ffmpeg `/bin` folder to your PATH envvar

libav:
1. Download and extract libav from [Windows binaries provided here](http://builds.libav.org/windows/).
2. Add the libav `/bin` folder to your PATH envvar

### Mac (using [homebrew](http://brew.sh)):

```bash
# libav
brew install libav

####    OR    #####

# ffmpeg
brew install ffmpeg
```

### Linux (using aptitude):

```bash
# libav
apt-get install libav-tools libavcodec-extra

####    OR    #####

# ffmpeg
apt-get install ffmpeg libavcodec-extra
```

# Download: [Releases](https://github.com/damaskar/TwitchTTS/releases)

# Setup:
1. Make sure you have [requirements](#Requirements:) listed above (gcp.json in configs folder and ffmpeg/libav).
2. Download the latest release and extract release to any folder on your pc.
3. Replace example gcp.json with your Service account key from [requirements](#Requirements:) in **TTS Folder\configs**. 
4. Get Twitch Chat OAuth Token from [Here](https://twitchapps.com/tmi/)
5. Put your channel, username and OAuth Token into **configs/config.yaml** (you can use any text editor).
6. Fill .yaml files with your settings, every .yaml file has commends to help you with syntax.
7. If you want to use channel points reward:
    - Start TwitchTTS.exe and wait until it join channel
    - Use your desired points reward in chat
    - You will get reward ID in console
    - Put that reward ID into config.yaml


# Changelog:
- **v1.1**, 10.06.2023
  - Completely rewrite code.
  - Add new feature to be able TTS all messages.
  - Multiple bugs fixed.
- **v1.0**, 27.05.2022
  - Initial release

# If you want to support me, click here: [Donate](https://www.donationalerts.com/r/damaskarr)
