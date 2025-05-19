from single_play import Game


class stage_D(Game):
    def __init__(self, screen, keys, config, soundFX):
        super().__init__(screen, keys, config, soundFX)

        print("STAGE D")
        # refactoring needed(after single_play refactoring - function seperation)
        # best: delete all variables below
        self.game_type = "stageD"