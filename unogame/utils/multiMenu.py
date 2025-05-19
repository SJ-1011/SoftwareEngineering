import pygame
from pygame.locals import *
import sys
import socket, requests, re
from multi_play import Game
from network import server, client

class multiPlayMenu:
    def __init__(self, keys, font, screen, config, soundFX):
        self.items = ["Create a Game", "Enter the Game", "Go Back"]
        self.items2 = ["Enter", "Go Back"]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.keys = keys
        self.config = config
        self.key_font = pygame.font.SysFont(None, 60)
        self.visible = [False, 255]
        self.backImage = [pygame.image.load('./resources/images/menu/multi_S.png'), pygame.image.load('./resources/images/menu/multi.png'),
                          pygame.image.load('./resources/images/menu/multi_L.png')]
        self.window = self.config['window']['default']
        req = requests.get("http://ipconfig.kr")
        self.hostIP = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
        self.soundFX = soundFX
        self.option = 'menu'                     # option = 0이면 선택창, option = 1이면 client menu
        self.text = ''
        self.cursorAct = False
        self.x, self.y, self.z = 48, 80, 60             # 글씨 크기 모음

        self.existPassword = False
        

        # Clear the screen
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.window = self.config['window']['default']
        if self.window == '1':
            self.screen.blit(self.backImage[0], (0, 0))
            self.x, self.y, self.z = 38, 64, 48
        elif self.window == '2':
            self.screen.blit(self.backImage[1], (0, 0))
            self.x, self.y, self.z = 48, 80, 60
        else:
            self.screen.blit(self.backImage[2], (0, 0))
            self.x, self.y, self.z = 61, 102, 77
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()
        if self.option == 'menu':
            CurrentIPAddress = "Current IP Address: "
            hostText = pygame.font.SysFont(None, self.x).render(CurrentIPAddress + self.hostIP, True, (255, 255, 255))
            self.screen.blit(hostText, (screenW - hostText.get_width() - screenW // 100, screenH // 100))

            
            multi = "Multi Player Game"
            multiText = pygame.font.SysFont(None, self.y).render(multi, True, (0, 0, 0))
            self.screen.blit(multiText, (screenW // 6, screenH // 3.5))

            # Draw the menu items
            for i, item in enumerate(self.items):
                text = pygame.font.SysFont(None, self.z).render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                )
                self.screen.blit(
                    text, (screenW // 6, screenH // 3 + 150 + i * (self.z + 10))
                )
        elif self.option == 'client' or 'password':
            input_box = pygame.Rect(0, 0, self.screen.get_width() // 1.5, self.screen.get_height() // 10)
            if self.option == 'password': input_box.width = self.screen.get_width() // 5
            input_box.center = (self.screen.get_width() // 2, self.screen.get_height() // 2.5)
            optionFont = pygame.font.SysFont(None, screenW // 10)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)
            text_surface = optionFont.render(self.text, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Draw the menu items
            if self.option == 'client':
                input_name = optionFont.render("IP Address", True, (0,0,0))
            elif self.option == 'password':
                input_name = optionFont.render("Password", True, (0,0,0))
            self.screen.blit(
                input_name, (self.screen.get_width() // 2 - input_name.get_width() // 2, self.screen.get_height() // 4.5)
            )
            for i, item in enumerate(self.items2):
                text = self.key_font.render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                )
                self.screen.blit(
                    text, (screenW // 3 * (i + 1) - text.get_width() // 2, screenH * 0.6)
                )
            
        

    def run(self):
        clock = pygame.time.Clock()
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and self.option == 'menu':
                    if event.key == self.keys["UP"]:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == self.keys["DOWN"]:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == self.keys["RETURN"]:
                        if self.selected == 0:
                            self.option = 'menu'
                            
                            # game = Game(self.screen, 1, self.keys, self.config, self.soundFX)           # 멀프 방만들기 삽입
                            
                            ## server open
                            self.server = server.server(False,self.screen, self.keys, self.config, self.soundFX)
                            self.server.main()
                            
                            # game.start_multi_play()
                        elif self.selected == 1:
                            self.option = 'client'
                        elif self.selected == 2:
                            self.option = 'menu'
                            return self.selected
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()


                elif event.type == KEYDOWN and (self.option == 'client' or 'password'):
                    if event.key == self.keys["LEFT"]:
                        self.selected = (self.selected - 1) % len(self.items2)
                    elif event.key == self.keys["RIGHT"]:
                        self.selected = (self.selected + 1) % len(self.items2)
                    elif event.key == self.keys["RETURN"]:
                        if self.selected == 0:
                            self.client = client.client(self.text, self.screen, self.keys, self.config, self.soundFX)
                            self.client.main()
                            print(self.text)    
                            # Todo: self.text(입력한 주소)의 방으로 연결시켜야함
                            self.text = ''    
                            # Todo: 비밀번호가 있으면 입력

                            if self.option == 'client' and self.existPassword:
                                self.option = 'password'
                        elif self.selected == 1:
                            self.text = ''
                            self.option = 'menu'
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()
                    else:
                        if event.unicode.isnumeric() or event.unicode == '.':
                            self.text += event.unicode
                        if (len(self.text) > 4 or event.unicode == '.') and self.option == 'password':
                            self.text = self.text[:-1]


                elif (event.type == MOUSEMOTION or MOUSEBUTTONUP) and self.option == 'menu':
                    pos = pygame.mouse.get_pos()
                    for i, item in enumerate(self.items):
                        text = pygame.font.SysFont(None, self.z).render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 6, screenH // 3 + 150 + i * (self.z + 10)
                        )
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if i == 0:
                                    self.option = 'menu'
                                    
                                    ## server open
                                    self.server = server.server(False, self.screen, self.keys, self.config, self.soundFX)
                                    self.server.main()
                                    
                                    # game = Game(self.screen, 1, self.keys, self.config, self.soundFX)
                                    # game.start_multi_play()                                     # 멀프 방만들기 삽입
                                elif i == 1:
                                    self.option = 'client'
                                    ## client open
                                    # self.client = client.client(self.text, self.screen, self.keys, self.config, self.soundFX)
                                    # self.client.main()
                                elif i == 2:
                                    self.option = 'menu'
                                    return i
                                
                elif (event.type == MOUSEMOTION or MOUSEBUTTONUP) and (self.option == 'client' or 'password'):
                    input_box = pygame.Rect(0, 0, self.screen.get_width() // 1.5, self.screen.get_height() // 10)
                    if self.option == 'password': input_box.width = self.screen.get_width() // 5
                    input_box.center = (self.screen.get_width() // 2, self.screen.get_height() // 2.5)
                    pos = pygame.mouse.get_pos()

                    for i, item in enumerate(self.items2):
                        text = self.font.render(item, True, (255, 255, 255))
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 3 * (i + 1) - text.get_width() // 2, screenH * 0.6
                        )
                        if rect.collidepoint(pos):
                            if event.type == MOUSEMOTION:
                                self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if i == 0:
                                    ## client open
                            
                                    self.client = client.client(self.text, self.screen, self.keys, self.config, self.soundFX)
                                    self.client.main()
                                    print(self.text)                            # Todo: self.text(입력한 주소)의 방으로 연결시켜야함
                                    self.text = ''
                                    if self.option == 'client' and self.existPassword:
                                        self.option = 'password'
                                elif i == 1:
                                    self.text = ''
                                    self.option = 'menu'

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
