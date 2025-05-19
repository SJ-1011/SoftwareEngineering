from models.AI import AI
from utils.stageB import stage_B


class AI_B(AI, stage_B):
    def __init__(self, number, hand, turn):
        super().__init__(number, hand, turn)
        self.type = "AI_B"
        self.stage = "B"
