import pygame
from models.card import Card
from models.Human import Human
from models.AI import AI
from models.button import Button, Component
from single_play import Game

import itertools
import random
import sys

from pause import PauseClass
import time

# 3명의 컴퓨터 플레이어와 대전 / 첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게 분배.


class stage_B(Game):
    def __init__(self, screen, keys, config, soundFX):
        super().__init__(screen, keys, config, soundFX)

        print("STAGE B")
        # refactoring needed(after single_play refactoring - function seperation)
        # best: delete all variables below
        self.game_type = "stageB"
