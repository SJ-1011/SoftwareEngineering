from models.player import Player


class AI(Player):
    def __init__(self, number, hand, turn):
        super().__init__(number, hand, turn)
        self.type = "AI"
        self.stage = "NORMAL"