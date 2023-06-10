import re
import utils
import random
import yaml
from configs import FileConfigs as Fc
from google_tts import google_tts


class MessageHandler:
    def __init__(self, message, tags):
        self.message = message
        self.tags = tags

        self.reward_id = None
        self.message_start = 0
        self.display_name = next(item for item in tags if item['key'] == 'display-name')
        self.name = self.display_name['value'].lower()
        self.mod = next(item for item in tags if item['key'] == 'mod')
        self.badges = next(item for item in tags if item['key'] == 'badges')
        self.vip = re.search(r'.*vip.*', str(self.badges.get('value')))
        self.sub = re.search(r'.*subscriber.*', str(self.badges.get('value')))
        self.redeemed = any(item for item in tags if item['key'] == 'custom-reward-id')

        self.command_actions = {
            '!blocktts': self.command_blocktts,
            '!unblocktts': self.command_unblocktts,
            '!addwltts': self.command_addwltts,
            '!delwltts': self.command_delwltts
        }

    def message_conditions(self):
        if self.redeemed:
            reward_id = next(item for item in self.tags if item['key'] == 'custom-reward-id')
            if Fc.tts_reward_id in reward_id.values():
                return True
        if self.message[self.message_start][:len(Fc.tts_prefix)] == Fc.tts_prefix and Fc.no_prefix is False:
            return True
        if Fc.no_prefix is True:
            return True
        return False

    def reward_print(self):
        if self.redeemed:
            reward_id = next(item for item in self.tags if item['key'] == 'custom-reward-id')
            if Fc.tts_reward_id not in reward_id.values():
                print('received reward id:', self.reward_id.get('value'))

    def config_conditions(self):
        if Fc.prefix_allow_all \
                or Fc.prefix_allow_sub and self.sub is not None \
                or Fc.prefix_allow_mod and self.mod['value'] == '1' \
                or Fc.prefix_allow_vip and self.vip is not None \
                or Fc.use_whitelist and self.name in Fc.whitelist_users \
                or self.name == Fc.channel:
            return True
        return False

    def banned_conditions(self):
        if self.name in Fc.blocked_users:
            print('Message blocked. User', self.name, 'present in blocked_users.yaml')
            return True
        if any(word in self.message.lower() for word in Fc.banned_words):
            print('Message blocked. Banned word founded in user', self.name, 'message. Text:', self.message)
            return True
        return False

    def user_conditions(self):
        if self.name in Fc.users.keys():
            user_voices = random.choice(utils.user_voices(Fc.users[self.name]['voice_filter']))
            user_speaking_rate = utils.random_float(Fc.users[self.name]['low_speaking_rate'],
                                                    Fc.users[self.name]['high_speaking_rate'])
            user_pitch = utils.random_float(Fc.users[self.name]['low_pitch'], Fc.users[self.name]['high_pitch'])
            user_message = utils.exclude_from_message(self.message)

            return {'voice': user_voices, 'speaking_rate': user_speaking_rate, 'pitch': user_pitch,
                    'text': user_message}
        else:
            default_voices = random.choice(utils.default_voices())
            default_speaking_rate = utils.random_float(Fc.low_speaking_rate, Fc.high_speaking_rate)
            default_pitch = utils.random_float(Fc.low_pitch, Fc.high_pitch)
            default_message = utils.exclude_from_message(self.message)

            return {'voice': default_voices, 'speaking_rate': default_speaking_rate, 'pitch': default_pitch,
                    'text': default_message}

    def command_conditions(self):
        if self.message[self.message_start][:1] == '!' and Fc.use_mod_commands is True:
            if self.mod['value'] == '1' or self.name == Fc.channel:
                return True
        return False

    def command_blocktts(self):
        blck_message = self.message[len('!blocktts '):]
        if blck_message != Fc.channel and blck_message not in Fc.blocked_users \
                and blck_message != '':
            Fc.blocked_users.append(blck_message)
            print('User', blck_message, 'blocked from tts by', self.name)
            with open('configs/blocked_users.yaml', 'w') as f:
                yaml.dump(Fc.blocked_users, f)

    def command_unblocktts(self):
        unblck_message = self.message[len('!unblocktts '):]
        if unblck_message in Fc.blocked_users and unblck_message != '':
            Fc.blocked_users.remove(unblck_message)
            print('User', unblck_message, 'unblocked from tts by', self.name)
            with open('configs/blocked_users.yaml', 'w') as f:
                yaml.dump(Fc.blocked_users, f)

    def command_addwltts(self):
        addwl_message = self.message[len('!addwltts '):]
        if addwl_message != Fc.channel and addwl_message not in Fc.whitelist_users \
                and addwl_message != '':
            Fc.whitelist_users.append(addwl_message)
            print('User', addwl_message, 'added to whitelist by', self.name)
            with open('configs/whitelist_users.yaml', 'w') as f:
                yaml.dump(Fc.whitelist_users, f)

    def command_delwltts(self):
        delwl_message = self.message[len('!delwltts '):]
        if delwl_message in Fc.whitelist_users and delwl_message != '':
            Fc.whitelist_users.remove(delwl_message)
            print('User', delwl_message, 'deleted from whitelist by', self.name)
            with open('configs/whitelist_users.yaml', 'w') as f:
                yaml.dump(Fc.whitelist_users, f)

    def action_handler(self):
        self.reward_print()
        if self.banned_conditions() is False and self.message_conditions() is True and self.config_conditions() is True:
            voice = self.user_conditions().get('voice')
            speaking_rate = self.user_conditions().get('speaking_rate')
            pitch = self.user_conditions().get('pitch')
            text = self.user_conditions().get('text')

            print(self.name, '-', text, voice, speaking_rate, pitch)
            google_tts('configs/gcp.json', text, voice, float(speaking_rate), float(pitch))

        elif self.command_conditions() is True:
            for command, action in self.command_actions.items():
                if command in self.message:
                    self.command_actions[command]()
