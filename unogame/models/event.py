import pygame
import random
import sys

import pygame

from pause import PauseClass

from models.animation import Animation
from models.AI import AI

from models.button import Component


class Event:
    pygame.init()

    def __init__(self, game):
        self.game = game
        self.config = game.config
    def event_loop(self, event, game):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            font = pygame.font.SysFont(None, 48)

            pause = PauseClass(
                game.screen, font, game.config, game.keys, game.soundFX
            )
            value = pause.run()  # Todo: 일시정지 후 게임 내부 크기 조절 기능 필요..
            for card in game.card_list:
                print(f"path : {card.file_path}")
                print(f"config : {game.config['color']['default']}")
                card.change_path(game.config)
            if game.game_active:
                game.me.update_hand(game.screen)
                game.now_card_surf = game.now_card.image
            if value == "out":
                return value
            game.make_screen()

            # # 치트키
        elif event.type == pygame.KEYDOWN and event.key in [pygame.K_q, pygame.K_w, pygame.K_t]:
            if event.key == pygame.K_q and game.game_active:
                game.turn_list[game.turn_index].hand.clear()

            if event.key == pygame.K_w and game.game_active:
                game.turn_list[1].hand = game.turn_list[1].hand[:1]

            if event.key == pygame.K_t and game.game_active:
                game.game_active = False
                game.is_win = True
                print("Key pressed")
            # # 치트키

        elif game.is_win and not game.game_active:
            if not game.event_active:
                pygame.time.delay(500)
                # hy - delay after the game end
                pygame.event.clear()
                # print("event_active")
                game.resume_event_handling()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return "out"

        # Timer 재설정 하는 event loop
        for ani in game.animation_list:
            if event.type == ani.timer and game.game_active:
                game.animation_list.remove(ani)
        if event.type == game.AI_timer and game.game_active:
            game.is_computer_turn = True
            game.AI_timer_on = False
            pygame.time.set_timer(game.AI_timer, 0)

        elif event.type == game.turn_timer and game.game_active:
            if game.current_time == 0:
                game.current_time = 10
                if not game.is_get:
                    game.draw_from_center(game.turn_list[game.turn_index].hand)

                    game.animation_list.append(Animation(
                        game.deck_rect.center,
                        game.me.hand[0].rect.center,
                        pygame.time.get_ticks(),
                        1
                    ))
                    game.soundFX.soundPlay(4)
                    pygame.time.set_timer(game.animation_list[-1].timer, 2000)

                if game.is_color_change:
                    game.is_color_change = False
                    var = random.randint(0, 3)
                    game.change_color(game.change_color_list[var][3])
                game.pass_turn()
            game.current_time -= 1

        elif (
            event.type == game.skill_active_timer
            and game.game_active
            and not game.is_win
        ):
            game.is_skill_active = False
            game.skill_active_button.text = ""
        elif event.type == game.block_timer and game.game_active and not game.is_win:
            for component in game.info_list:
                component.is_block = False

        if (event.type == pygame.MOUSEBUTTONUP
            and game.start_button.rect.collidepoint(event.pos)
            and not game.edit_name
            # and not game.settingPassword
        ) or (event.type == pygame.KEYDOWN and event.key == game.keys["RETURN"] and not game.edit_name): #and not game.settingPassword):
            # 수정중
            if game.game_type == "stageA":
                game.info_list[1].is_empty = False
                game.info_list[1].player = AI(1, [], 1)
                game.info_list[1].player.stage = "A"
            elif game.game_type == "stageB":
                for i in range(1,4):
                    game.info_list[i].is_empty = False
                    game.info_list[i].player = AI(i, [], i)
                    game.info_list[i].player.stage = "B"
                    game.player_number += 1
                game.info_list[0].player.stage = "B"
            elif game.game_type == "stageC":
                for i in range(1,3):
                    game.info_list[i].is_empty = False
                    game.info_list[i].player = AI(i, [], i)
                    game.info_list[i].player.stage = "C"
                    game.player_number += 1

            elif game.game_type == "stageD":
                    game.info_list[1].is_empty = False
                    game.info_list[1].player = AI(1, [], 1)
                    game.info_list[1].player.stage = "D"

            if not game.game_active:
                if game.player_number == 1:
                    game.player_number += 1
                    game.info_list[1].is_empty = False
                game.game_active = True
                game.is_win = False
                game.generate_deck()
                game.player_card_setting()
                game.skill_active(game.now_card)
        elif event.type == pygame.KEYDOWN and game.edit_name:

            if game.edit_text == "__________":
                game.edit_text = ""

            if event.key == pygame.K_BACKSPACE:
                game.edit_text = game.edit_text[:-1]
            elif event.key == pygame.K_RETURN:
                if game.edit_text == "__________" or game.edit_text == "":
                    Component.now_component.is_edit = False
                else:
                    Component.now_component.text = game.edit_text
                    Component.now_component.is_edit = True
                game.edit_name = False
            else:
                if len(game.edit_text) < 8:
                    game.edit_text += pygame.key.name(event.key)

        elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and game.edit_name
                and game.ok_button.is_clicked(event.pos)
            ):
            Component.now_component.text = game.edit_text
            Component.now_component.is_edit = True

            if game.edit_text == "__________" or game.edit_text == "":
                Component.now_component.is_edit = False
            else:
                game.edit_text = "__________"
            game.edit_name = False
            Component.now_component = None

        elif event.type == pygame.KEYDOWN and game.edit_name and not game.game_active:
            if event.key == game.keys["RETURN"]:
                game.info_list[0].text = game.edit_text
                if game.edit_text == "__________" or game.edit_text == "":
                    game.info_list[0].text = "PLAYER 1(ME)"
                    game.edit_text = "__________"
                game.edit_name = False

        elif event.type == pygame.KEYDOWN and game.settingPassword:

            if game.edit_text == "__________":
                game.edit_text = ""

            if event.key == pygame.K_BACKSPACE:
                game.edit_text = game.edit_text[:-1]
            elif event.key == pygame.K_RETURN:
                if game.edit_text == "__________" or game.edit_text == "":
                    game.password = ""
                    game.edit_text = "__________"
                game.settingPassword = False
                game.ok_button.rect.x = game.screen_width // 2
                game.ok_button.rect.y = game.screen_height // 2 + 100
            elif event.unicode.isnumeric():
                if len(game.edit_text) < 4:
                    game.edit_text += event.unicode

        elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and game.settingPassword
                and game.ok_button.is_clicked(event.pos)
            ):
            game.password = game.edit_text
            if game.edit_text == "__________" or game.edit_text == "":
                game.password = ""
                game.edit_text = "__________"
            game.settingPassword = False
            game.ok_button.rect.x = game.screen_width // 2
            game.ok_button.rect.y = game.screen_height // 2 + 100

        if event.type == pygame.MOUSEBUTTONDOWN and not game.game_active and game.game_type[0:5] != "stage":
            for i in range(1, len(game.info_list)):
                if (
                        game.info_list[i].close_button.is_clicked(event.pos)
                        and not game.info_list[i].is_empty
                ):
                    if game.player_number > 1:
                        game.player_number -= 1
                        game.info_list[i].ban_player()
                elif (
                        game.info_list[i].is_clicked(event.pos)
                        and game.info_list[i].is_empty
                ):
                    if game.player_number <= 5:
                        game.player_number += 1
                        game.info_list[i].is_empty = False
                        game.info_list[i].is_choose = True
                elif not game.info_list[i].is_empty and game.info_list[i].is_choose and game.info_list[
                    i].change_clicked(event.pos):
                    game.info_list[i].is_choose = False
                    print(game.info_list[i].choose_AI_type(event.pos, i))

            if game.info_list[0].is_clicked(event.pos):
                game.edit_name = True
                Component.now_component = game.info_list[0]

        # 매 턴 UNO를 할 수 있는지 없는지 체크하는 부분
        for player in game.turn_list:
            if len(player.hand) == 1 and player.uno == "unactive":
                pygame.time.set_timer(game.uno_timer, 2000, 1)
                player.uno = "active"
                game.is_uno = True
                break
        if event.type == game.uno_timer and game.game_active:
            for player in game.turn_list:
                # 인간이면 2초가 지났을 때 무조건 우노 실패
                if player.uno == "active" and player.type == "Human":
                    game.draw_card(player.hand)
                    if(player.type == "Human"):  # achievement
                        game.otherUno = True
                    player.uno = "unactive"
                    game.uno_active_button.text = "defence failed"
                    game.uno_pressed = True
                    pygame.time.set_timer(game.uno_active_timer, 1000)
                # 컴퓨터라면 2초가 지났을 때 무조건 우노 성공
                elif player.uno == "active" and player.type == "AI":
                    player.uno = "success"
                    game.uno_active_button.text = "AI UNO success"
                    game.uno_pressed = True
                    pygame.time.set_timer(game.uno_active_timer, 1000)
            game.is_uno = False

        if event.type == game.uno_active_timer and game.game_active:
            game.uno_pressed = False
        # 카드에 마우스커서를 올렸을 때 애니메이션 > 리팩토링

        if (
            event.type == pygame.MOUSEMOTION
            and game.game_active
            and not game.is_color_change
        ):
            for card in game.me.hand:
                if card.rect.collidepoint(event.pos):
                    game.now_select = card
                    break
            for rect in [
                game.deck_rect,
                game.uno_button.rect,
            ]:
                if rect.collidepoint(event.pos):
                    if rect == game.deck_rect and len(game.deck) == 0:
                        pass
                    else:
                        game.now_select = rect
        elif (
            event.type == pygame.MOUSEMOTION
            and game.game_active
            and not game.is_color_change
        ):
            if game.uno_button.rect.collidepoint(event.pos):
                game.now_select = game.uno_button

        # 키보드 입력을 정의
        if (
            event.type == pygame.KEYDOWN
            and game.game_active
            and not game.is_color_change
            and game.me.type == "Human"
        ):
            if event.key == game.keys["RIGHT"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select == game.deck_rect:
                    game.now_select = game.uno_button
                elif game.now_select == game.uno_button and len(game.deck) != 0:
                    game.now_select = game.deck_rect

                elif len(game.me.hand) == game.me.hand.index(game.now_select) + 1:
                    game.now_select = game.me.hand[0]
                else:
                    game.now_select = game.me.hand[
                        game.me.hand.index(game.now_select) + 1
                    ]

            elif event.key == game.keys["LEFT"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select == game.deck_rect and len(game.deck) != 0:
                    game.now_select = game.uno_button

                elif game.now_select == game.uno_button:
                    game.now_select = game.deck_rect

                elif game.me.hand.index(game.now_select) == 0:
                    game.now_select = game.me.hand[len(game.me.hand) - 1]
                else:
                    game.now_select = game.me.hand[
                        game.me.hand.index(game.now_select) - 1
                    ]

            elif event.key == game.keys["UP"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select in game.me.hand:
                    if len(game.deck):
                        game.now_select = game.deck_rect
                    else:
                        game.now_select = game.uno_button
                elif game.now_select in [
                    game.deck_rect,
                    game.uno_button,
                ]:
                    game.now_select = game.me.hand[0]
            elif event.key == game.keys["DOWN"]:
                if game.now_select is None:
                    game.now_select = game.me.hand[0]
                elif game.now_select in game.me.hand:
                    if len(game.deck):
                        game.now_select = game.deck_rect
                    else:
                        game.now_select = game.uno_button
                elif game.now_select in [
                    game.deck_rect,
                    game.uno_button,
                ]:
                    game.now_select = game.me.hand[0]
        elif (
            event.type == pygame.KEYDOWN
            and game.game_active
            and not game.is_color_change
            and game.me.turn != game.turn_index
        ):
            if event.key:
                game.now_select = game.uno_button
        # game.is_color_change에 따라 색깔을 바꿔주는 옵션
        if game.is_color_change and event.type == pygame.MOUSEBUTTONDOWN:
            for color_list in game.change_color_list:
                if color_list[1].collidepoint(event.pos):
                    # lsj: 색약모드 change card
                    game.change_color(color_list[3])
                    game.is_skill_active = True
                    game.is_color_change = False
                    if game.turnCount == 1:
                        break
                    game.pass_turn()

        # 클릭 및 엔터 이벤트
        if game.game_active and not game.is_color_change:
            pos = (0, 0)
            key = None
            # 5. 카드가 1장만 남았을 경우 UNO 버튼을 눌러야 한다.
            if event.type == pygame.KEYDOWN:
                if event.key == game.keys["RETURN"] and game.now_select == game.uno_button:
                    print("uno_button active")
                    game.press_uno()
            elif(event.type == pygame.MOUSEBUTTONDOWN
                    and game.uno_button.rect.collidepoint(event.pos)
                    and game.now_select == game.uno_button):
                print("uno_button active")
                game.press_uno()

            if game.turn_list[game.turn_index].type == "Human":
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        key = event.key
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos

                    # 0 덱이 있는지 확인 점수 계산

                    # 1. 낼 수 있는 카드를 낸다

                    if (key == game.keys["RETURN"]) or (
                        game.check_collide(pos) and key is None
                    ):
                        if game.now_select in game.me.hand:
                            if game.check_condition(game.now_select):
                                game.animation_list.append(Animation(
                                    game.me.hand[0].rect.center,
                                    game.now_card_rect.center,
                                    pygame.time.get_ticks(),
                                    1
                                ))
                                game.soundFX.soundPlay(4)
                                pop_card = game.now_select
                                game.turn_list[game.turn_index].hand.remove(pop_card)
                                game.now_select = None
                                if pop_card.skill is not None:
                                    game.skill_active(pop_card)
                                    game.skillNeverUsed = False    # achievement
                                else: game.numNeverUsed = False    # achievement
                                if pop_card.skill not in [
                                    "change",
                                    "block",
                                    "all",
                                ]:
                                    game.pass_turn()
                                # achievement
                                if pop_card.skill in ["plus2", "plus4", "all4"]:
                                    game.luckyThree += 1
                                    print(game.luckyThree)
                                else: game.luckyThree = 0
                                if game.luckyThree == 3 and self.config['Achievement']['luckythree'] == '0':
                                    game.achieve.accomplish(11)

                                pygame.time.set_timer(game.animation_list[-1].timer, 2000)

                                game.remain.append(game.now_card)
                                game.now_card = pop_card
                                game.now_card_surf = pop_card.image

                        # 2. 가운데에서 카드를 가져온다
                        if (
                            (key == game.keys["RETURN"] and game.now_select == game.deck_rect)
                            or (game.check_collide(pos) and key is None and game.now_select == game.deck_rect)
                            and game.turn_index == game.me.turn
                        ):

                            game.draw_from_center(game.turn_list[game.turn_index].hand)

                            game.animation_list.append(Animation(
                                game.deck_rect.center,
                                game.me.hand[0].rect.center,
                                pygame.time.get_ticks(),
                                1
                            ))
                            game.soundFX.soundPlay(4)
                            pygame.time.set_timer(game.animation_list[-1].timer, 2000)

                            game.now_select = None
                            game.pass_turn()
                            game.next_screen(game.screen)

            # 4. 컴퓨터의 알고리즘 수행

            ## lms
            if game.turn_list[game.turn_index].type == "AI":
                if game.is_computer_turn:
                    game.computer_turn()
                    game.is_computer_turn = False
                    # game.next_screen(screen)
                elif not game.AI_timer_on and not game.is_computer_turn:
                    pygame.time.set_timer(game.AI_timer, 3000)
                    game.AI_timer_on = True
            if game.start_count:
                game.next_screen(game.screen)
                game.start_count -= 1

            ## lms


            # 6. 누군가의 덱이 모두 사라지면 그 사람의 승리 > 승리 화면 전환 > 메인 화면 전환
            for player in game.turn_list:
                if len(player.hand) == 0:
                    game.game_active = False
                    game.is_win = True

                    game.who = player
                    if game.who.type == "Human":
                        game.win_button.text = "You win !!"
                        game.checkAchieve()    # check achievement condition
                    else:
                        game.win_button.text = f"Player {player.number + 1} win !!"
                    #game.event_active = False
                    game.pause_event_handling()

            # # 7. 뽑을 수 있는 카드가 없고, 모든 플레이어가 현재 낼 수 있는 카드가 없으면 카드가 가장 적은 사람이 승리
            if(len(game.deck) == 0):
                game.refillCard()
            game.deck_none()
