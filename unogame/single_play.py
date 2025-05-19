import itertools
import random
import sys

import pygame

from models.button import Button, Component
from models.card import Card
from models.Human import Human
from models.AI import AI

from models.button import Button, Component
from pause import PauseClass
import time
from models.animation import Animation, AnimationWin
from models.event import *

from utils.achievement import achievement


class Game:
    pygame.font.init()
    font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", 36)
    clock = pygame.time.Clock()

    def __init__(self, screen, keys, config, soundFX):
        # lms
        self.achieve = achievement(config)
        # lms

        self.start_count = 1

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.player_number = 1

        self.soundFX = soundFX
        self.screen = screen

        self.who = None
        self.keys = keys
        self.config = config
        self.event_active = True

        self.game_active = False  # start를 누른 이후 게임 진행 중이면 True
        self.is_win = False
        self.is_get = False  # 자기 턴에 카드 뽑음
        self.run = True
        self.is_color_change = False
        self.is_AI_B = False
        self.is_AI_C = False
        self.edit_name = False
        self.edit_text = "__________"
        self.turn_counter = 0
        self.game_type = "single"
        # for achievement
        self.turnCount = 1
        self.numNeverUsed = True
        self.skillNeverUsed = True
        self.otherUno = False
        self.luckyThree = 0

        # color change하는 중 배경
        self.alpha_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.alpha_surface.fill(
            (0, 0, 0, 128)
        )  # (0,0,0,128) -> (0,0,0)으로 (불필요한 값. 작동 안될 수 있음)
        self.alpha_surface.set_alpha(128)

        self.turn_list = []  # 차례의 순서를 나타내는 list
        self.turn_index = 0  # 누구의 차례인지 알려주는 변수

        self.me = None
        self.deck = []  # 가운데에서 뽑힐 카드
        self.remain = []  # 낸 카드들

        self.deck_surf = pygame.image.load(
            "resources/images/card/normalMode/backcart.png"
        ).convert_alpha()
        self.deck_rect = self.deck_surf.get_rect(
            center=(self.screen_width / 3, self.screen_height / 3)
        )

        # self.now_card = Card("red", None, 0, False, self.config)
        self.now_card = None
        self.now_card_surf = pygame.image.load(
            "resources/images/card/normalMode/backcart.png"
        ).convert_alpha()
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 30, self.screen_height / 3)
        )

        self.win_list = []

        self.uno_button = Button(
            self.screen_width / 3 + 240,
            self.screen_height / 3,
            50,
            30,
            (255, 255, 255),
            "UNO",
            (64, 64, 64),
            30,
            255,
        )
        self.retry_surf = Game.font.render(
            "click to return to main", False, (64, 64, 64)
        )
        self.retry_rect = self.retry_surf.get_rect(
            center=(self.screen_width / 2, 70)
        )

        self.start_button = Button(
            self.screen_width // 2 - 100,
            self.screen_height // 2 - 30,
            100,
            60,
            (255, 255, 255),
            "START",
            (64, 64, 64),
            40,
            255,
        )

        self.backImage = pygame.image.load('./resources/images/play/play.png')
        self.backImage2 = pygame.image.load('./resources/images/play/play2.png')
        self.backImage3 = pygame.image.load('./resources/images/play/before.png')
        self.player_list = []
        for i in range(0,6):
            button = Button(
            self.screen_width // 8,
            self.screen_height/5 + 90 * i,
            100,
            60,
            (255, 0, 0),
            f"player {i + 1}",
            (255, 255, 255),
            28,
            0,
        )
            self.player_list.append(button)

        # 로비를 생성하는데 필요한 변수
        self.lobby_background = pygame.Rect(
            self.screen_width - 150, 0, 150, self.screen_height
        )

        self.now_button = Button(
            self.screen_width // 2 + 60,
            self.screen_height // 5 - 50,
            40,
            40,
            (255, 255, 255),
            "now",
            (0, 0, 0),
            15,
            255,
        )

        self.ok_button = Button(
            self.screen_width // 2,
            self.screen_height // 2 + 100,
            50,
            40,
            (255, 255, 255),
            "ok",
            (64, 64, 64),
            40,
            255,
        )
        self.now_turn_button = Button(
            self.screen_width // 8,
            self.screen_height // 2 - 30,
            40,
            30,
            (255, 255, 255),
            "",
            (255, 255, 255),
            35,
            0,
        )

        self.skill_active_button = Button(
            self.screen_width // 8 + 50,
            self.screen_height // 8,
            40,
            30,
            (255, 255, 255),
            "reverse skill active yellow > green",
            (255, 255, 255),
            35,
            0,
        )

        self.uno_active_button = Button(
            self.screen_width / 3 + 240,
            self.screen_height / 3 + 30,
            50,
            30,
            (255, 255, 255),
            "Uno!",
            (255, 255, 255),
            35,
            0,
        )
        self.info_list = []
        self.info_list.append(
            Component(
                self.lobby_background.x,
                self.lobby_background.y,
                150,
                90,
                (255, 255, 255),
                f"PLAYER 1(ME)",
                (64, 64, 64),
                20,
                None,
            )
        )
        self.info_list[0].is_empty = False
        self.info_list[0].player= Human(0, [], 0)
        for i in range(1, 6):
            self.info_list.append(
                Component(
                    self.lobby_background.x,
                    self.lobby_background.y + 100 * i,
                    150,
                    90,
                    (64, 64, 64),
                    f"EMPTY",
                    (220, 220, 220),
                    20,
                    None,
                )
            )

        self.animation_list = []
        self.animation_list_2 = []
        self.card_list = []
        self.change_color_list = []
        self.CENTER_X_POS = self.screen_width // 10
        self.CENTER_Y_POS = self.screen_height // 5
        for color, pos, color_string in zip(
            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
            [
                (self.CENTER_X_POS - 25, self.CENTER_Y_POS - 25),
                (self.CENTER_X_POS + 25, self.CENTER_Y_POS - 25),
                (self.CENTER_X_POS - 25, self.CENTER_Y_POS + 25),
                (self.CENTER_X_POS + 25, self.CENTER_Y_POS + 25),
            ],
            ["red", "green", "blue", "yellow"],
        ):
            surf = pygame.Surface((50, 50))
            surf.fill(color_string)
            rect = surf.get_rect(center=pos)
            self.change_color_list.append([surf, rect, color, color_string])

        # 지금 선택한 카드를 나타내는 변수
        self.now_select = None

        # Timer 변수 세팅
        self.turn_timer = pygame.USEREVENT + 1
        self.current_time = 10
        pygame.time.set_timer(self.turn_timer, 1000)

        self.time_button = Button(
            self.screen_width // 8 + 40,
            self.screen_height // 2 + 15,
            80,
            30,
            (255, 255, 255),
            f"TIME : {self.current_time}",
            (64, 64, 64),
            30,
            255,
        )

        self.win_button = Button(
            self.screen_width / 2 - 50,
            20,
            100,
            40,
            (255, 255, 255),
            "Player 1 win !!",
            (255, 255, 255),
            30,
            0,
        )

        self.uno_timer = pygame.USEREVENT + 2
        self.uno_active_timer = pygame.USEREVENT + 3
        self.is_uno = False
        self.uno_pressed = False

        self.skill_active_timer = pygame.USEREVENT + 4
        self.is_skill_active = False

        self.block_timer = pygame.USEREVENT + 5

        self.AI_timer = pygame.USEREVENT + 6
        self.is_computer_turn = False
        self.AI_timer_on = False

        self.event = Event(self)

        self.isMulti = False
        self.settingPassword = True
        self.password = ""

    def start_single_play(self):
        pygame.init()
        #screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        while self.run:

            # backImage_num = self.config['window']['default']
            # if backImage_num == '1':
            #     new_backImage = pygame.transform.scale(self.backImage, (800, 600))
            # elif backImage_num == '2':
            #     new_backImage = pygame.transform.scale(self.backImage, (1000, 750))
            # elif backImage_num == '3':
            #     new_backImage = pygame.transform.scale(self.backImage, (1280, 960))
            # self.screen.blit(new_backImage, (0, 0))
            # self.screen.fill((57, 157, 220))
            self.screen.blit(self.backImage2, (0, 0))
            
            # hy - only execute after pausing
            self.make_screen()
            # event loop

            if self.game_active:
                self.time_button.text = f"TIME : {self.current_time}"
                self.time_button.draw(self.screen)

            for event in pygame.event.get():
                #print(event)
                if self.event.event_loop(event, self) == "out":
                    return
                if(not self.event_active):
                    pygame.event.clear()
                    break
            # event loop 종료

            self.next_screen(self.screen)
            pygame.display.update()

            # Limit the frame rate
            Game.clock.tick(60)

    def make_screen(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.deck_rect.centerx = self.screen_width / 3
        self.deck_rect.centery = self.screen_height / 3

        # self.uno_button.rect.x = self.deck_rect.centerx + 150
        # self.uno_button.rect.y = self.deck_rect.centery + 30

        self.uno_active_button.rect.x = self.deck_rect.centerx + 150
        self.uno_active_button.rect.y = self.deck_rect.centery + 70

        self.retry_rect.centerx = self.screen_width / 2
        self.retry_rect.centery = 70

        # self.start_button.rect.x = self.screen_width // 2 - 100
        # self.start_button.rect.y = self.screen_height // 2 - 30

        self.lobby_background.x = self.screen_width - 150
        self.lobby_background.y = 0
        self.lobby_background.height = self.screen_height

        self.now_button.rect.x = self.deck_rect.centerx + 150
        self.now_button.rect.y = self.deck_rect.centery - 50

        self.skill_active_button.rect.x = self.screen_width // 8 + 50
        self.skill_active_button.rect.y = 30
        self.ok_button.rect.x = self.screen_width // 2
        self.ok_button.rect.y = self.screen_height // 2 + 100

        self.win_button.rect.center = (
            self.screen_width / 2,
            40,
        )
        self.now_turn_button.center = (
            self.screen_width // 8,
            self.screen_height // 2 - 30,
        )
        self.time_button.center = (
            self.screen_width // 8 + 40,
            self.screen_height // 2 + 15,
        )

        self.now_card_rect.centerx = self.deck_rect.centerx + 80
        self.now_card_rect.centery = self.deck_rect.centery

        self.alpha_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.alpha_surface.fill(
            (0, 0, 0, 128)
        )  # (0,0,0,128) -> (0,0,0)으로 (불필요한 값. 작동 안될 수 있음)
        self.alpha_surface.set_alpha(128)

        self.change_color_list = []
        self.CENTER_X_POS = self.screen_width // 10
        self.CENTER_Y_POS = self.screen_height // 5
        for color, pos, color_string in zip(
            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
            [
                (self.CENTER_X_POS - 32, self.CENTER_Y_POS - 32),
                (self.CENTER_X_POS + 32, self.CENTER_Y_POS - 32),
                (self.CENTER_X_POS - 32, self.CENTER_Y_POS + 32),
                (self.CENTER_X_POS + 32, self.CENTER_Y_POS + 32),
            ],
            ["red", "green", "blue", "yellow"],
        ):
            surf = Game.font.render(color_string, False, (64, 64, 64))
            rect = surf.get_rect(center=pos)
            self.change_color_list.append([surf, rect, color, color_string])

        for i, component in enumerate(self.info_list):
            component.rect.x = self.lobby_background.x
            component.rect.y = self.lobby_background.y + 100 * i

        if self.me is not None:
            self.me.update_hand(self.screen)
        for i in range(0, self.player_number):
            self.player_list[i].rect.center = (self.screen_width // 8, self.screen_height // 4 + 100 * i)
    def next_screen(self, screen):
        if self.game_active:
            # 누구의 턴인지 보여주는 부분
            if self.turn_list[self.turn_index] == self.me:
                self.now_turn_button.text = f"my turn"
            else:
                self.now_turn_button.text = (
                    f"PLAYER {self.turn_list[self.turn_index].number + 1}'s turn"
                )
            self.now_turn_button.draw(screen)

            c_time = pygame.time.get_ticks()
            for ani in self.animation_list:
                for count in range(ani.count):
                    ani.card_move(ani.move_list[count], c_time + (100 * count), 2000)
                    screen.blit(ani.move_list[count].surf, ani.move_list[count].rect)

            if len(self.deck):
                screen.blit(self.deck_surf, self.deck_rect)
            screen.blit(self.now_card_surf, self.now_card_rect)

            # 손패를 그려주는 부분
            self.me.draw_hand(screen)

            if self.is_color_change:
                screen.blit(self.alpha_surface, (0, 0))
                for color_list in self.change_color_list:
                    screen.blit(color_list[0], color_list[1])
                    temp_rect = pygame.Rect(
                        color_list[1].x - 1,
                        color_list[1].y - 1,
                        color_list[1].width + 2,
                        color_list[1].height + 2,
                    )
                    pygame.draw.rect(screen, (0, 0, 0), temp_rect, 3)

            self.uno_button.draw(screen)
            if (
                self.now_select and self.me.turn == self.turn_index
            ) or self.now_select == self.uno_button:
                pygame.draw.rect(screen, (255, 255, 255), self.now_select, 3)
                
            pygame.draw.rect(screen, (16, 24, 30), self.lobby_background)
            for i in range(0, self.player_number):
                self.info_list[i].draw(screen, self.game_active, self.game_type)

            if self.now_card.color is not None:
                pixel = self.now_card_surf.get_at(
                    (
                        self.now_card_surf.get_width() // 2,
                        self.now_card_surf.get_height() - 1,
                    )
                )

                self.now_button.surface.fill(pixel)
            else:
                self.now_button.surface.fill((80, 80, 80))

            self.now_button.draw(screen)

            if self.is_skill_active:
                self.skill_active_button.draw(screen)

            if self.uno_pressed:
                self.uno_active_button.draw(screen)

        else:
            screen.blit(self.backImage3, (0, 0))
            # # 게임이 종료되었을 때 덱 초기화
            # for player in self.turn_list:
            #     player.hand.clear()
            # self.deck.clear()
            # self.remain.clear()

            if self.is_win:
                # hy
                self.win_button.draw(screen)
                screen.blit(self.retry_surf, self.retry_rect)

                for i in range(0, self.player_number):
                    self.player_list[i].text = self.info_list[i].text
                    if self.info_list[i].player == self.me:
                        self.player_list[i].text = "YOU"
                    self.player_list[i].draw(self.screen)
                if not len(self.animation_list_2):
                    for j in range(0, self.player_number):
                        for i in range(0, len(self.info_list[j].player.hand)):
                            self.animation_list_2.append(AnimationWin(
                                (self.player_list[j].rect.midright[0] + 120, self.player_list[j].rect.midright[1]),
                                (self.player_list[j].rect.midright[0] + 120 + 30 * i,
                                 self.player_list[j].rect.midright[1]),
                                pygame.time.get_ticks(),
                                1,
                                self.info_list[j].player.hand[i]
                            ))

                c_time = pygame.time.get_ticks()
                for ani in self.animation_list_2:
                    for count in range(ani.count):
                        ani.card_move(ani.move_list[count], c_time + (100 * count), 2000)
                        screen.blit(ani.move_list[count].surf, ani.move_list[count].rect)
            else:
                self.start_button.draw(screen)
                # hy - seperate lobby
                pygame.draw.rect(screen, (16, 24, 30), self.lobby_background)
                for i in range(0, len(self.info_list)):
                    self.info_list[i].draw(screen, self.game_active, self.game_type)

            if self.edit_name:
                screen.blit(self.alpha_surface, (0, 0))
                rect = pygame.Rect(
                    self.screen_width // 2 - 150, self.screen_height // 2 - 50, 300, 180
                )
                pygame.draw.rect(screen, (255, 255, 255), rect)
                name_surf = Game.font.render(
                    "Enter Name(maximum 8)", False, (64, 64, 64)
                )
                name_rect = name_surf.get_rect(
                    center=(self.screen_width // 2, self.screen_height // 2 - 20)
                )
                input_surf = Game.font.render(self.edit_text, False, (64, 64, 64))
                input_rect = input_surf.get_rect(
                    center=(self.screen_width // 2, self.screen_height // 2 + 50)
                )
                self.ok_button.rect.center = (
                    self.screen_width // 2,
                    self.screen_height // 2 + 100,
                )
                screen.blit(name_surf, name_rect)
                screen.blit(input_surf, input_rect)
                self.ok_button.draw(screen)

            pygame.display.update()
        self.achieve.update(screen)  # achievement
    
    def drawLobby(self, screen):
        pygame.draw.rect(screen, (16, 24, 30), self.lobby_background)
        for i in range(0, len(self.info_list)):
            self.info_list[i].draw(screen, self.game_active, self.game_type)
        
        if self.isMulti and self.settingPassword:
            screen.blit(self.alpha_surface, (0, 0))
            back_rect = pygame.Rect(
                self.screen_width // 2 - 325, self.screen_height - 200, 500, 200
            )
            pygame.draw.rect(screen, (255, 255, 255), back_rect)
            phrase_surf = Game.font.render(
                "Enter Password(maximum 4)", False, (64, 64, 64)
            )
            phrase_rect = phrase_surf.get_rect(
                center=(back_rect.centerx, back_rect.centery - 50)
            )
            input_surf = Game.font.render(self.edit_text, False, (64, 64, 64))
            input_rect = input_surf.get_rect(
                center=(back_rect.centerx, back_rect.centery)
            )
            self.ok_button.rect.center = (
                back_rect.centerx, back_rect.centery + 50
            )
            screen.blit(phrase_surf, phrase_rect)
            screen.blit(input_surf, input_rect)
            self.ok_button.draw(screen)

        if self.edit_name:
            screen.blit(self.alpha_surface, (0, 0))
            rect = pygame.Rect(
                self.screen_width // 2 - 150, self.screen_height // 2 - 50, 300, 180
            )
            pygame.draw.rect(screen, (255, 255, 255), rect)
            name_surf = Game.font.render(
                "Enter Name(maximum 8)", False, (64, 64, 64)
            )
            name_rect = name_surf.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 - 20)
            )
            input_surf = Game.font.render(self.edit_text, False, (64, 64, 64))
            input_rect = input_surf.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + 50)
            )
            self.ok_button.rect.center = (
                self.screen_width // 2,
                self.screen_height // 2 + 100,
            )
            screen.blit(name_surf, name_rect)
            screen.blit(input_surf, input_rect)
            self.ok_button.draw(screen)

    def computer_turn(self):
        self.com_card = []

        for card in self.turn_list[self.turn_index].hand:
            if self.check_condition(card):
                self.com_card.append(card)
        if len(self.com_card) == 0:
            self.draw_from_center(self.turn_list[self.turn_index].hand)

            self.animation_list.append(Animation(
                self.deck_rect.center,
                self.info_list[self.turn_index].rect.center,
                pygame.time.get_ticks(),
                1
            ))
            self.soundFX.soundPlay(4)

            pygame.time.set_timer(self.animation_list[-1].timer, 2000)

            self.pass_turn()
        else:
            self.now_card = self.com_card[0]
            self.now_card_surf = self.now_card.image
            self.turn_list[self.turn_index].hand.remove(self.now_card)
            if (self.turn_list[self.turn_index].stage == "A"
                and len(self.turn_list[self.turn_index].hand)
                and self.now_card.skill is not None):
                self.remain.append(self.turn_list[self.turn_index].hand.pop())
            self.remain.append(self.now_card)
            self.animation_list.append(Animation(
                self.info_list[self.turn_index].rect.center,
                self.now_card_rect.center,
                pygame.time.get_ticks(),
                1
            ))
            pygame.time.set_timer(self.animation_list[-1].timer, 2000)
            self.soundFX.soundPlay(4)

            if self.now_card.skill is not None:
                self.skill_active(self.com_card[0])
            if self.now_card.skill not in [
                # "change",
                "block",
                # "all",
            ]:
                self.pass_turn()

    def deck_none(self):
        if len(self.deck) == 0 :
            print("덱이 없어서 계산을 합니다")
            win_condition = True
            ## test
            for hand in self.turn_list[self.turn_index].hand:
                if self.check_condition(hand):
                    win_condition = False
                    print("AI available")
                    break
            if win_condition or self.is_win:
                less_point = self.calculation_point(self.me.hand)
                for player in self.turn_list:
                    if less_point >= self.calculation_point(player.hand):
                        less_point = self.calculation_point(player.hand)
                        # self.win_button.text = f"Player {player.number + 1} win !!"
                    self.who = player
                # lms
                if self.who.type == "Human":
                    self.win_button.text = f"You win !!"
                    self.checkAchieve()  # achievement
                else:
                    self.win_button.text = f"You Loose. . ."
                # lms

                self.game_active = False
                self.is_win = True

                self.pause_event_handling()

    def block_turn(self):
        self.turn_index = (self.turn_index + 1) % len(self.turn_list)
        self.current_time = 10
        self.pass_turn()

    def reverse_turn(self):
        temp_player = self.turn_list[self.turn_index]
        self.info_list.reverse()
        self.turn_list.reverse()
        for player in self.turn_list:
            player.turn = self.turn_list.index(player)
        for component in self.info_list:
            if component.player == self.me:
                if self.edit_text == "__________":
                    component.text = "PLAYER 1(ME)"
                else:
                    component.text = self.edit_text
                print(f"text : {self.edit_text}")
        self.turn_index = self.turn_list.index(temp_player)

        ## lms
        for player in self.turn_list:
            if player.type == "Human":
                self.me = player


    def draw_card(self, input_deck):
        #if len(input_deck) == 0 and input_deck == self.deck:
        #    return
        if len(self.deck) != 0:
            pop_card = self.deck.pop()
            input_deck.append(pop_card)
        else:
            canRefill = self.refillCard()
            if canRefill:
                pop_card = self.deck.pop()
                input_deck.append(pop_card)
            else:
                print("Lack of Remain - plus")
        if len(self.me.hand) >= 15 and self.config["Achievement"]["grabover15card"] == "0":   # achievement
            self.achieve.accomplish(10)  


    def plus(self, input_deck, count):  # deck : list / first, second : card
        for _ in range(count):
            if len(self.deck) != 0:
                pop_card = self.deck.pop()
                input_deck.append(pop_card)
            else:
                canRefill = self.refillCard()
                if canRefill:
                    pop_card = self.deck.pop()
                    input_deck.append(pop_card)
                else:
                    print("Lack of Remain - plus")

        if len(self.me.hand) >= 15 and self.config["Achievement"]["grabover15card"] == "0":   # achievement
            self.achieve.accomplish(10)

    def generate_deck(self):
        for color, number in itertools.product(Card.colors, Card.numbers):
            temp_card = Card(color, number, None, False, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

            if number != 0:
                temp_card = Card(color, number, None, False, self.config)
                self.deck.append(temp_card)
                self.card_list.append(temp_card)
        # 색깔별로 기술 카드를 담음
        for color, skill in itertools.product(Card.colors, Card.skills):
            for _ in range(2):
                temp_card = Card(color, None, skill, False, self.config)
                self.deck.append(temp_card)
                self.card_list.append(temp_card)

        # all, all4 카드 추가
        for _ in range(4):
            temp_card = Card(None, None, "all", True, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

            temp_card = Card(None, None, "all4", True, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

        random.shuffle(self.deck)
        pop_card = self.deck.pop()

        # self.remain.append(pop_card)  # 낸 카드 리스트에 pop_card 추가(바닥에 있는 카드)
        self.turn_index = 0
        self.now_card = pop_card  # pop_card(바닥에 있는 카드)가 현재 카드임
        self.now_card_surf = pop_card.image  # 현재 카드 객체화
        self.remain.append(pop_card)
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )
        empty_list = []
        for i in range(0,len(self.info_list)):
            if self.info_list[i].is_empty:
                empty_list.append(self.info_list[i])
        # print test
        # print(f"player number : {self.player_number}")
        # print(f"info_list length : {len(self.info_list)}")
        for i in range(0,len(empty_list)):
            self.info_list.remove(empty_list[i])
        for i in range(1, len(self.info_list)):
            if self.info_list[i].player is None:
                self.info_list[i].player = AI(i, [], i)
                self.info_list[i].is_choose = False
            self.info_list[i].player.turn = i
            self.info_list[i].player.number = i

        self.turn_list = [component.player for component in self.info_list]
        for player in self.turn_list:
            if player.type == "Human":
                self.me = player

    def draw_from_center(self, input_deck):
        # print("draw_from_center")
        self.draw_card(input_deck)
        self.is_get = True
        self.turn_list[self.turn_index].uno = "unactive"

    def player_card_setting(self):
        sorted_list = []
        stage_list = ["A", "C", "D", "NORMAL", "Human", "B"]
        b_list = []
        b_count = 0
        for stage in stage_list:
            for player in self.turn_list:
                if player.stage == stage:
                    if stage == "B":
                        b_count += 1
                    sorted_list.append(player)
        for player in sorted_list:
            if player.stage == "Human":
                print("Human loop")
                for i in range(7):
                    self.draw_card(player.hand)
            elif player.stage == "A":
                prob = 60
                for i in range(7):
                    if random.randrange(0, 100) < prob:
                        while True:
                            random_card = random.choice(self.deck)
                            if random_card.skill is not None:
                                player.hand.append(random_card)
                                self.deck.remove(random_card)
                                break
                    else:
                        while True:
                            random_card = random.choice(self.deck)
                            if random_card.skill is None:
                                player.hand.append(random_card)
                                self.deck.remove(random_card)
                                break
            elif player.stage == "B":
                self.is_AI_B = True
                b_list.append(player)
            elif player.stage == "C":
                self.is_AI_C = True
                for i in range(7):
                    self.draw_card(player.hand)
            elif player.stage == "D":
                for i in range(3):
                    self.draw_card(player.hand)
            elif player.stage == "NORMAL":
                for i in range(7):
                    self.draw_card(player.hand)
        if self.is_AI_B:
            draw = True
            while draw:
                for b in b_list:
                    if len(b.hand) > 30:
                        draw = False
                        break
                    self.draw_card(b.hand)
    def check_condition(self, input_card):
        now = self.now_card

        if input_card.is_wild or now.is_wild:
            return True

        if input_card.color == now.color:  # yellow none 9 / blue none 5
            return True
        elif input_card.number == now.number:
            if input_card.color is not None and input_card.skill is not None:
                if input_card.skill == now.skill:
                    return True
                return False
            return True
        elif input_card.skill == now.skill:  # yellow none 9 / blue none 5
            if input_card.color is not None and input_card.number is not None:
                return False
            return True
        else:
            return False

    def set_skill_text(self, text):
        self.skill_active_button.text = text
        self.is_skill_active = True

    def skill_active(self, pop_card):
        next_player = self.turn_index + 1
        if next_player == len(self.turn_list):
            next_player = 0

        if pop_card.skill == "reverse":
            self.set_skill_text("reverse active : turn reversed")
            self.reverse_turn()
        elif pop_card.skill == "block":
            self.set_skill_text("block active")
            self.info_list[next_player].is_block = True
            pygame.time.set_timer(self.block_timer, 1000)
            self.block_turn()
        elif pop_card.skill == "change" or pop_card.skill == "all":
            if self.turn_list[self.turn_index].type == "Human":
                if self.is_color_change:
                    self.is_color_change = False
                    return 0
                self.is_color_change = True
            elif self.turn_list[self.turn_index].type == "AI":
                self.change_color_ai()
            else:
                pass

        elif pop_card.skill == "plus2":
            self.set_skill_text("plus2 attack active")
            self.plus(self.turn_list[next_player].hand, 2)

            self.animation_list.append(Animation(
                self.deck_rect.center,
                self.info_list[next_player].rect.center,
                pygame.time.get_ticks(),
                2
            ))
            pygame.time.set_timer(self.animation_list[-1].timer, 2000)
            self.soundFX.soundPlay(4)

        elif pop_card.skill == "plus4" or pop_card.skill == "all4":
            self.set_skill_text("plus4 attack active")
            self.plus(self.turn_list[next_player].hand, 4)

            self.animation_list.append(Animation(
                self.deck_rect.center,
                self.info_list[next_player].rect.center,
                pygame.time.get_ticks(),
                4
            ))
            pygame.time.set_timer(self.animation_list[-1].timer, 2000)
            self.soundFX.soundPlay(4)


    def change_color_ai(self):
        color_list = {"red": 0, "blue": 0, "green": 0, "yellow": 0}

        if self.turn_list[self.turn_index].hand is not None:
            for hand in self.turn_list[self.turn_index].hand:
                color = hand.color
                if color == None:
                    continue
                if color != None:
                    color_list[color] += 1
        self.change_color(max(color_list, key=color_list.get))

    def change_color(self, after_color):
        self.set_skill_text(f"color is changed {self.now_card.color} > {after_color}")
        self.now_card.color = after_color
        # lsj: 색약모드 change card
        if self.config["color"]["default"] == str(2):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/normalMode/change/{self.now_card.color}_change.png"
            ).convert_alpha()
        elif self.config["color"]["default"] == str(1):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/YB/change/{self.now_card.color}_change.png"
            ).convert_alpha()
        elif self.config["color"]["default"] == str(0):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/RG/change/{self.now_card.color}_change.png"
            ).convert_alpha()
        self.now_card_surf = pygame.transform.scale(self.now_card_surf, (50, 70))

