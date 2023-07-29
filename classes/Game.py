from pathlib import Path

from pygame.locals import *
from classes.Printables.Background import Background
from classes.Printables.Cursor import Cursor
from classes.Printables.Dragon import Dragon
from classes.Printables.Dungeon import Dungeon
from classes.Printables.Player import Player
from classes.Printables.TextZone import TextZone
from classes.Printables.Side import Side
from classes.SpriteSet import SpriteSet
from classes.Printables.Tilerender import Renderer
from constants import *
from constants import GameState as Gs
from constants import PrintableNames as Pn
from constants import DoNow as Dn


"""
This is a kind of handler for the game.
The GAME object contains all the Printable object (that it, all the components which are visible on the screen) that are
used in the game.
The GAME object is instantiated in the _init() function.
GAME has different kind of state, like TITLE (for the title screen), PLAY (for gameplay), etc. And so a 
getNameOfStateSurface for getting a Surface which takes all the WINDOW place, with all the Printable objects arranged
on the screen as needed.
GAME also contains two lists of sprites (actually SpriteofSpritesSheet object). One indexed with sprites ID, and another 
with the same sprites, but index with their position on the sprite_set image. 
"""


class Game:

    def __init__(self):
        self.assetsPath = Path(root / "assets")

        self.sprites_sets = {
            'gui': SpriteSet(self.assetsPath / "GUI.png", SPRITE_WIDTH, SPRITE_HEIGHT),
            'overworldL': SpriteSet(self.assetsPath / "Overworld (Light).png", 16, 16)
        }

        self.state = None

        # Sounds
        self.sounds = {
            Sounds.CURSOR: pygame.mixer.Sound(self.assetsPath / "sounds" / 'cursor.wav'),
            Sounds.SELECT: pygame.mixer.Sound(self.assetsPath / "sounds" / 'select.wav'),
            Sounds.LETTER: pygame.mixer.Sound(self.assetsPath / "sounds" / 'letter.wav'),
            Sounds.TEXT_DONE: pygame.mixer.Sound(self.assetsPath / "sounds" / 'text_Done.wav'),
            Sounds.WALL: pygame.mixer.Sound(self.assetsPath / "sounds" / 'wall.wav'),
            Sounds.DRAGON_FLY: pygame.mixer.Sound(self.assetsPath / "sounds" / 'dragon_fly.wav'),
            Sounds.DRAGON_AWAKE: pygame.mixer.Sound(self.assetsPath / "sounds" / 'dragoon_awake.wav'),
            Sounds.HURT_PLAYER: pygame.mixer.Sound(self.assetsPath / "sounds" / 'hurt.wav'),
            Sounds.TELEPORT_PLAYER: pygame.mixer.Sound(self.assetsPath / "sounds" / 'teleport.wav'),
            Sounds.WALK_PLAYER: pygame.mixer.Sound(self.assetsPath / "sounds" / 'walk.wav'),
            Sounds.FOUND_TREASURE: pygame.mixer.Sound(self.assetsPath / "sounds" / 'found_treasure.wav'),
            Sounds.GET_ITEM: pygame.mixer.Sound(self.assetsPath / "sounds" / 'get_item.wav'),
            Sounds.WIN: pygame.mixer.Sound(self.assetsPath / "sounds" / 'win.wav'),
            Sounds.BOUNCE: pygame.mixer.Sound(self.assetsPath / "sounds" / 'bounce.wav')
        }

        # Printable objects
        self.printables = {
            Pn.BACKGROUND: Background(self, zoom=2),
            Pn.DUNGEON: Dungeon(self, zoom=2),
            Pn.DRAGON: Dragon(self, zoom=2),
            Pn.PLAYER: Player(self, zoom=2),
            Pn.CURSOR: Cursor(self, zoom=2),
            Pn.SIDE: Side(self, zoom=2),
            Pn.TEXT_ZONE: TextZone(self, zoom=2),
            Pn.TITLE_SCREEN: Renderer(self, self.assetsPath / 'title.tmx', 2)
        }

        self.getPrintable(Pn.CURSOR).actual_room = self.getPrintable(Pn.DUNGEON).rooms[0][0]

        self.title_img = pygame.image.load(self.assetsPath / 'title.png').convert_alpha()
        self.title_img = pygame.transform.scale(
            self.title_img,
            (int(self.title_img.get_width() / 2.75), int(self.title_img.get_height() / 2.75))
        )
        self.last_state = False

        self.shuffle = False
        self.shuffle_sign = 1
        self.shuffle_current_offset = 0
        self.shuffle_current_frame = 0
        self.offset_x = 0
        self.offset_y = 0

        self.hurting_player = False
        self.picking_treasure = False
        self.ending = False

    def getPrintable(self, name):
        return self.printables[name]

    def showText(self):
        self.getPrintable(Pn.TEXT_ZONE).show()

    def setVisibleAll(self, value):
        for name, printable in self.printables.items():
            printable.visible = value

    def setFreezeAll(self, value):
        for name, printable in self.printables.items():
            printable.visible = value

    def changeState(self, state):
        title_screen = self.getPrintable(Pn.TITLE_SCREEN)
        background = self.getPrintable(Pn.BACKGROUND)
        dungeon = self.getPrintable(Pn.DUNGEON)
        cursor = self.getPrintable(Pn.CURSOR)
        text_zone = self.getPrintable(Pn.TEXT_ZONE)
        side = self.getPrintable(Pn.SIDE)
        dragon = self.getPrintable(Pn.DRAGON)
        player = self.getPrintable(Pn.PLAYER)

        self.last_state = self.state
        self.state = state

        if state == Gs.TITLE:
            title_screen.visible = True
        elif state == Gs.ROOM_SELECTION:
            title_screen.visible = False
            background.visible = True
            dungeon.visible = True
            dungeon.position = [SPRITE_WIDTH * 10, SPRITE_HEIGHT * 5]
            cursor.visible = True
            self.updateScreenPositionForVisiblePrintable()
            text_zone.setNewText(TEXT_HINT_CHOOSE_START_ROOM)
            self.showText()
        elif state == Gs.INITIALISATION:
            cursor.visible = False
            background.color = BACKGROUND_COLOR_2
            # Initialise the translation of the dungeon board with no DoNow action at the end
            dungeon.initialiseTranslation(
                Direction.LEFT,
                Direction.UP,
                dungeon.position,
                [0, 0],
                0.75
            )
            player.visible = True
        elif state == Gs.PLAY:
            d_width = dungeon.getSurface().get_width()
            s_width = side.getSurface().get_width()

            background.color = BACKGROUND_COLOR_5
            dragon.visible = False
            side.visible = True
            side.initialiseTranslation(
                Direction.LEFT,
                None,
                [d_width + s_width, 0],
                [d_width, 0],
                2
            )
            self.updateScreenPositionForVisiblePrintable()
            player.freeze = True
        elif state == Gs.CONFIG_CONTROLS:
            background.visible = True
            background.color = BACKGROUND_COLOR_1
            background.initialiseTranslation(
                Direction.LEFT,
                Direction.UP,
                [0, 0],
                [-64, -64],
                1,
                Dn.REDO_TRANSLATION
            )
            text_zone.setNewText(TEXT_NEED_CONFIG_CONTROLS_A, do_on_end_text=Dn.SET_BUTTON_A, get_key=True)
            self.showText()
            background.freeze = False

    def isOnStateOrOnTextWith(self, state):
        return self.state == state or (self.state == Gs.TEXT_DISPLAY and self.last_state == state)

    def getSprite(self, x, y, spriteSetName='gui'):
        return self.sprites_sets[spriteSetName].sprites[y][x].image

    def getSpriteById(self, sprite_id, spriteSetName='gui'):
        return self.sprites_sets[spriteSetName].spritesById[sprite_id].image

    def handleEvents(self, event):
        textZone = self.getPrintable(Pn.TEXT_ZONE)
        dungeon = self.getPrintable(Pn.DUNGEON)
        player = self.getPrintable(Pn.PLAYER)
        dragon = self.getPrintable(Pn.DRAGON)
        background = self.getPrintable(Pn.BACKGROUND)

        # Player turn is finished
        if event.type == PLAYER_TURN_FINISHED and not self.ending:
            if not dragon.asleep:
                dragon.doDragonTurn()
            else:
                player.refreshPlayerMove()
        elif event.type == PLAYER_BLOCK:
            self.shuffle = True
        # End of printables translations
        elif event.type == END_TRANSLATION:
            if self.state == Gs.INITIALISATION:
                if event.printable == dungeon:
                    # Set the text indicates the dragon place is initialized, with the order to set the PLAY state after
                    textZone.setNewText(TEXT_DRAGON_PLACE, do_on_end_text=Dn.SET_PLAY_STATE)
                    event = pygame.event.Event(TEXT_ZONE_SHOW)
                    pygame.event.post(event)
                    # Set the dragon start room
                    dragon.setDragonRoom()
            elif self.state == Gs.PLAY:
                player.freeze = False
            elif self.state == Gs.CONFIG_CONTROLS:
                if event.printable == background and event.doNow == Dn.REDO_TRANSLATION:
                    background.redoTranslation()

        # Text Zone events
        elif event.type == TEXT_ZONE_SHOW:
            self.showText()
        elif event.type == TEXT_ZONE_DISMISS:
            # Set the PLAY state
            if event.doNow == Dn.SET_PLAY_STATE:
                self.changeState(Gs.PLAY)
            elif event.doNow == Dn.MOVE_DRAGON:
                player.refreshPlayerMove()
                dragon.move()
            elif event.doNow == Dn.HURT_PLAYER:
                player.hurt()
                self.hurting_player = False
            elif event.doNow == Dn.TAKE_TREASURE:
                player.got_treasure = True
                self.sounds[Sounds.GET_ITEM].play()
                self.picking_treasure = False
            elif event.doNow == Dn.END_LOSE or event.doNow == Dn.END_WIN:
                event = pygame.event.Event(RESTART_GAME)
                pygame.event.post(event)
            elif event.doNow == Dn.SET_BUTTON_A:
                config.set('CONTROL_A', textZone.key_pressed)
                textZone.setNewText(TEXT_NEED_CONFIG_CONTROLS_B, do_on_end_text=Dn.SET_BUTTON_B, get_key=True)
                self.showText()
                background.freeze = False
            elif event.doNow == Dn.SET_BUTTON_B:
                config.set('CONTROL_B', textZone.key_pressed)
                textZone.setNewText(TEXT_NEED_CONFIG_CONTROLS_UP, do_on_end_text=Dn.SET_BUTTON_UP, get_key=True)
                self.showText()
                background.freeze = False
            elif event.doNow == Dn.SET_BUTTON_UP:
                config.set('CONTROL_UP', textZone.key_pressed)
                textZone.setNewText(TEXT_NEED_CONFIG_CONTROLS_DOWN, do_on_end_text=Dn.SET_BUTTON_DOWN, get_key=True)
                self.showText()
                background.freeze = False
            elif event.doNow == Dn.SET_BUTTON_DOWN:
                config.set('CONTROL_DOWN', textZone.key_pressed)
                textZone.setNewText(TEXT_NEED_CONFIG_CONTROLS_LEFT, do_on_end_text=Dn.SET_BUTTON_LEFT, get_key=True)
                self.showText()
                background.freeze = False
            elif event.doNow == Dn.SET_BUTTON_LEFT:
                config.set('CONTROL_LEFT', textZone.key_pressed)
                textZone.setNewText(TEXT_NEED_CONFIG_CONTROLS_RIGHT, do_on_end_text=Dn.SET_BUTTON_RIGHT, get_key=True)
                self.showText()
                background.freeze = False
            elif event.doNow == Dn.SET_BUTTON_RIGHT:
                config.set('CONTROL_RIGHT', textZone.key_pressed)
                event = pygame.event.Event(RESTART_GAME)
                pygame.event.post(event)
        elif event.type == TEXT_ZONE_ANSWER_YES:
            if event.doNow == Dn.SET_PLAYER_START_ROOM:
                player.setPlayerStartRoom()
                self.changeState(Gs.INITIALISATION)
        elif event.type == KEYUP or event.type == JOYBUTTONDOWN or event.type == JOYHATMOTION:
            # inputs
            for name, printable in self.printables.items():
                if not printable.freeze and printable.visible:
                    printable.handleInput(event)

        self.updateScreenPositionForVisiblePrintable()

    def update(self, frame):
        for name, printable in self.printables.items():
            if not printable.freeze and printable.visible:
                printable.update(frame)

        dungeon = self.getPrintable(Pn.DUNGEON)
        dragon = self.getPrintable(Pn.DRAGON)
        player = self.getPrintable(Pn.PLAYER)
        textZone = self.getPrintable(Pn.TEXT_ZONE)

        # Win
        if player.actual_room == player.start_room and player.got_treasure and self.state == Gs.PLAY and not self.ending:
            self.ending = True
            textZone.setNewText(TEXT_WIN, do_on_end_text=Dn.END_WIN)
            event = pygame.event.Event(TEXT_ZONE_SHOW)
            pygame.event.post(event)
            self.sounds[Sounds.WIN].play()

        # Game over
        if player.max_move < 5 and not self.ending:
            self.ending = True
            textZone.setNewText(TEXT_LOSE, do_on_end_text=Dn.END_LOSE)
            event = pygame.event.Event(TEXT_ZONE_SHOW)
            pygame.event.post(event)
        # Player Hurt
        elif player.actual_room == dragon.actual_room and player.actual_room is not None and not self.hurting_player:
            self.hurting_player = True
            dragon.last_strike_room = player.actual_room
            dragon.visible = True
            textZone.setNewText(TEXT_DRAGON_ATTACK, do_on_end_text=Dn.HURT_PLAYER)
            event = pygame.event.Event(TEXT_ZONE_SHOW)
            pygame.event.post(event)
            self.sounds[Sounds.HURT_PLAYER].play()

        if player.actual_room == dragon.start_room and not player.got_treasure and player.actual_room is not None and not self.picking_treasure:
            self.picking_treasure = True
            player.actual_room.color = COLOR_TREASURE_ROOM

            if not dungeon.treasure_discovered:
                dungeon.treasure_discovered = True
                self.sounds[Sounds.FOUND_TREASURE].play()
                textZone.setNewText(TEXT_TREASURE_FOUND, do_on_end_text=Dn.TAKE_TREASURE)
            else:
                textZone.setNewText(TEXT_TREASURE_TAKE, do_on_end_text=Dn.TAKE_TREASURE)

            if player.rest_of_move > 4:
                player.rest_of_move = 4

            event = pygame.event.Event(TEXT_ZONE_SHOW)
            pygame.event.post(event)

        if self.shuffle:
            self.shuffle_current_frame += 1

            if self.shuffle_current_offset > 40 or self.shuffle_current_offset < -40:
                self.shuffle_sign = self.shuffle_sign * -1

            self.offset_x += self.shuffle_sign
            self.offset_y += self.shuffle_sign

            self.shuffle_current_offset += self.shuffle_sign * 20

            if self.shuffle_current_frame > 60:
                self.shuffle_current_frame = 0
                self.shuffle = False
                self.offset_x = 0
                self.offset_y = 0
                self.shuffle_current_offset = 0
                event = pygame.event.Event(PLAYER_TURN_FINISHED)
                pygame.event.post(event)
                self.getPrintable(Pn.PLAYER).freeze = False

        self.updateScreenPositionForVisiblePrintable()

    def updateScreenPositionForVisiblePrintable(self):
        for name, printable in self.printables.items():
            if not printable.freeze and printable.visible:
                printable.updateScreenPosition()

    def getSurface(self):
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        for printable_name, printable in self.printables.items():
            if printable is not None and printable.visible:
                surface.blit(
                    printable.getSurface(),
                    (printable.position[0] + printable.offset[0],
                     printable.position[1] + printable.offset[1])
                )

                if printable_name == Pn.TITLE_SCREEN:
                    title_img = pygame.transform.scale(
                        self.title_img,
                        (self.title_img.get_width() * printable.zoom, self.title_img.get_height() * printable.zoom)
                    )
                    surface.blit(title_img, (10 * printable.zoom, 2 * printable.zoom))

        return surface
