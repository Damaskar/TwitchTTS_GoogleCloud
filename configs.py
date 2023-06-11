import yaml


class FileConfigs:
    """Open config files and set up variables"""

    try:
        with open('configs/config.yaml', 'r', encoding='UTF8') as f:
            config = yaml.safe_load(f)
            channel = config['authorization']['channel'].lower()
            bot_username = config['authorization']['bot_username'].lower()
            bot_token = config['authorization']['bot_token'].lower()
            tts_reward_id = config['general_options']['tts_reward_id']
            show_reward_id = config['general_options']['show_reward_id']
            volume = config['voice_settings']['volume']
            sample_rate = config['voice_settings']['sample_rate']
            voice_filter = config['voice_settings']['voice_filter']
            low_speaking_rate = config['voice_settings']['low_speaking_rate']
            high_speaking_rate = config['voice_settings']['high_speaking_rate']
            low_pitch = config['voice_settings']['low_pitch']
            high_pitch = config['voice_settings']['high_pitch']
            use_whitelist = config['features']['use_whitelist']
            use_mod_commands = config['features']['use_mod_commands']
            no_prefix = config['prefix_options']['no_prefix']
            tts_prefix = config['prefix_options']['tts_prefix']
            prefix_allow_mod = config['prefix_options']['prefix_allow_mod']
            prefix_allow_sub = config['prefix_options']['prefix_allow_sub']
            prefix_allow_vip = config['prefix_options']['prefix_allow_vip']
            prefix_allow_all = config['prefix_options']['prefix_allow_all']

        with open('configs/users.yaml', 'r', encoding='UTF8') as f:
            u = yaml.safe_load(f)
            users = {k.lower(): v for k, v in u.items()}

        with open('configs/blocked_users.yaml', 'r', encoding='UTF8') as f:
            bu = yaml.safe_load(f)
            blocked_users = [v.lower() for v in bu]

        with open('configs/banned_words.yaml', 'r', encoding='UTF8') as f:
            bw = yaml.safe_load(f)
            banned_words = [v.lower() for v in bw]

        with open('configs/whitelist_users.yaml', 'r', encoding='UTF8') as f:
            wu = yaml.safe_load(f)
            whitelist_users = [v.lower() for v in wu]

        with open('configs/exclude_words.yaml', 'r', encoding='UTF8') as f:
            ew = yaml.safe_load(f)
            exclude_words = [v.lower() for v in ew]

    except Exception as e:
        print('\nError:', e)