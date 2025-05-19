from models.AI import AI
from utils.stageD import stage_D


class AI_D(AI, stage_D):
    def __init__(self, number, hand, turn):
        super().__init__(number, hand, turn)
        self.type = "AI_D"
        self.stage = "D"
