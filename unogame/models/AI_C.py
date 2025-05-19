from models.AI import AI
from utils.stageC import stage_C


class AI_C(AI, stage_C):
    def __init__(self, number, hand, turn):
        super().__init__(number, hand, turn)
        self.type = "AI_C"
        self.stage = "C"
