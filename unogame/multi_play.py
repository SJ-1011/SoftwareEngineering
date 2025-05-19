import itertools
import random
import sys
import socket, requests, re

import pygame

from models.button import Button, Component
from models.card import Card
from models.Human import Human
from models.AI import AI

from models.button import Button, Component
from pause import PauseClass
import time


class Game:
    pygame.font.init()
    font = pygame.font.Font("./resources/fonts/Pixeltype.ttf", 36)
    spacing = 2
    card_width = 50
    card_height = 70

    CENTER_X_POS = 625
    CENTER_Y_POS = 325
    change_color_list = []  # color change 시 표시될 사각형들

    def __init__(self, screen, player_number, keys, config, soundFX):
        self.start_count = 1

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.player_number = player_number

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
        self.edit_name = False
        self.edit_text = "__________"
        req = requests.get("http://ipconfig.kr")
        self.hostIP = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]


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
            center=(self.screen_width / 2, self.screen_height / 2 + 50)
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
            40,
            30,
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
            (64, 64, 64),
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
            (64, 64, 64),
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
        # print(f"self.info_list[0] : {self.info_list[0].text}")

        self.move_surf = pygame.image.load(
            "resources/images/card/normalMode/backcard.png"
        ).convert_alpha()
        self.move_surf = pygame.transform.scale(self.move_surf, (50, 70))
        self.move_rect = self.move_surf.get_rect(
            center=(self.screen_width, self.screen_height)
        )

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
            self.screen_height / 2 - 20,
            100,
            40,
            (255, 255, 255),
            "Player 1 win !!",
            (64, 64, 64),
            30,
            0,
        )

        self.AI_timer = pygame.USEREVENT + 5
        self.is_computer_turn = False
        self.AI_timer_on = False

        self.uno_timer = pygame.USEREVENT + 2
        self.is_uno = False

        self.skill_active_timer = pygame.USEREVENT + 3
        self.is_skill_active = False

        self.block_timer = pygame.USEREVENT + 4

    def start_multi_play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        clock = pygame.time.Clock()

        while self.run:
            screen.fill((50, 200, 50))
            self.make_screen()
            # event loop

            ## lms

            if self.game_active:
                self.time_button.text = f"TIME : {self.current_time}"
                self.time_button.draw(screen)
            ##

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        font = pygame.font.SysFont(None, 48)

                        pause = PauseClass(
                            screen, font, self.config, self.keys, self.soundFX
                        )
                        value = pause.run()
                        for card in self.card_list:
                            card.change_path(self.config)
                        self.me.update_hand(screen)
                        self.now_card_surf = self.now_card.image
                        if value == "out":
                            return
                # 치트키
                #                    if event.key == pygame.K_q and self.game_active:
                #                        self.turn_list[self.turn_index].hand.clear()
                #
                #                    if event.key == pygame.K_w and self.game_active:
                #                        self.turn_list[2].hand.clear()

                if self.is_win and not self.game_active:
                    if not self.event_active:
                        pygame.time.delay(1000)
                        # print("event_active")
                        self.resume_event_handling()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # print(self.who.number)
                        # print(type(self.who.number))
                        return (
                            self.who.number
                        )  ################################################################

                # Timer 재설정 하는 event loop
                # if event.type == self.AI_timer:
                # self.is_computer_turn = True

                if event.type == self.AI_timer and self.game_active:
                    self.is_computer_turn = True
                    self.AI_timer_on = False

                if event.type == self.turn_timer and self.game_active:
                    if self.current_time == 0:
                        self.current_time = 10
                        if not self.is_get:
                            self.draw_from_center(self.turn_list[self.turn_index].hand)
                        if self.is_color_change:
                            self.is_color_change = False
                            var = random.randint(0, 3)
                            if self.config["color"]["default"] == str(2):
                                self.now_card_surf = pygame.image.load(
                                    f"resources/images/card/normalMode/change/{self.change_color_list[var][3]}_change.png"
                                ).convert_alpha()
                            elif self.config["color"]["default"] == str(1):
                                self.now_card_surf = pygame.image.load(
                                    f"resources/images/card/YB/change/{self.change_color_list[var][3]}_change.png"
                                ).convert_alpha()
                            elif self.config["color"]["default"] == str(0):
                                self.now_card_surf = pygame.image.load(
                                    f"resources/images/card/RG/change/{self.change_color_list[var][3]}_change.png"
                                ).convert_alpha()

                            self.now_card_surf = pygame.transform.scale(
                                self.now_card_surf, (50, 70)
                            )
                            self.now_card.color = self.change_color_list[var][3]
                            self.is_color_change = False
                        self.pass_turn()
                        break
                    self.current_time -= 1

                if (
                    event.type == self.skill_active_timer
                    and self.game_active
                    and not self.is_win
                ):
                    self.is_skill_active = False
                if (
                    event.type == self.block_timer
                    and self.game_active
                    and not self.is_win
                ):
                    for component in self.info_list:
                        component.is_block = False
                # 게임 전 카드 덱과 손 패를 세팅하는 부분 > 따로빼서 함수로 refactor하기
                elif (
                    event.type == pygame.MOUSEBUTTONUP
                    and self.start_button.rect.collidepoint(event.pos)
                    and not self.edit_name
                ):
                    if not self.game_active:
                        self.game_active = True
                        self.is_win = False
                        self.generate_deck()
                        # self.test_set_all_card_to_red0()
                        # 여기서 덱 위에 있는 카드들을 나눠줌
                        for player in self.turn_list:
                            print("Player-card_setting1!!")
                            self.player_card_setting(player)
                            self.turn_index += 1
                        # self.deck.clear()
                        self.turn_index = 0
                        # test
                        # while True:
                        #     if len(self.deck) == 1:
                        #         break
                        #     self.draw_card(self.turn_list[self.turn_index].hand)
                        # for _ in range(0, 6):
                        #     self.me.hand.pop()
                        # for _ in range(0, 5):
                        #     self.turn_list[self.turn_index + 1].hand.pop()
                        # for _ in range(0, 6):
                        #     self.turn_list[self.turn_index + 2].hand.pop()
                else:
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_active:
                    for i in range(2, len(self.info_list)):
                        if (
                            self.info_list[i].is_clicked(event.pos)
                            and self.info_list[i].text != "EMPTY"
                        ):
                            if self.player_number > 2:
                                self.player_number -= 1
                        elif (
                            self.info_list[i].is_clicked(event.pos)
                            and self.info_list[i].text == "EMPTY"
                        ):
                            if self.player_number <= 5:
                                self.player_number += 1
                    if self.info_list[0].is_clicked(event.pos):
                        self.edit_name = True

                if event.type == pygame.KEYDOWN and self.edit_name:
                    if self.edit_text == "__________":
                        self.edit_text = ""

                    if event.key == pygame.K_BACKSPACE:
                        self.edit_text = self.edit_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.info_list[0].text = self.edit_text
                        if self.edit_text == "__________" or self.edit_text == "":
                            self.info_list[0].text = "PLAYER 1(ME)"
                        self.edit_name = False
                    else:
                        if len(self.edit_text) < 8:
                            self.edit_text += pygame.key.name(event.key)

                if event.type == pygame.MOUSEBUTTONDOWN and self.edit_name:
                    if self.ok_button.is_clicked(event.pos):
                        self.info_list[0].text = self.edit_text
                        if self.edit_text == "__________" or self.edit_text == "":
                            self.info_list[0].text = "PLAYER 1(ME)"
                        self.edit_name = False

                # 매 턴 UNO를 할 수 있는지 없는지 체크하는 부분
                for player in self.turn_list:
                    if len(player.hand) == 1 and player.uno == "unactive":
                        # print("uno timer start")
                        pygame.time.set_timer(self.uno_timer, 2000, 1)
                        player.uno = "active"
                        self.is_uno = True
                        break
                if event.type == self.uno_timer and self.game_active:
                    for player in self.turn_list:
                        # print(f"self.me.uno : {self.me.uno}")
                        if player.uno == "active" and player == self.me:
                            self.draw_card(player.hand)
                            player.uno = "unactive"
                        elif player.uno == "active" and player != self.me:
                            # print("computer defense success")
                            player.uno = "success"
                    self.is_uno = False

                # 카드에 마우스커서를 올렸을 때 애니메이션 > 리팩토링

                if (
                    event.type == pygame.MOUSEMOTION
                    and self.game_active
                    and not self.is_color_change
                    ## test lines
                    # and self.me.type == "Human"
                ):
                    for card in self.me.hand:
                        if card.rect.collidepoint(event.pos):
                            self.now_select = card
                    for rect in [
                        self.deck_rect,
                        self.uno_button.rect,
                    ]:
                        if rect.collidepoint(event.pos):
                            if rect == self.deck_rect and len(self.deck) == 0:
                                pass
                            else:
                                self.now_select = rect
                elif (
                    event.type == pygame.MOUSEMOTION
                    and self.game_active
                    and not self.is_color_change
                    ## test lines
                    # and self.me.type == "Human"
                ):
                    if self.uno_button.rect.collidepoint(event.pos):
                        self.now_select = self.uno_button
                # 키보드 입력을 정의
                if (
                    event.type == pygame.KEYDOWN
                    and self.game_active
                    and not self.is_color_change
                    and self.me.type == "Human"
                ):
                    if event.key == self.keys["RIGHT"]:
                        # print("key pressed")
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select == self.deck_rect:
                            self.now_select = self.uno_button
                        elif self.now_select == self.uno_button and len(self.deck) != 0:
                            self.now_select = self.deck_rect

                        elif (
                            len(self.me.hand) == self.me.hand.index(self.now_select) + 1
                        ):
                            self.now_select = self.me.hand[0]
                        else:
                            self.now_select = self.me.hand[
                                self.me.hand.index(self.now_select) + 1
                            ]

                    elif event.key == self.keys["LEFT"]:
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select == self.deck_rect and len(self.deck) != 0:
                            self.now_select = self.uno_button

                        elif self.now_select == self.uno_button:
                            self.now_select = self.deck_rect

                        elif self.me.hand.index(self.now_select) == 0:
                            self.now_select = self.me.hand[len(self.me.hand) - 1]
                        else:
                            self.now_select = self.me.hand[
                                self.me.hand.index(self.now_select) - 1
                            ]

                    elif event.key == self.keys["UP"]:
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select in self.me.hand:
                            if len(self.deck):
                                self.now_select = self.deck_rect
                            else:
                                self.now_select = self.uno_button
                        elif self.now_select in [
                            self.deck_rect,
                            self.uno_button,
                        ]:
                            self.now_select = self.me.hand[0]
                    elif event.key == self.keys["DOWN"]:
                        if self.now_select is None:
                            self.now_select = self.me.hand[0]
                        elif self.now_select in self.me.hand:
                            if len(self.deck):
                                self.now_select = self.deck_rect
                            else:
                                self.now_select = self.uno_button
                        elif self.now_select in [
                            self.deck_rect,
                            self.uno_button,
                        ]:
                            self.now_select = self.me.hand[0]
                elif (
                    event.type == pygame.KEYDOWN
                    and self.game_active
                    and not self.is_color_change
                    and self.me.turn != self.turn_index
                ):
                    if event.key:
                        self.now_select = self.uno_button
                # self.is_color_change에 따라 색깔을 바꿔주는 옵션
                if self.is_color_change and event.type == pygame.MOUSEBUTTONDOWN:
                    for color_list in self.change_color_list:
                        if color_list[1].collidepoint(event.pos):
                            # lsj: 색약모드 change card
                            if self.config["color"]["default"] == str(2):
                                self.now_card_surf = pygame.image.load(
                                    f"resources/images/card/normalMode/change/{color_list[3]}_change.png"
                                ).convert_alpha()
                            elif self.config["color"]["default"] == str(1):
                                self.now_card_surf = pygame.image.load(
                                    f"resources/images/card/YB/change/{color_list[3]}_change.png"
                                ).convert_alpha()
                            elif self.config["color"]["default"] == str(0):
                                self.now_card_surf = pygame.image.load(
                                    f"resources/images/card/RG/change/{color_list[3]}_change.png"
                                ).convert_alpha()

                            self.now_card_surf = pygame.transform.scale(
                                self.now_card_surf, (50, 70)
                            )
                            self.now_card.color = color_list[3]
                            self.is_color_change = False
                            self.pass_turn()

                # 클릭 및 엔터 이벤트
                if self.game_active and not self.is_color_change:
                    pos = (0, 0)
                    key = None

                    if self.turn_list[self.turn_index].type == "Human":
                        if (
                            event.type == pygame.MOUSEBUTTONDOWN
                            or event.type == pygame.KEYDOWN
                        ):
                            if event.type == pygame.KEYDOWN:
                                key = event.key
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = event.pos

                            # 0 덱이 있는지 확인 점수 계산
                            ## back up code
                            # if len(self.deck) == 0:
                            # print("덱이 없어서 계산을 합니다")
                            #     win_condition = True
                            #     for player in self.turn_list:
                            #         for card in player.hand:
                            #             if self.check_condition(card):
                            #                 win_condition = False

                            #     if win_condition:
                            #         less_point = self.calculation_point(self.me.hand)
                            #         for player in self.turn_list:
                            #             if less_point >= self.calculation_point(
                            #                 player.hand
                            #             ):
                            #                 less_point = self.calculation_point(
                            #                     player.hand
                            #                 )
                            #                 self.win_button.text = (
                            #                     f"Player {player.number + 1} win !!"
                            #                 )
                            #         self.game_active = False
                            #         self.is_win = True

                            #         self.pause_event_handling()
                            ## back up code

                            # print(pos)
                            # 1. 낼 수 있는 카드를 낸다

                            if (key == self.keys["RETURN"]) or (
                                self.check_collide(pos) and key is None
                            ):
                                if self.now_select in self.me.hand:
                                    if self.check_condition(self.now_select):
                                        pop_card = self.now_select
                                        self.turn_list[self.turn_index].hand.remove(
                                            pop_card
                                        )
                                        self.now_select = None
                                        # self.remain.append(pop_card)
                                        if pop_card.skill is not None:
                                            self.skill_active(pop_card)
                                        if pop_card.skill not in [
                                            "change",
                                            "block",
                                            "all",
                                        ]:
                                            self.pass_turn()
                                        # print(pop_card.skill)

                                        self.now_card = pop_card
                                        self.now_card_surf = pop_card.image

                                # 2. 가운데에서 카드를 가져온다 > 낼 수 있는 카드가 있다면 낸다
                                if (
                                    (key == self.keys["RETURN"] and pos is None)
                                    or (self.check_collide(pos) and key is None)
                                    and self.now_select == self.deck_rect
                                    and not self.is_get
                                ):
                                    self.draw_from_center(
                                        self.turn_list[self.turn_index].hand
                                    )
                                    self.now_select = None
                                    # # 3. 낼 수 있는 카드가 없거나, 가운데에서 이미 카드를 가져온 상태면 PASS를 눌러 턴을 넘김
                                    # if (
                                    #     (key == self.keys["RETURN"] and pos is None)
                                    #     or (self.check_collide(pos) and key is None)
                                    #     and self.now_select == self.skip_button
                                    #     and self.is_get
                                    # ):
                                    self.pass_turn()
                                    self.next_screen(screen)
                    # 4. 컴퓨터의 알고리즘 수행

                    ## lms
                    if self.turn_list[self.turn_index].type == "AI":
                        if self.is_computer_turn:
                            self.computer_turn()
                            self.is_computer_turn = False
                            # self.next_screen(screen)
                        if not self.AI_timer_on and not self.is_computer_turn:
                            pygame.time.set_timer(self.AI_timer, 2000)
                            self.AI_timer_on = True
                        print("AI timer set")

                        # for card in self.turn_list[self.turn_index].hand:
                        #     if self.check_condition(card):
                        #         self.com_card.append(card)
                        # if len(self.com_card) == 0:
                        #     self.draw_from_center(self.turn_list[self.turn_index].hand)
                        #     self.pass_turn()
                        # else:
                        #     self.now_card = self.com_card[0]
                        #     self.now_card_surf = self.now_card.image
                        #     self.turn_list[self.turn_index].hand.remove(self.now_card)
                        #     self.remain.append(self.now_card)
                        #     if self.now_card.skill is not None:
                        #         # edit by sth
                        #         # self.skill_active(self.now_card.skill)
                        #         self.skill_active(self.com_card[0])
                        #     if self.now_card.skill not in [
                        #         "change",
                        #         "block",
                        #         "all",
                        #     ]:
                        #         self.pass_turn()
                    if self.start_count:
                        self.next_screen(screen)
                        self.start_count -= 1

                    ## lms

                    # 5. 카드가 1장만 남았을 경우 UNO 버튼을 눌러야 한다.
                    if (
                        (key == self.keys["RETURN"] and pos is None)
                        or (self.check_collide(pos) and key is None)
                        and self.now_select == self.uno_button
                        and self.is_uno
                    ):
                        # print("if enter")
                        self.press_uno()
                    # 6. 누군가의 덱이 모두 사라지면 그 사람의 승리 > 승리 화면 전환 > 메인 화면 전환
                    for player in self.turn_list:
                        if len(player.hand) == 0:
                            self.game_active = False
                            self.is_win = True

                            #################################################
                            self.who = player
                            ##################################################

                            self.win_button.text = f"Player {player.number + 1} win !!"
                            self.pause_event_handling()

                    # # 7. 뽑을 수 있는 카드가 없고, 모든 플레이어가 현재 낼 수 있는 카드가 없으면 카드가 가장 적은 사람이 승리
                    self.deck_none()

                    ## back up code
                    # if len(self.deck) == 0:
                    #     win_condition = True
                    #     for player in self.turn_list:
                    #         for card in player.hand:
                    #             if self.check_condition(card):
                    #                 win_condition = False

                    #     if win_condition:
                    #         less_point = self.calculation_point(self.me.hand)
                    #         for player in self.turn_list:
                    #             if less_point >= self.calculation_point(player.hand):
                    #                 less_point = self.calculation_point(player.hand)
                    #                 self.win_button.text = (
                    #                     f"Player {player.number + 1} win !!"
                    #                 )
                    #         self.game_active = False
                    #         self.is_win = True

                    #         self.pause_event_handling()
                    ### back up code

            # event loop 종료 *****************************
            self.next_screen(screen)

            # if self.game_active:
            #     if len(self.deck):
            #         screen.blit(self.deck_surf, self.deck_rect)
            #     screen.blit(self.now_card_surf, self.now_card_rect)

            #     # 누구의 턴인지 보여주는 부분
            #     screen.blit(
            #         self.now_turn_list[self.turn_index][0],
            #         self.now_turn_list[self.turn_index][1],
            #     )

            #     # 손패를 그려주는 부분
            #     self.me.draw_hand(screen)

            #     if self.is_color_change:
            #         screen.blit(self.alpha_surface, (0, 0))
            #         for color_list in self.change_color_list:
            #             screen.blit(color_list[0], color_list[1])

            #     self.uno_button.draw(screen)
            #     if self.is_get:
            #         self.skip_button.surface.fill((255, 255, 255))
            #         self.skip_button.draw(screen)
            #     else:
            #         self.skip_button.surface.fill((120, 120, 120))
            #         self.skip_button.draw(screen)
            #     if self.now_select and self.me.turn == self.turn_index:
            #         pygame.draw.rect(screen, (0, 0, 0), self.now_select, 5)
            #     pygame.draw.rect(screen, (20, 20, 20), self.lobby_background)
            #     for i in range(0, self.player_number - 1):
            #         self.info_list[i].draw(screen)

            #     self.time_button.text = f"TIME : {self.current_time}"
            #     self.time_button.draw(screen)

            # else:
            #     screen.fill("green")
            #     # 게임이 종료되었을 때 덱 초기화
            #     for player in self.turn_list:
            #         player.hand.clear()
            #     self.deck.clear()
            #     self.remain.clear()

            #     pygame.draw.rect(screen, (20, 20, 20), self.lobby_background)
            #     self.add_button.draw(screen)
            #     self.del_button.draw(screen)
            #     for i in range(0, self.player_number - 1):
            #         self.info_list[i].draw(screen)
            #     self.start_button.draw(screen)

            #     for i in range(0, self.player_number - 1):
            #         self.info_list[i].draw(screen)

            #     if self.is_win:
            #         screen.blit(
            #             self.win_list[self.turn_index][0],
            #             self.win_list[self.turn_index][1],
            #         )
            #         screen.blit(self.retry_surf, self.retry_rect)
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)

    def computer_turn(self):
        self.com_card = []

        for card in self.turn_list[self.turn_index].hand:
            if self.check_condition(card):
                self.com_card.append(card)
        if len(self.com_card) == 0:
            self.draw_from_center(self.turn_list[self.turn_index].hand)
            self.pass_turn()
        else:
            self.now_card = self.com_card[0]
            self.now_card_surf = self.now_card.image
            self.turn_list[self.turn_index].hand.remove(self.now_card)
            self.remain.append(self.now_card)
            if self.now_card.skill is not None:
                # edit by sth
                # self.skill_active(self.now_card.skill)
                self.skill_active(self.com_card[0])
            if self.now_card.skill not in [
                # "change",
                "block",
                # "all",
            ]:
                self.pass_turn()

    def deck_none(self):
        if len(self.deck) == 0:
            print("덱이 없어서 계산을 합니다")
            win_condition = True

            ## back up code
            # for player in self.turn_list:
            #     for card in player.hand:
            #         if self.check_condition(card):
            #             win_condition = False
            ## back up code

            ## test
            for hand in self.turn_list[self.turn_index].hand:
                if self.check_condition(hand):
                    win_condition = False
                    break

            ##

            if win_condition:
                less_point = self.calculation_point(self.me.hand)
                for player in self.turn_list:
                    if less_point >= self.calculation_point(player.hand):
                        less_point = self.calculation_point(player.hand)
                        self.win_button.text = f"Player {player.number + 1} win !!"
                    self.who = player
                self.game_active = False
                self.is_win = True
                self.pause_event_handling()

    def next_screen(self, screen):
        # print("next_screen")

        if self.game_active:
            ## error point!!
            ##
            if len(self.deck):
                screen.blit(self.deck_surf, self.deck_rect)
            screen.blit(self.now_card_surf, self.now_card_rect)

            # 누구의 턴인지 보여주는 부분
            if self.turn_list[self.turn_index].type == "Human":
                # if self.me.turn == self.turn_index:
                self.now_turn_button.text = f"my turn"
            if self.turn_list[self.turn_index].type == "AI":
                self.now_turn_button.text = f"PLAYER {self.turn_index + 1}'s turn"
            self.now_turn_button.draw(screen)
            # screen.blit(
            #     self.now_turn_list[self.turn_index][0],
            #     self.now_turn_list[self.turn_index][1],
            # )

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
            # if self.is_get:
            #     self.skip_button.surface.fill((255, 255, 255))
            #     self.skip_button.draw(screen)
            # else:
            #     self.skip_button.surface.fill((120, 120, 120))
            #     self.skip_button.draw(screen)
            if (
                self.now_select and self.me.turn == self.turn_index
            ) or self.now_select == self.uno_button:
                pygame.draw.rect(screen, (0, 0, 0), self.now_select, 3)

            pygame.draw.rect(screen, (47, 101, 177), self.lobby_background)
            for i in range(0, self.player_number):
                self.info_list[i].draw(screen, self.player_number, i)

            ## test
            # self.time_button.text = f"TIME : {self.current_time}"
            # self.time_button.draw(screen)
            ##

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
        else:
            screen.fill("green")
            # 게임이 종료되었을 때 덱 초기화
            for player in self.turn_list:
                player.hand.clear()
            self.deck.clear()
            self.remain.clear()

            if self.is_win:
                ## time.sleep(3)
                time.sleep(3)
                self.win_button.draw(screen)
                screen.blit(self.retry_surf, self.retry_rect)
            else:
                CurrentIPAddress = "Host IP Address: "
                hostText = self.font.render(CurrentIPAddress + self.hostIP, True, (0, 0, 0))
                self.screen.blit(hostText, (self.screen.get_width() // 2 - hostText.get_width() // 2, self.screen.get_height() * 0.02))

                self.start_button.draw(screen)
                pygame.draw.rect(screen, (47, 101, 177), self.lobby_background)
                for i in range(0, len(self.info_list)):
                    self.info_list[i].draw(screen, self.player_number, i)

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
                # self.add_button.draw(screen)
                # self.del_button.draw(screen)

            pygame.display.update()

    def make_screen(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.deck_rect.centerx = self.screen_width / 3
        self.deck_rect.centery = self.screen_height / 3

        self.uno_button.rect.x = self.deck_rect.centerx + 150
        self.uno_button.rect.y = self.deck_rect.centery + 30

        self.retry_rect.centerx = self.screen_width / 2
        self.retry_rect.centery = self.screen_height / 2 + 50

        self.start_button.rect.x = self.screen_width // 2 - 100
        self.start_button.rect.y = self.screen_height // 2 - 30

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
            self.screen_width / 2 - 50,
            self.screen_height / 2 - 20,
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

        # self.name_rect.x = self.screen_width // 2
        # self.name_rect.y = self.screen_height // 2 - 20
        # self.input_rect.x = self.screen_width // 2
        # self.input_rect.y = self.screen_height // 2 + 50

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

    def block_turn(self):
        # print("block_turn")
        # print(f"before block : {self.turn_index}")
        ## test
        # if self.turn_list[self.turn_index].type == "AI":
        #     print("computer turn!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # else:
        #     print("human turn!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        ##
        self.turn_index = (self.turn_index + 1) % len(self.turn_list)
        # print(f"after block : {self.turn_index}")

        self.current_time = 10
        self.pass_turn()

    def reverse_turn(self):
        temp_player = self.turn_list[self.turn_index]

        self.turn_list.reverse()
        for player in self.turn_list:
            player.turn = self.turn_list.index(player)

        self.turn_index = self.turn_list.index(temp_player)

        ## lms
        for player in self.turn_list:
            if player.type == "Human":
                self.me = player

        ## error point

    def change_color(self):
        # print("change_color")
        if self.is_color_change:
            self.is_color_change = False
            return 0
        self.is_color_change = True

    def draw_card(self, input_deck):
        # print("draw_card 1059")
        if len(input_deck) == 0 and input_deck == self.deck:
            return
        if len(self.deck) != 0:
            pop_card = self.deck.pop()
            input_deck.append(pop_card)

    # 중복 부분
    # def plus(
    #     self, input_deck, next_player, count
    # ):  # deck : list / first, second : card
    #     for _ in range(count):
    #         if len(self.deck) != 0:
    #             pop_card = self.deck.pop()
    #             input_deck.append(pop_card)

    def plus(self, input_deck, count):  # deck : list / first, second : card
        # print("plus")
        for _ in range(count):
            if len(self.deck) != 0:
                pop_card = self.deck.pop()
                input_deck.append(pop_card)

    # def hand_update(self, input_deck):
    #     for i, card in enumerate(input_deck):
    #         card.rect.x = i * (Game.card_width + Game.spacing) + self.screen_width // 6 - len(input_deck) * (
    #                 Game.card_width + Game.spacing) // 2
    #         card.rect.y = card.initial_y

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
            temp_card = Card(None, None, "all4", True, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

            temp_card = Card(None, None, "all4", True, self.config)
            self.deck.append(temp_card)
            self.card_list.append(temp_card)

        random.shuffle(self.deck)
        pop_card = self.deck.pop()
        # test
        # for card in self.deck:
        #     if card.is_wild:
        #         pop_card = card
        #         break

        self.remain.append(pop_card)  # 낸 카드 리스트에 pop_card 추가(바닥에 있는 카드)
        self.turn_index = 0
        self.now_card = pop_card  # pop_card(바닥에 있는 카드)가 현재 카드임
        self.now_card_surf = pop_card.image  # 현재 카드 객체화
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

        self.turn_list = [
            Human(i, [], i) if i == 0 else AI(i, [], i)
            for i in range(self.player_number)
        ]

        # for player in self.turn_list:
        # print(player)

        for i, component in enumerate(self.info_list):
            component.player = self.turn_list[i]
            if i == len(self.turn_list) - 1:
                break

            for player in self.turn_list:
                if player.type == "Human":
                    self.me = player

            # print("self.me : ", self.me.type, "1081")

    # self.turn_index를 더 깔끔하게 다루기
    def draw_from_center(self, input_deck):
        # print("draw_from_center")
        self.draw_card(input_deck)
        self.is_get = True
        self.turn_list[self.turn_index].uno = "unactive"
        # # layer를 다시 수정해주는 작업
        # for i, card in enumerate(input_deck.sprites()):
        #     # input_deck.change_layer(card, len(input_deck.sprites()) - i - 1)
        #     input_deck.change_layer(card, i)

    def player_card_setting(self, player):
        # print("player_card_setting")
        # 초기에 7장 뽑기
        # 맨 처음에 카드 나눠줄 때만 사용하는 함수라 if 문 삭제함
        for i in range(7):
            self.draw_card(player.hand)

    def check_condition(self, input_card):
        # print("check_condition")
        # input 카드가 현재 맨 위에 있는 카드에 낼 수 있는 카드인지 확인하는 함수

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

    def skill_active(self, pop_card):
        # print("skill_active")
        next_player = self.turn_index + 1
        if next_player == len(self.turn_list):
            next_player = 0

        if pop_card.skill == "reverse":
            self.skill_active_button.text = "reverse active : turn reversed"
            self.reverse_turn()
        elif pop_card.skill == "block":
            self.skill_active_button.text = f"block active"
            self.info_list[next_player].is_block = True
            # 타이머를 설정하고 타이머가 끝나면 X가 삭제
            pygame.time.set_timer(self.block_timer, 1000)
            self.block_turn()
        elif pop_card.skill == "change" or pop_card.skill == "all":
            self.skill_active_button.text = (
                f"color is changed {self.now_card.color} > {pop_card.color}"
            )
            if self.turn_list[self.turn_index].type == "Human":
                ## error point
                # print("플레이어가 색깔을 바꿉니다.")
                self.change_color()
            elif self.turn_list[self.turn_index].type == "AI":
                ## error point
                # print("AI가 색깔을 바꿉니다.")
                self.change_color_ai()
            else:
                pass

        elif pop_card.skill == "plus2":
            self.skill_active_button.text = "plus2 attack active"
            self.plus(self.turn_list[next_player].hand, 2)
        elif pop_card.skill == "plus4" or pop_card.skill == "all4":
            self.skill_active_button.text = "plus4 attack active"
            self.plus(self.turn_list[next_player].hand, 4)
        self.is_skill_active = True

    def change_color_ai(self):
        # print("change_color_ai")
        color_list = {"red": 0, "blue": 0, "green": 0, "yellow": 0}
        ## error

        if self.turn_list[self.turn_index].hand is not None:
            for hand in self.turn_list[self.turn_index].hand:
                color = hand.color
                # print(color)
                if color == None:
                    # if color != "None":
                    # print("color is not none")
                    # print("color is bool none")
                    continue
                if color != None:
                    color_list[color] += 1

        self.now_card.color = max(color_list, key=color_list.get)
        # print(self.now_card.color)

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
        self.now_card_rect = self.now_card_surf.get_rect(
            center=(self.screen_width / 3 + 100, self.screen_height / 3)
        )

    def pass_turn(self):
        # print("pass_turn")
        # print("turn is passed")
        ## test
        # if self.turn_list[self.turn_index].type == "AI":
        #     print("computer turn!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # else:
        #     print("human turn!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # ##

        self.turn_index += 1
        if self.turn_index == len(self.turn_list):
            self.turn_index = 0
        self.is_get = False
        self.current_time = 10
        if (
            len(self.turn_list[self.turn_index].hand) == 1
            and self.turn_list[self.turn_index].uno == "active"
        ):
            self.draw_card(self.turn_list[self.turn_index].hand)
            self.turn_list[self.turn_index].uno = "unactive"

        # 일반카드를 냈을 때도 텍스트가 뜨는 코드 > 바꿔야함
        pygame.time.set_timer(self.skill_active_timer, 3000)

    def check_collide(self, pos):
        # print("check_collide")
        for card in self.me.hand:
            if card.rect.collidepoint(pos):
                return True
        if self.deck_rect.collidepoint(pos):
            return True
        elif self.uno_button.rect.collidepoint(pos):
            return True
        else:
            return False

    def press_uno(self):
        # print("press_uno")
        # print("calling")
        # print(f"self.me.uno : {self.me.uno} / self.is_uno : {self.is_uno}")
        # print(self.me.uno == "active")
        # print(self.is_uno)
        if self.me.uno == "active" and self.is_uno:
            self.me.uno = "success"
        # print(f"self.me.uno : {self.me.uno} / self.is_uno : {self.is_uno}")

    def calculation_point(self, input_hand):
        # print("calculation_point")
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

    def card_move(self, start, end, card, clock):
        temp = Card(None, None, None, False)
        if card is not None:
            temp = card
        temp.rect.x += 100 * clock.get_time() / 1000
