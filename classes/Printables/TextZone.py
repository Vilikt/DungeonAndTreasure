from pathlib import Path

import pygame
from pygame.locals import *
from constants import *
from classes.Printable import Printable
from constants import PrintableNames as Pn


class TextZone(Printable):
    def __init__(self, game, zoom=1, police=None, text='', question=False, start_position=None, end_position=None):
        self.assetsPath = Path(root / "assets")

        super().__init__(game, zoom, start_position, end_position)

        self.police = police
        if police is None:
            self.police = pygame.font.Font(self.assetsPath / "zeldadxt.ttf", TEXT_SIZE * self.zoom)

        self.text = text
        self.question = question
        self.width = (WINDOW_WIDTH / SPRITE_WIDTH) / self.zoom
        self.height = TEXT_ZONE_HEIGHT_SPRITE
        self.text_position_y = 2
        self.text_lines = []
        self.nbr_of_lines = 0
        self.current_text_line_index = 0
        self.current_text_col_index = 0
        self.current_text_line_offset = 0

        self.pause = False
        self.show_arrow = False
        self.show_select_cursor = False
        self.select_cursor_position = 1
        self.key_pressed = None

        self.splitText()

        self.do_on_end_text = None
        self.get_key = False

    def setNewText(self, text, question=False, do_on_end_text=None, get_key=False):
        self.reset()
        self.text = text
        self.question = question
        self.splitText()
        self.do_on_end_text = do_on_end_text
        self.get_key = get_key

    def show(self):
        self.setFreezeAll(True)
        self.visible = True

    def setFreezeAll(self, value):
        for name, printable in self.game.printables.items():
            if name is not Pn.TEXT_ZONE:
                printable.freeze = value

    def splitText(self):
        text_split = self.text.split()

        current_line = 0
        self.text_lines.insert(0, '')
        for word in text_split:
            if len(word) + len(self.text_lines[current_line] + ' ') > self.width:
                current_line += 1
                self.text_lines.insert(current_line, '')

            self.text_lines[current_line] += word + ' '

        if self.question:
            self.text_lines.append(' ')
            self.text_lines.append('     ' + TEXT_YES + '    ' + TEXT_NO + ' ')

        self.nbr_of_lines = len(self.text_lines)

    def update(self, frame):
        if self.pause:
            if not self.question:
                if frame in get_frequency_list(30):
                    self.show_arrow = True
                else:
                    self.show_arrow = False
            elif self.isEndOfText():
                if frame in get_frequency_list(30):
                    self.show_select_cursor = True
                else:
                    self.show_select_cursor = False
        elif frame in get_frequency_list(40):
            self.show_arrow = False

            if (self.current_text_line_index >= 3 and self.isEndOfTheCurrentLine()) or self.isEndOfText():
                self.game.sounds[Sounds.TEXT_DONE].play()
                self.pause = True

            if self.isEndOfTheCurrentLine():
                if self.current_text_line_index < self.nbr_of_lines - 1:
                    self.current_text_line_index += 1
                    self.current_text_col_index = 0
            else:
                if self.current_text_line_index > 3:
                    self.current_text_line_offset += 1

                if self.current_text_col_index < len(self.text_lines[self.current_text_line_index]):
                    self.current_text_col_index += 1
                    self.game.sounds[Sounds.LETTER].play()

        super().update(frame)

    def handleInputWhenGetKey(self):
        self.pause = False
        self.game.sounds[Sounds.SELECT].play()
        event_to_send = pygame.event.Event(TEXT_ZONE_DISMISS, doNow=self.do_on_end_text)
        pygame.event.post(event_to_send)
        self.reset()
        self.setFreezeAll(False)

    def handleInputWhenAControlPressed(self):
        if self.pause:
            self.pause = False

            if self.isEndOfText():
                if self.question:
                    if self.select_cursor_position == 1:
                        event = pygame.event.Event(TEXT_ZONE_ANSWER_YES, doNow=self.do_on_end_text)
                        self.game.sounds[Sounds.SELECT].play()
                    elif self.select_cursor_position == 0:
                        event = pygame.event.Event(TEXT_ZONE_ANSWER_NO, doNow=self.do_on_end_text)
                else:
                    event = pygame.event.Event(TEXT_ZONE_DISMISS, doNow=self.do_on_end_text)

                pygame.event.post(event)
                self.reset()
                self.setFreezeAll(False)

    """
    def handleInputJoy(self, event):
        if event.type == JOYBUTTONDOWN:
            if self.get_key:
                self.handleInputWhenGetKey()
                self.key_pressed = event.button
            elif event.button == CONTROL_A:
                self.handleInputWhenAControlPressed()
        elif event.type == JOYHATMOTION and event.value != (0, 0):
            if self.get_key:
                self.handleInputWhenGetKey()
                self.key_pressed = event.value
            elif event.value == CONTROL_RIGHT:
                if self.question and self.isEndOfText() and self.select_cursor_position == 1:
                    self.select_cursor_position = 0
                    self.game.sounds[Sounds.CURSOR].play()
            elif event.value == CONTROL_LEFT:
                if self.question and self.isEndOfText() and self.select_cursor_position == 0:
                    self.select_cursor_position = 1
                    self.game.sounds[Sounds.CURSOR].play()
    """

    def handleInput(self, event):
        if hasattr(event, 'key'):
            k = event.key
        elif hasattr(event, 'value'):
            k = event.value
        elif hasattr(event, 'button'):
            k = event.button

        if event.type == KEYUP or event.type == JOYBUTTONDOWN or event.type == JOYHATMOTION:
            if self.get_key and k != (0, 0):
                self.handleInputWhenGetKey()
                self.key_pressed = k
            elif k == CONTROL_A:
                self.handleInputWhenAControlPressed()
            elif k == CONTROL_RIGHT:
                if self.question and self.isEndOfText() and self.select_cursor_position == 1:
                    self.select_cursor_position = 0
                    self.game.sounds[Sounds.CURSOR].play()
            elif k == CONTROL_LEFT:
                if self.question and self.isEndOfText() and self.select_cursor_position == 0:
                    self.select_cursor_position = 1
                    self.game.sounds[Sounds.CURSOR].play()

    def reset(self):
        self.current_text_line_offset = 0
        self.current_text_line_index = 0
        self.current_text_col_index = 0
        self.text_lines = []
        self.visible = False
        self.pause = False
        self.show_arrow = False
        self.show_select_cursor = False
        self.select_cursor_position = 1

    def isEndOfTheCurrentLine(self):
        return self.current_text_col_index == len(self.text_lines[self.current_text_line_index]) - 1

    def isEndOfText(self):
        return self.isEndOfTheCurrentLine() and self.current_text_line_index == len(self.text_lines) - 1

    def getSurface(self):
        self.surface = pygame.Surface((SPRITE_WIDTH * self.width, SPRITE_HEIGHT * self.height))
        self.surface.fill(COLOR_BLACK)

        if self.show_arrow:
            self.surface.blit(
                self.game.getSpriteById(515),
                (SPRITE_WIDTH * self.width - SPRITE_WIDTH, (SPRITE_HEIGHT - 2) * self.height)
            )
        if self.show_select_cursor:
            if self.select_cursor_position == 1:
                self.surface.blit(self.game.getSpriteById(517), (SPRITE_WIDTH * 4, SPRITE_HEIGHT * 2))
            elif self.select_cursor_position == 0:
                self.surface.blit(self.game.getSpriteById(517), (SPRITE_WIDTH * 11, SPRITE_HEIGHT * 2))

        # text
        self.text_position_y = 0
        for line in range(0, self.current_text_line_index):
            text_surf = self.police.render(self.text_lines[line], False, COLOR_TEXT)
            self.surface.blit(text_surf, (6, self.text_position_y - self.current_text_line_offset))
            self.text_position_y += SPRITE_HEIGHT

        for col in range(0, self.current_text_col_index):
            text_surf = self.police.render(
                self.text_lines[self.current_text_line_index][0: self.current_text_col_index], False, COLOR_TEXT)
            self.surface.blit(text_surf, (6, self.text_position_y - self.current_text_line_offset))

        return super().getSurface()

    def updateScreenPosition(self):
        self.setScreenPosition([0, (WINDOW_HEIGHT - TEXT_ZONE_HEIGHT_SPRITE * SPRITE_HEIGHT * self.zoom)])