# stageC 수정
    def random_change_color(self, now_card, after_color):
        self.set_skill_text(f"color is changed {self.now_card.color} > {after_color}")
        now_card.color = after_color
        if now_card.is_wild:
            return
        if now_card.number != None:
            self.colorBlind(now_card.number, after_color)
        if now_card.skill != None:
            self.colorBlind(now_card.skill, after_color)    
        
    def colorBlind(self, type, after_color):
        if self.config["color"]["default"] == str(2):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/normalMode/{type}/{after_color}_{type}.png"
            ).convert_alpha()
        elif self.config["color"]["default"] == str(1):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/YB/{type}/{after_color}_{type}.png"
            ).convert_alpha()
        elif self.config["color"]["default"] == str(0):
            self.now_card_surf = pygame.image.load(
                f"resources/images/card/RG/{type}/{after_color}_{type}.png"
            ).convert_alpha()
        self.now_card_surf = pygame.transform.scale(self.now_card_surf, (50, 70))        


    # def colorBlind(self, type):
    #     if self.config["color"]["default"] == str(2):
    #         self.now_card_surf = pygame.image.load(
    #             f"resources/images/card/normalMode/{self.now_card.number}/{self.now_card.color}_{self.now_card.number}.png"
    #         ).convert_alpha()
    #     elif self.config["color"]["default"] == str(1):
    #         self.now_card_surf = pygame.image.load(
    #             f"resources/images/card/YB/{self.now_card.number}/{self.now_card.color}_{self.now_card.number}.png"
    #         ).convert_alpha()
    #     elif self.config["color"]["default"] == str(0):
    #         self.now_card_surf = pygame.image.load(
    #             f"resources/images/card/RG/{self.now_card.number}/{self.now_card.color}_{self.now_card.number}.png"
    #         ).convert_alpha()
    #     self.now_card_surf = pygame.transform.scale(self.now_card_surf, (50, 70))        

    def pass_turn(self):
        self.turn_index += 1
        self.turn_counter += 1
        if self.turn_counter % 5 == 0 and self.is_AI_C:
            print(self.now_card.color)
            self.random_change_color(self.now_card, self.change_color_list[random.randint(0,3)][3])
            print("COLOR CHANGE")
            print(self.now_card.color)
            
        if self.turn_index == len(self.turn_list):
            self.turn_index = 0
        self.is_get = False
        self.current_time = 10
        if(self.turn_list[self.turn_index] == self.me) : self.turnCount += 1   # achievement
        if (
            len(self.turn_list[self.turn_index].hand) == 1
            and self.turn_list[self.turn_index].uno == "active"
        ):
            self.draw_card(self.turn_list[self.turn_index].hand)
            self.turn_list[self.turn_index].uno = "unactive"

        # 일반카드를 냈을 때도 텍스트가 뜨는 코드 > 바꿔야함
        if self.is_skill_active:
            pygame.time.set_timer(self.skill_active_timer, 2000)

    def check_collide(self, pos):
        # print("check_collide")
        for card in self.me.hand:
            if card.rect.collidepoint(pos):
                return True
        if self.deck_rect.collidepoint(pos):
            return True
        else:
            return False

    def press_uno(self):
        self.uno_pressed = True
        pygame.time.set_timer(self.uno_active_timer, 1000)
        if self.is_uno:
            if self.me.uno == "active":
                self.me.uno = "success"
                self.uno_active_button.text = "UNO success"
                print("uno defence success")

            for player in self.turn_list:
                if player != self.me and player.uno == "active":
                    self.draw_card(player.hand)
                    player.uno = "unactive"
                    self.uno_active_button.text = "UNO attack success"
        else:
            self.uno_active_button.text = "nobody UNO"

    def calculation_point(self, input_hand):
        point = 0
        for card in input_hand:
            if card.is_wild:
                point += 5
            elif card.skill:
                point += 3
            else:
                point += 1
        return point

    def test_set_all_card_to_red0(self):
        self.deck.clear()
        for _ in range(0, 128):
            self.deck.append(Card("red", None, 0, False, self.config))
        self.now_card = Card("blue", None, 1, False, self.config)
        self.now_card_surf = self.now_card.image

    def pause_event_handling(self):
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.event_active = False

    # 마우스 이벤트를 처리할 때, 이벤트 처리를 다시 시작하는 함수
    def resume_event_handling(self):
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_allowed(pygame.MOUSEMOTION)
        self.event_active = True

    def edit_name_function(self, screen):
        self.edit_name = True
        while self.edit_name:
            screen.blit(self.alpha_surface, (0, 0))

    def checkAchieve(self):
        if self.config["Achievement"]["singleclear"] == "0":
            self.achieve.accomplish(0)
        if self.turnCount <= 10 and self.config["Achievement"]["in10turnwin"] == "0":
            self.achieve.accomplish(6)
        if self.numNeverUsed and self.config["Achievement"]["onlyskillcardwin"] == "0":
            self.achieve.accomplish(8)
        if self.skillNeverUsed and self.config["Achievement"]["onlynumbercardwin"] == "0":
            self.achieve.accomplish(7)
        if self.otherUno and self.config["Achievement"]["otherplayerunowin"] == "0":
            self.achieve.accomplish(9)
    
    def refillCard(self):
        print("refill Card called")
        if len(self.remain) == 0: return False
        random.shuffle(self.remain)
        while len(self.remain) != 0:
            card = self.remain.pop()
            self.deck.append(card)
            
        self.soundFX.soundPlay(4)
        return True
