from models.AI import AI
from utils.stageA import stage_A


class AI_A(AI, stage_A):
    def __init__(self, number, hand, turn):
        super().__init__(number, hand, turn)
        self.type = "AI_A"
        self.stage = "A"
