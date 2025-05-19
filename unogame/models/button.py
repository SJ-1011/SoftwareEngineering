import pygame
from .player import Player
from models.AI import AI


class Button:
    def __init__(self, x, y, width, height, color, text, text_color, font_size, alpha):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", font_size)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alpha = alpha
        self.surface.fill(color)
        self.surface.set_alpha(self.alpha)
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2 + 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Component:

    now_component = None
    WHITE = (255, 255, 255)
    GRAY = (64, 64, 64)
    def __init__(
        self, x, y, width, height, color, player_name, text_color, font_size, player
    ):
        white = Component.WHITE
        gray = Component.GRAY
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = player_name
        self.text_color = text_color
        self.font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", font_size)
        self.player = player
        self.is_block = False
        self.is_choose = False
        self.is_empty = True
        self.is_edit = False
        self.surf = pygame.image.load(
            "resources/images/card/normalMode/backcard.png"
        ).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (15, 20))
        self.close_button = Button(x+width-20,y,20,20,white,"X",gray,20,0)

        self.a_button = Button(x,y,width/2,height/2,white,"A",gray,20,0)
        self.b_button = Button(x+(width/2),y,width/2,height/2,white,"B",gray,20,0)
        self.c_button = Button(x,y+(height/2),width/3,height/2,white,"C",gray,20,0)
        self.d_button = Button(x+(width/3),y+(height/2),width/3,height/2,white,"D",gray,20,0)
        self.normal_button = Button(x+(width/3*2),y+(height/2),width/3,height/2,white,"normal",gray,15,0)

    def draw(self, screen, game_active, game_type):
        # game_type = ["single", "story"] / 추가할 수도 있음
        white = Component.WHITE
        gray = Component.GRAY
        if not self.is_empty and self.player is not None:
            if self.is_edit:
                pass
            elif self.player.type == "Human":
                self.text = f"PLAYER {self.player.number + 1} ({self.player.type})"
                if game_type[0:5] == "stage":
                    self.text = "ME"
            elif self.player.type == "AI":
                self.text = f"PLAYER {self.player.number + 1} ({self.player.type})"
                if self.player.stage == "NORMAL":
                    self.text = f"PLAYER {self.player.number + 1} ({self.player.type})"
                else:
                    self.text = f"PLAYER {self.player.number + 1} ({self.player.type}_{self.player.stage})"

            self.color = white
            self.text_color = gray
        elif self.is_choose:
            self.color = white
        else:
            self.text = "EMPTY"
            self.color = gray
            self.text_color = white

        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_x = self.rect.x + 5
        text_y = self.rect.y + 5

        if self.player is not None and game_active:
            for i in range(len(self.player.hand)):
                rect = self.surf.get_rect(
                    midleft=(self.rect.x + 5 + 10 * (i % 14), self.rect.y + 30 + 8 * (i//14))
                )
                screen.blit(self.surf, rect)

            text_surface = self.font.render(
                self.text + f" : {len(self.player.hand)}",
                False,
                self.text_color,
            )
            
        if self.is_choose and not game_active:
            self.a_button.draw(screen)
            self.b_button.draw(screen)
            self.c_button.draw(screen)
            self.d_button.draw(screen)
            self.normal_button.draw(screen)
        elif not self.is_empty and not game_active:
            self.close_button.draw(screen)
        if not self.is_choose:
            screen.blit(text_surface, (text_x, text_y))
        if self.is_block:
            pygame.draw.line(screen, (255, 0, 0), self.rect.topleft, self.rect.bottomright, 5)
            pygame.draw.line(screen, (255, 0, 0), self.rect.bottomleft, self.rect.topright, 5)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def ban_player(self):
        self.is_empty = True
        self.player = None

    def change_clicked(self, pos):
        if self.a_button.is_clicked(pos) or self.b_button.is_clicked(pos) or self.c_button.is_clicked(pos) or self.d_button.is_clicked(pos) or self.normal_button.is_clicked(pos):
            return True
        else:
            return False
    def choose_AI_type(self, pos, index):
        if self.a_button.is_clicked(pos):
            self.player = AI(index, [], index)
            self.player.stage = "A"
            return "A"
        elif self.b_button.is_clicked(pos):
            self.player = AI(index, [], index)
            self.player.stage = "B"
            return "B"
        elif self.c_button.is_clicked(pos):
            self.player = AI(index, [], index)
            self.player.stage = "C"
            return "C"
        elif self.d_button.is_clicked(pos):
            self.player = AI(index, [], index)
            self.player.stage = "D"
            return "D"
        elif self.normal_button.is_clicked(pos):
            self.player = AI(index, [], index)
            self.player.stage = "NORMAL"
            return "normal"
