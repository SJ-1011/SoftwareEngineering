import pygame, configparser
import sys
from pygame.locals import *
from utils import menu , settings, sound, achieveMenu



class PauseClass:

    def __init__(self, screen, font, config, key, soundFX):
        self.screen = screen                                                        # 게임의 스크린
        self.font = font                                                            # 폰트
        self.title_font = pygame.font.SysFont(None, 72)
        self.key_font = pygame.font.SysFont(None, 48)
        self.items = ['Resume', 'Settings', 'Achievement','Return to menu']
        self.title_text = self.title_font.render("PAUSE", True, (255, 255, 255))
        self.keys = key
        self.selected = 0
        self.config = config
        self.soundFX = soundFX
        self.backImage = pygame.image.load('./resources/images/play/play2.png')


        self.screen.blit(self.backImage, (0, 0))

    def draw(self):
        # backImage_num = self.config['window']['default']
        # if backImage_num == '1':
        #     new_backImage = pygame.transform.scale(self.backImage, (800, 600))
        # elif backImage_num == '2':
        #     new_backImage = pygame.transform.scale(self.backImage, (1000, 750))
        # elif backImage_num == '3':
        #     new_backImage = pygame.transform.scale(self.backImage, (1280, 960))
        self.screen.blit(self.backImage, (0, 0))
        # self.screen.fill((68, 86, 213))

        # Draw the title
        self.screen.blit(
            self.title_text,
            (self.screen.get_width() // 2 - self.title_text.get_width() // 2, self.screen.get_height() // 6),
        )

        # Draw the menu items
        for i, item in enumerate(self.items):
            text = self.font.render(
                item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
            )
            self.screen.blit(
                text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 + i * 50)
            )


    def run(self):
        clock = pygame.time.Clock()
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        # 메인 루프
        running = True
        while running:
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.keys["UP"]:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == self.keys["DOWN"]:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == self.keys["RETURN"]:
                        if self.selected == 0:                                      # Resume 선택 -> 게임 계속하기
                            return
                        elif self.selected == 1:                                    # Settings 선택 -> 설정 화면으로
                            setting = settings.Setting(self.keys, self.font, self.screen, self.soundFX, self.config)
                            num = setting.run()
                        elif self.selected == 2:
                            print("achieve")
                            achieve = achieveMenu.achieveMenu(self.keys, self.font, self.screen, self.config, self.soundFX)
                            num = achieve.run()
                        elif self.selected == 3:                                    # Return to menu 선택 -> 메뉴 화면으로
                            return "out"
                    elif event.key == self.keys["ESCAPE"]:                          # 게임 계속 진행하기
                        return


                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            self.screen.get_width() // 2 - text.get_width() // 2,
                            self.screen.get_height() // 2 + i * 50,
                        )
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if self.selected == 0:                                      # Resume 선택 -> 게임 계속하기
                                    return
                                elif self.selected == 1:                                    # Settings 선택 -> 설정 화면으로
                                    setting = settings.Setting(self.keys, self.font, self.screen, self.soundFX, self.config)
                                    num = setting.run()
                                elif self.selected == 2:
                                    print("achieve")
                                    achieve = achieveMenu.achieveMenu(self.keys, self.font, self.screen, self.config, self.soundFX)
                                    num = achieve.run()
                                elif self.selected == 3:                                    # Return to menu 선택 -> 메뉴 화면으로
                                    return "out"
            
            # 화면 채우기
            self.draw()
            
            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)