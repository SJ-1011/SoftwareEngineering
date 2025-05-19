from single_play import Game
import pygame, random


class stage_C(Game):

    def __init__(self, screen, keys, config, soundFX):
        super().__init__(screen, keys, config, soundFX)

        print("STAGE C")
        # refactoring needed(after single_play refactoring - function seperation)
        # best: delete all variables below
        self.game_type = "stageC"