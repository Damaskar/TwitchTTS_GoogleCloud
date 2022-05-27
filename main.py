import irc.bot
import random
import re
import threading
import time
import yaml
from pprint import pprint

import utils
from configs import FileConfigs as Fc
from google_tts import google_tts, stop_tts


class ChatBot(irc.bot.SingleServerIRCBot):
    """
    Base IRC class to work with Twitch chat implemented by irc library
    """

    def __init__(self, username, token, channel):
        """
        Connect to twitch irc server.

        Arguments:
            username - User for bot to connect as
            token - User OAuth token
            channel - Channel name what bot will join
        """

        self.username = username
        self.token = token
        self.channel = '#' + channel
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('\nConnecting to', server + ':' + str(port), '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)

    def on_welcome(self, connection, event):
        """Join twitch channel after successful connection"""

        connection.cap('REQ', ':twitch.tv/tags')
        connection.join(self.channel)
        print('Joined chat:', self.channel)

    def on_disconnect(self, connection, event):
        """If connection is lost or failed - try to reconnect"""

        print('Disconnected from', self.channel, ', trying to reconnect ...')
        time.sleep(2)
        bot.start()

    def tts_custom_user(self, event, name):
        """Queue voice parameters and text for user presented in users.yaml"""

        tts_wait_voice.append(
            utils.user_voices(Fc.users[name]['voice_filter']))
        tts_wait_speaking_rate.append(
            utils.random_float(Fc.users[name]['low_speaking_rate'], Fc.users[name]['high_speaking_rate']))
        tts_wait_pitch.append(
            utils.random_float(Fc.users[name]['low_pitch'], Fc.users[name]['high_pitch']))
        tts_wait_text.append(utils.exclude_from_message(event))

    def tts_default_user(self, event):
        """Queue default voice parameters and text from config.yaml for unknown users"""

        tts_wait_voice.append(
            random.choice(utils.default_voices()))
        tts_wait_speaking_rate.append(
            utils.random_float(Fc.low_speaking_rate, Fc.high_speaking_rate))
        tts_wait_pitch.append(
            utils.random_float(Fc.low_pitch, Fc.high_pitch))
        tts_wait_text.append(utils.exclude_from_message(event))

    def on_pubmsg(self, connection, event):
        """
        Method for chat events.

        Checks for:
            If user or some word in message are blocked.
            Points reward redeem or prefix used in chat message and user has rights for TTS.
            If mod commands allowed and was used.
        """

        global name

        display_name = next(item for item in event.tags if item['key'] == 'display-name')
        name = display_name['value'].lower()
        mod = next(item for item in event.tags if item['key'] == 'mod')
        badges = next(item for item in event.tags if item['key'] == 'badges')
        vip = re.search(r'.*vip.*', str(badges.get('value')))
        sub = re.search(r'.*subscriber.*', str(badges.get('value')))

        if name in Fc.blocked_users:
            print('Message blocked. User', name, 'present in blocked_users.yaml')
        elif any(word in event.arguments[0].lower() for word in Fc.banned_words):
            print('Message blocked. Banned word founded in user', name, 'message. Text:', event.arguments[0])
        else:
            """Check for twitch point redeem"""
            if any(item for item in event.tags if item['key'] == 'custom-reward-id'):
                reward_id = next(item for item in event.tags if item['key'] == 'custom-reward-id')

                if Fc.tts_reward_id in reward_id.values() and display_name['value'].lower() in Fc.users.keys():
                    self.tts_custom_user(event.arguments[0], name)

                elif Fc.tts_reward_id in reward_id.values() and display_name['value'].lower() not in Fc.users.keys():
                    self.tts_default_user(event.arguments[0])

                elif Fc.tts_reward_id not in reward_id.values():
                    print('received reward id:', reward_id.get('value'))

            if event.arguments[0][:1] == Fc.tts_prefix and event.arguments[0][1:] != '':
                """Check if message starts from TTS prefix"""

                if Fc.prefix_allow_all:
                    self.tts_default_user(event.arguments[0][1:])

                elif name == Fc.channel:
                    self.tts_default_user(event.arguments[0][1:])

                elif Fc.use_whitelist and name in Fc.whitelist_users and name in Fc.users.keys():
                    self.tts_custom_user(event.arguments[0][1:], name)

                elif Fc.use_whitelist and name in Fc.whitelist_users and name not in Fc.users.keys():
                    self.tts_default_user(event.arguments[0][1:])

                elif Fc.prefix_allow_mod and mod['value'] == '1' and name in Fc.users.keys():
                    self.tts_custom_user(event.arguments[0][1:], name)

                elif Fc.prefix_allow_mod and mod['value'] == '1' and name not in Fc.users.keys():
                    self.tts_default_user(event.arguments[0][1:])

                elif Fc.prefix_allow_vip and vip is not None and name in Fc.users.keys():
                    self.tts_custom_user(event.arguments[0][1:], name)

                elif Fc.prefix_allow_vip and vip is not None and name not in Fc.users.keys():
                    self.tts_default_user(event.arguments[0][1:])

                elif Fc.prefix_allow_sub and sub is not None and name in Fc.users.keys():
                    self.tts_custom_user(event.arguments[0][1:], name)

                elif Fc.prefix_allow_sub and sub is not None and name not in Fc.users.keys():
                    self.tts_default_user(event.arguments[0][1:])

            if Fc.use_mod_commands and mod['value'] == '1' or name == Fc.channel and event.arguments[0][:1] == '!':
                """Check if command was used by legit moderator and message is not empty"""

                if event.arguments[0] == '!stoptts':
                    """Stop current playback"""
                    stop_tts()

                elif event.arguments[0][:9] == '!blocktts':
                    """Add user to blacklist"""

                    if event.arguments[0][10:] != Fc.channel and event.arguments[0][10:] not in Fc.blocked_users \
                            and event.arguments[0][10:] != '':
                        Fc.blocked_users.append(event.arguments[0][10:])
                        print('User', event.arguments[0][10:], 'blocked from tts by', name)
                        with open('configs/blocked_users.yaml', 'w') as f:
                            yaml.dump(Fc.blocked_users, f)

                elif event.arguments[0][:11] == '!unblocktts':
                    """Remove user from blacklist"""

                    if event.arguments[0][12:] in Fc.blocked_users and event.arguments[0][12:] != '':
                        Fc.blocked_users.remove(event.arguments[0][12:])
                        print('User', event.arguments[0][12:], 'unblocked from tts by', name)
                        with open('configs/blocked_users.yaml', 'w') as f:
                            yaml.dump(Fc.blocked_users, f)

                elif event.arguments[0][:9] == '!addwltts':
                    """Add user to whitelist"""

                    if event.arguments[0][10:] != Fc.channel and event.arguments[0][10:] not in Fc.whitelist_users \
                            and event.arguments[0][10:] != '':
                        Fc.whitelist_users.append(event.arguments[0][10:])
                        print('User', event.arguments[0][10:], 'added to whitelist by', name)
                        with open('configs/whitelist_users.yaml', 'w') as f:
                            yaml.dump(Fc.whitelist_users, f)

                elif event.arguments[0][:9] == '!delwltts':
                    """Remove user from whitelist"""

                    if event.arguments[0][10:] in Fc.whitelist_users and event.arguments[0][10:] != '':
                        Fc.whitelist_users.remove(event.arguments[0][10:])
                        print('User', event.arguments[0][10:], 'deleted from whitelist by', name)
                        with open('configs/whitelist_users.yaml', 'w') as f:
                            yaml.dump(Fc.whitelist_users, f)


def speach():
    """Use queued TTS from ChatBot and play it using google_tts function"""

    global tts_wait_text, tts_wait_voice, tts_wait_pitch, tts_wait_speaking_rate
    tts_wait_text = []
    tts_wait_voice = []
    tts_wait_pitch = []
    tts_wait_speaking_rate = []
    while True:
        time.sleep(1)
        if len(tts_wait_text) > 0:
            text = tts_wait_text.pop(0)
            voice = tts_wait_voice.pop(0)
            speaking_rate = tts_wait_speaking_rate.pop(0)
            pitch = tts_wait_pitch.pop(0)
            print(name, '-', text, voice, speaking_rate, pitch)
            google_tts('configs/gcp.json', text, voice, float(speaking_rate), float(pitch))


if __name__ == '__main__':
    """Print configuration and voices"""
    try:
        print('Configuration - Channel:', Fc.channel, 'Bot username:', Fc.bot_username, 'Bot token:',
              Fc.bot_token[6:9] + '*' * (len(Fc.bot_token) - 9), 'TTS Reward ID:', Fc.tts_reward_id)
        print('\nFiltered voices for TTS:')
        pprint(utils.default_voices())

        """Initialize bot and speach threads"""

        bot = ChatBot(Fc.bot_username, Fc.bot_token, Fc.channel)
        bot_thread = threading.Thread(target=bot.start, name='bot_thread', daemon=True)
        speach_thread = threading.Thread(target=speach, name='speach_thread', daemon=True)

        bot_thread.start()
        speach_thread.start()

        bot_thread.join()
        speach_thread.join()
    except Exception as e:
        print('\nError:', e, '\n')
        input('Press enter to exit')
