import irc.bot
import threading
import time
from pprint import pprint

import utils
from configs import FileConfigs as Fc
from message_handler import MessageHandler


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

    def on_pubmsg(self, connection, event):
        """
        Method for chat events.

        Checks for:
            If user or some word in message are blocked.
            Points reward redeem or prefix used in chat message and user has rights for TTS.
            If mod commands allowed and was used.
        """
        message = MessageHandler(event.arguments[0], event.tags)
        message.action_handler()


if __name__ == '__main__':
    """Print configuration and voices"""
    try:
        print('\nChannel:', Fc.channel, '\nBot username:', Fc.bot_username, '\nBot token:',
              Fc.bot_token[6:9] + '*' * (len(Fc.bot_token) - 9), '\nTTS Reward ID:', Fc.tts_reward_id)
        print('\nFiltered voices for TTS:')
        pprint(utils.default_voices())

        """Initialize bot and speach threads"""

        bot = ChatBot(Fc.bot_username, Fc.bot_token, Fc.channel)
        bot_thread = threading.Thread(target=bot.start, name='bot_thread', daemon=True)

        bot_thread.start()

        bot_thread.join()
    except Exception as e:
        print('\nError:', e, '\n')
        input('Press enter to exit')
