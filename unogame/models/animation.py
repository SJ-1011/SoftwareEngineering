import pygame

animation_count = 1
class Animation:

    def __init__(self, start, end, start_time, count):
        global animation_count
        self.timer = pygame.USEREVENT + 100 + animation_count
        animation_count += 1
        self.start = start
        self.end = end
        self.start_time = start_time
        self.count = count
        self.move_list = [MoveRect() for _ in range(count)]

    def card_move(self, move_rect, current_time, duration):
        elapsed_time = current_time - self.start_time
        progress = min(1, elapsed_time / duration)
        eased_progress = (progress - 1) ** 3 + 1
        move_rect.rect.centerx = self.start[0] + (self.end[0] - self.start[0]) * eased_progress
        move_rect.rect.centery = self.start[1] + (self.end[1] - self.start[1]) * eased_progress


class AnimationWin(Animation):

    def __init__(self, start, end, start_time, count, card):
        super().__init__(start, end, start_time, count)
        self.card = card
        self.move_list.clear()
        move_object = MoveRect()
        move_object.surf = self.card.image
        move_object.rect = self.card.rect
        self.move_list.append(move_object)
class MoveRect:

    def __init__(self):
        move_surf = pygame.image.load(
            "resources/images/card/normalMode/backcard.png"
        ).convert_alpha()
        move_surf = pygame.transform.scale(move_surf, (50, 70))
        move_rect = move_surf.get_rect(center=(-200, -200))
        self.rect = move_rect
        self.surf = move_surf

        # for i in range(0, 2):
        #     self.card_move(
        #         self.deck_rect.center,
        #         self.info_list[self.turn_index].rect.center,
        #         c_time + 100 * i,
        #         self.moving_start_time,
        #         2000,
        #         i
        #     )