import itertools, random
from single_play import Game
from models.card import Card
from models.button import Button
from models.Human import Human
from models.AI import AI


class stage_A(Game):
    def __init__(self, screen, keys, config, soundFX):
        super().__init__(screen, keys, config, soundFX)

        print("STAGE A")
        # refactoring needed(after single_play refactoring - function seperation)
        # best: delete all variables below
        self.game_type = "stageA"

