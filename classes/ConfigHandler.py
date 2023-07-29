import configparser
from pathlib import Path
import constants


class ConfigHandler:
    def __init__(self):
        self.configParser = configparser.ConfigParser()

        self.default_data = {
            'ENVIRONMENT': {
                'SCALE': '2',
                'WINDOW_WIDTH': '320',
                'WINDOW_HEIGHT': '240'
            },
            'DUNGEON': {
                'DUNGEON_MAX_WIDTH': '8',
                'DUNGEON_MAX_HEIGHT': '8',
                'DUNGEON_MIN_DISTANCE_BTW_P_AND_D': '4',
                'DUNGEON_MIN_DISTANCE_DRAG_AWAKE': '3',
                'DUNGEON_MAX_NBR_WALLS': '40',
            },
            'LANGUAGE': {
                'LNG': 'FRENCH'
            },
            'TEXTS_ENGLISH': {
                'TEXT_YES': 'Yes',
                'TEXT_NO': 'No',
                'TEXT_HINT_CHOOSE_START_ROOM': 'Please use the arrow keys to select your starting point.',
                'TEXT_Q_SURE': 'Are you sure ?',
                'TEXT_DRAGON_PLACE': 'The Dragon is taking his place...',
                'TEXT_DRAGON_TURN': 'The Dragon is flying...',
                'TEXT_DRAGON_AWAKE': 'The Dragon is awakening !',
                'TEXT_DRAGON_ATTACK': 'The Dragon strikes you !',
                'TEXT_TREASURE_FOUND': 'You found the treasure !',
                'TEXT_TREASURE_TAKE': 'You take the treasure back.',
                'TEXT_WIN': 'You win !',
                'TEXT_LOSE': 'You lose...',
                'TEXT_NEED_CONFIG_CONTROLS_A': 'Press button for A',
                'TEXT_NEED_CONFIG_CONTROLS_B': 'Press button for B',
                'TEXT_NEED_CONFIG_CONTROLS_UP': 'Press button for UP',
                'TEXT_NEED_CONFIG_CONTROLS_DOWN': 'Press button for DOWN',
                'TEXT_NEED_CONFIG_CONTROLS_LEFT': 'Press button for LEFT',
                'TEXT_NEED_CONFIG_CONTROLS_RIGHT': 'Press button for RIGHT'
            },
            'TEXTS_FRENCH': {
                'TEXT_YES': 'Oui',
                'TEXT_NO': 'Non',
                'TEXT_HINT_CHOOSE_START_ROOM': 'Sélectionnez votre salle de départ.',
                'TEXT_Q_SURE': 'Etes-vous sûr ?',
                'TEXT_DRAGON_PLACE': 'Le Dragon se met en place...',
                'TEXT_DRAGON_TURN': 'Le Dragon se déplace...',
                'TEXT_DRAGON_AWAKE': 'Le Dragon se réveille !',
                'TEXT_DRAGON_ATTACK': 'Le Dragon vous attaque !',
                'TEXT_TREASURE_FOUND': 'Vous avez trouver le trésor !',
                'TEXT_TREASURE_TAKE': 'Vous reprenez le trésor.',
                'TEXT_WIN': 'Vous avez gagné !',
                'TEXT_LOSE': 'Vous avez perdu...',
                'TEXT_NEED_CONFIG_CONTROLS_A': 'Press button for A',
                'TEXT_NEED_CONFIG_CONTROLS_B': 'Press button for B',
                'TEXT_NEED_CONFIG_CONTROLS_UP': 'Press button for UP',
                'TEXT_NEED_CONFIG_CONTROLS_DOWN': 'Press button for DOWN',
                'TEXT_NEED_CONFIG_CONTROLS_LEFT': 'Press button for LEFT',
                'TEXT_NEED_CONFIG_CONTROLS_RIGHT': 'Press button for RIGHT'
            },
            'CONTROLS': {
                'CONTROL_UP': 'None',
                'CONTROL_DOWN': 'None',
                'CONTROL_LEFT': 'None',
                'CONTROL_RIGHT': 'None',
                'CONTROL_A': 'None',
                'CONTROL_B': 'None'
            }
        }

        #if not os.path.exists('config.ini'):
        if not (constants.root / "config.ini").exists():
            self.createConfigFile()

        #self.configFilePath = os.path.join(os.path.dirname(__file__), '../config.ini')
        self.configFilePath = "config.ini"
        self.configParser.read(self.configFilePath)

        self.needConfigControls = False
        self.checkControls()

    def checkControls(self):
        print(self.configParser)
        controls_option = dict(self.configParser.items('CONTROLS'))

        for option_name, value in controls_option.items():
            if value == 'None':
                self.needConfigControls = True

    def get(self, option_name_wanted):
        for section_name, options in self.default_data.items():
            for option_name, value in options.items():
                if option_name == option_name_wanted:
                    section = self.configParser[section_name]
                    temp = section.get(option_name, self.default_data[section_name][option_name])
                    if temp == 'None':
                        return 0
                    return temp

    def set(self, option_name_wanted, value_set):
        for section_name, options in self.default_data.items():
            for option_name, value in options.items():
                if option_name == option_name_wanted:
                    self.configParser.set(section_name, option_name, str(value_set))

                    with open('config.ini', 'w') as configfile:
                        self.configParser.write(configfile)

    def getL(self, option_name_wanted):
        lng = self.configParser.get('LANGUAGE', 'LNG')
        section = self.configParser['TEXTS_' + lng]
        return section.get(option_name_wanted, self.default_data['TEXTS_' + lng][option_name_wanted])

    def createConfigFile(self):
        for section_name, options in self.default_data.items():
            if not self.configParser.has_section(section_name):
                self.configParser.add_section(section_name)

            for option_name, value in options.items():
                if not self.configParser.has_option(section_name, option_name):
                    self.configParser[section_name][option_name] = str(value)

        with open('config.ini', 'w') as configfile:
            self.configParser.write(configfile)
