from models.player import Player


class Human(Player):
    def __init__(self, number, hand, turn):
        super().__init__(number, hand, turn)
        self.type = "Human"
        self.stage = "Human"
    def update_hand(self, screen):
        if len(self.hand) <= 10:
            for i, card in enumerate(self.hand):
                card.rect = card.large_image_surface.get_rect(center=(-300, -300))
                card.rect.x = 20 + (card.width + 5) * i
                card.rect.y = screen.get_height() - 120
                card.initial_y = card.rect.y
        elif 10 < len(self.hand) <= 20:
            for i, card in enumerate(self.hand):
                card.rect = card.large_image_surface.get_rect(center=(-300, -300))
                if i <= 9:
                    card.rect.x = 20 + (card.width + 5) * i
                    card.rect.y = screen.get_height() - 200
                    card.initial_y = card.rect.y
                elif 10 <= i < 20:
                    card.rect.x = 20 + (card.width + 5) * (i - 10)
                    card.rect.y = screen.get_height() - 120
                    card.initial_y = card.rect.y

        elif 20 < len(self.hand) <= 35:
            for i, card in enumerate(self.hand):
                card.rect = card.small_image_surface.get_rect(center=(-300, -300))
                if i <= 9:
                    card.rect.x = 20 + (card.width // 2 + 5) * i
                    card.rect.y = screen.get_height() - 200
                    card.initial_y = card.rect.y

                elif 10 <= i < 20:
                    card.rect.x = 20 + (card.width // 2 + 5) * (i - 10)
                    card.rect.y = screen.get_height() - 160
                    card.initial_y = card.rect.y

                elif 20 <= i < 35:
                    card.rect.x = 20 + (card.width // 2 + 5) * (i - 20)
                    card.rect.y = screen.get_height() - 120
                    card.initial_y = card.rect.y
                else:
                    pass

    def draw_hand(self, screen):
        for card in self.hand:
            if len(self.hand) > 20:
                screen.blit(card.small_image_surface, card.rect)
            else:
                screen.blit(card.large_image_surface, card.rect)
