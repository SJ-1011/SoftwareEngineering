import pygame, configparser
import sys
from pygame.locals import *
from utils import sound

class Setting:
    
    def __init__(self, keys, font, screen, sounds, config):
        self.items = [
                      ["Window Size", "Key Configuration", "Color Blindness Mode", "Set Volume", "Reset Settings"],
                      ["800 x 600", "1000 x 750", "1280 x 960"],
                      list(keys.items()),
                      ["Deuteranopia(Red-Green)", "Tritanopia(Blue-Yellow)", "None"],
                      ["Music Volume", "", "Sound Volume", ""]
                      ]
        self.font = font
        self.screen = screen
        self.selected = 0
        self.title_font = pygame.font.SysFont(None, 72)
        self.titles = ["Settings", "Window Size", "Key Configuration", "Color Blindness Mode", "Set Volume"]
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 20)
        self.option = 0 
        self.sounds = sounds
        self.visible = [False, 255]
        self.backImage = [pygame.image.load('./resources/images/menu/setting.png'), pygame.image.load('./resources/images/menu/setting_L.png')]

        # load data
        self.config = config
        
        # Clear the screen
        if self.config['window']['default'] == '3':
            self.screen.blit(self.backImage[1], (0, 0))
        else:
            self.screen.blit(self.backImage[0], (0, 0))


    def draw(self):
        if self.config['window']['default'] == '3':
            self.screen.blit(self.backImage[1], (0, 0))
        else:
            self.screen.blit(self.backImage[0], (0, 0))
        self.title_text = self.title_font.render(self.titles[self.option], True, (255, 255, 255))
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        # Draw the title
        self.screen.blit(
            self.title_text,
            (screenW // 10, screenH // 12),
        )


        # Draw the menu items
        gap = 80
        if self.option == 0 : gap = 70
        for i, item in enumerate(self.items[self.option]):
            if self.option == 2: #key setting의 경우 간격 다르게
                text = self.font.render(
                f"{item[0]}: {pygame.key.name(item[1]).capitalize()}",
                True,
                (255, 255, 255) if i != self.selected else (255, 0, 0)
                )
                gap = 50
            elif self.option == 4: #volume setting이면 선택해도 색 안 바뀜
                text = self.font.render(item, True, (255, 255, 255))
            else:   
                text = self.font.render(
                    item, True, (255, 255, 255) if i != self.selected else (255, 0, 0)
                    )
                
            self.screen.blit(
                text,
                (screenW // 5, screenH // 4 + i * gap)
            )
        if self.option == 4: #draw volume setting (if in volume setting)
            fonts = pygame.font.SysFont(None, 60)
            minus1 = fonts.render("-",True,(255, 255, 255) if self.selected != 0 else (255,0,0))
            minus2 = fonts.render("-",True,(255, 255, 255) if self.selected != 1 else (255,0,0))
            minus3 = fonts.render("-",True,(255, 255, 255) if self.selected != 5 else (255,255,0))
            plus1 = fonts.render("+",True,(255, 255, 255) if self.selected != 2 else (255,0,0))
            plus2 = fonts.render("+",True,(255, 255, 255) if self.selected != 3 else (255,0,0))
            plus3 = fonts.render("+",True,(255, 255, 255) if self.selected != 6 else (255,255,0))
            self.screen.blit(minus1, (screenW // 4, screenH // 4 + 1 * gap))
            self.screen.blit(minus2, (screenW // 4, screenH // 4 + 3 * gap))
            self.screen.blit(minus3, (screenW // 10 + 300, screenH // 12 + 5))
            self.screen.blit(plus1, (screenW * 3 // 4, screenH // 4 + 1 * gap))
            self.screen.blit(plus2, (screenW * 3 // 4, screenH // 4 + 3 * gap))
            self.screen.blit(plus3, (screenW // 10 + 340, screenH // 12 + 5))

            musicVol = sound.getMusicVol()
            soundVol = self.sounds.getSoundVol()
            for i in range(0, int(musicVol)):
                pygame.draw.rect(
                    self.screen, 
                    (255,255,255), 
                    pygame.Rect(screenW * 27//100 + (i+1) * screenW // 25, screenH // 4 + 1 * gap + 10, screenW // 27, 20)
                    )
            for i in range(int(musicVol), 10):
                pygame.draw.rect(
                    self.screen, 
                    (70,70,70), 
                    pygame.Rect(screenW * 27//100 + (i+1) * screenW // 25, screenH // 4 + 1 * gap + 10, screenW // 27, 20)
                    )
            for i in range(0, int(soundVol)):
                pygame.draw.rect(
                    self.screen, 
                    (255,255,255), 
                    pygame.Rect(screenW * 27//100 + (i+1) * screenW // 25, screenH // 4 + 3 * gap + 10, screenW // 27, 20)
                    )
            for i in range(int(soundVol), 10):
                pygame.draw.rect(
                    self.screen, 
                    (70,70,70), 
                    pygame.Rect(screenW * 27//100 + (i+1) * screenW // 25, screenH // 4 + 3 * gap + 10, screenW // 27, 20)
                    )




        
        #Draw "Save"
        text = self.font.render("Save", True,
                                (255, 255, 255) if len(self.items[self.option]) != self.selected else (255, 255, 0)
                                )
        self.screen.blit(
            text,
            (screenW // 5, screenH * 10 // 12)
            )
        
        #Show Keys Event
        if self.visible[0] and self.option != 2: 
            for i, (name, key) in enumerate(self.keys.items()):
                text = self.key_font.render(
                        f"{name}: {pygame.key.name(key).capitalize()}",
                        True,
                        (255, 255, 255)
                    )
                text.set_alpha(self.visible[1])
                self.screen.blit(text, (
                    screenW // 10 * 8,
                    screenH // 12 + i * 30
                    ))
            
            if self.visible[1] < 10:
                self.visible[0] = False
                self.visible[1] = 0
            else: self.visible[1] -= 2



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
                elif event.type == KEYDOWN:
                    if event.key == self.keys["UP"]:
                        self.selected -= 1
                        if self.option == 4:
                            if self.selected >= 4: self.selected = 4
                            elif abs(self.selected) == 1: self.selected = 5
                            elif self.selected == 3: self.selected = 1
                        else: self.selected %= (len(self.items[self.option])+1)
                    elif event.key == self.keys["DOWN"]:
                        self.selected += 1
                        if self.option == 4:
                            if self.selected >= 6: self.selected = 0
                            elif self.selected == 2: self.selected = 4
                        else:  self.selected %= (len(self.items[self.option])+1)
                    elif event.key == self.keys["LEFT"] and self.option == 4:
                        if self.selected == 5: self.selected = 6
                        elif self.selected == 6: self.selected = 5
                        else: self.selected = (self.selected - 2) % (len(self.items[self.option]))
                    elif event.key == self.keys["RIGHT"] and self.option == 4:
                        if self.selected == 5: self.selected = 6
                        elif self.selected == 6: self.selected = 5
                        else: self.selected = (self.selected + 2) % (len(self.items[self.option]))
                    elif event.key == self.keys["RETURN"]:
                        if self.option == 0 and self.selected == 4 : # setting 화면의 reset 버튼
                            self.reset()
                            screenW = self.screen.get_width() # 화면 크기 다시 계산
                            screenH = self.screen.get_height()
                        elif self.option == 0 and self.selected == len(self.items[self.option]) : # setting 화면의 save 버튼
                            with open('setting_data.ini', 'w') as f:
                                    self.config.write(f)
                            return 0
                        elif self.option == 0: # setting 화면에 save 제외 버튼 누를 경우
                            self.option = self.selected+1
                            self.selected = len(self.items[self.option])                                # option 3이 색맹모드
                        elif self.selected == len(self.items[self.option]): # 다른 화면의 save 버튼
                            self.option = 0
                            self.selected = len(self.items[self.option])
                        elif self.option == 1: # 화면 바꾸기 세팅
                            self.screenSize(self.selected+1)
                            screenW = self.screen.get_width() # 화면 크기 다시 계산
                            screenH = self.screen.get_height()
                        elif self.option == 2: # 키 설정 세팅
                            print(self.selected)
                            self.configKeys(self.selected) # selected는 left 0 right 1 up 2 ...
                        elif self.option == 3:                                                      # selected가 0이면 RG, 1이면 YB, 2면 None
                            self.setBlindness(self.selected)
                        elif self.option == 4:
                            if self.selected == 0: 
                                sound.musicDown()
                                self.config['sound']['music'] = str(sound.getMusicVol())
                            elif self.selected == 1:
                                self.sounds.soundDown()
                                self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                            elif self.selected == 2: 
                                sound.musicUp()
                                self.config['sound']['music'] = str(sound.getMusicVol())
                            elif self.selected == 3: 
                                self.sounds.soundUp()
                                self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                            elif self.selected == 5:
                                sound.musicDown()
                                self.config['sound']['music'] = str(sound.getMusicVol())
                                self.sounds.soundDown()
                                self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                            elif self.selected == 6:
                                sound.musicUp()
                                self.config['sound']['music'] = str(sound.getMusicVol())
                                self.sounds.soundUp()
                                self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                    elif event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.visible = [True, 255]

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    gap = 80
                    if self.option == 0 : gap = 70
                    for i, item in enumerate(self.items[self.option]):
                        if self.option == 2 and type(item[1]) == int:
                            text = self.font.render(
                                f"{item[0]}: {pygame.key.name(item[1]).capitalize()}",
                                True,
                                (255, 255, 255)
                            )
                            gap = 50
                        elif type(item) == str:
                            text = self.font.render(
                            item,
                            True,
                            (255, 255, 255)
                            )
                        
                        rect = text.get_rect()
                        rect.topleft = (
                            screenW // 5,
                            screenH // 4 + i * gap
                        )
                        if rect.collidepoint(pos) and self.option != 4:
                            if event.type == MOUSEMOTION: self.selected = i
                            elif event.type == MOUSEBUTTONUP:
                                if self.option == 0 and self.selected == 4: # setting 화면의 reset 버튼
                                    self.reset()
                                    screenW = self.screen.get_width() # 화면 크기 다시 계산
                                    screenH = self.screen.get_height()
                                elif self.option == 0: # setting 화면의 다른 버튼
                                    self.option = i+1
                                elif self.option == 1: # 화면 바꾸기 세팅
                                    self.screenSize(self.selected+1)
                                    screenW = self.screen.get_width() # 화면 크기 다시 계산
                                    screenH = self.screen.get_height()
                                elif self.option == 2: # 키 설정 변경
                                    self.configKeys(self.selected)
                                elif self.option == 3:
                                    self.setBlindness(self.selected)
                    if self.option == 4: # volume setting의 경우
                        fonts = pygame.font.SysFont(None, 60)
                        icons = [
                            fonts.render("-",True,(255, 255, 255)),
                            fonts.render("-",True,(255, 255, 255)),
                            fonts.render("+",True,(255, 255, 255)),
                            fonts.render("+",True,(255, 255, 255))
                            ]
                        for i, icon in enumerate(icons):
                            rect = icon.get_rect()
                            rect.topleft = (screenW * (1 + (i//2)*2) // 4, screenH // 4 + (1 + (i%2)*2) * gap)
                            if rect.collidepoint(pos):
                                if event.type == MOUSEMOTION: self.selected = i
                                elif event.type == MOUSEBUTTONDOWN:
                                    if self.selected == 0: 
                                        sound.musicDown()
                                        self.config['sound']['music'] = str(sound.getMusicVol())
                                    elif self.selected == 1:
                                        self.sounds.soundDown()
                                        self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                                    elif self.selected == 2: 
                                        sound.musicUp()
                                        self.config['sound']['music'] = str(sound.getMusicVol())
                                    elif self.selected == 3: 
                                        self.sounds.soundUp()
                                        self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                        all = [fonts.render("-",True,(255, 255, 255)), fonts.render("+",True,(255, 255, 255))]
                        for i, icon in enumerate(all): # 전체 소리 조정
                            rect = icon.get_rect()
                            rect.topleft = (screenW // 10 + 300 + 40 * i, screenH // 12 + 5)
                            if rect.collidepoint(pos):
                                if event.type == MOUSEMOTION: self.selected = i+5
                                elif event.type == MOUSEBUTTONDOWN:
                                    if self.selected == 5:
                                        sound.musicDown()
                                        self.config['sound']['music'] = str(sound.getMusicVol())
                                        self.sounds.soundDown()
                                        self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                                    elif self.selected == 6:
                                        sound.musicUp()
                                        self.config['sound']['music'] = str(sound.getMusicVol())
                                        self.sounds.soundUp()
                                        self.config['sound']['sound'] = str(self.sounds.getSoundVol())
                        
                        

                    save = self.font.render("Save", True, (255, 255, 255))
                    rectSave = save.get_rect()
                    rectSave.topleft = (
                        screenW // 5,
                        screenH * 10 // 12
                    )
                    if rectSave.collidepoint(pos): # Save 버튼
                        if event.type == MOUSEMOTION: self.selected = len(self.items[self.option])
                        elif event.type == MOUSEBUTTONUP: 
                            if self.option == 0 and self.selected == len(self.items[self.option]): # 메인 화면의 Save 버튼을 눌렀을 때
                                with open('setting_data.ini', 'w') as f: # ini 파일에 저장
                                    self.config.write(f)
                                    if self.config['window']['default'] == '3':
                                        self.screen.blit(self.backImage[1], (0, 0))
                                    else:
                                        self.screen.blit(self.backImage[0], (0, 0))
                                return 0
                            else: # 다른 setting 화면의 Save 버튼을 눌렀을 때
                                if self.config['window']['default'] == '3':
                                    self.screen.blit(self.backImage[1], (0, 0))
                                else:
                                    self.screen.blit(self.backImage[0], (0, 0))
                                self.option = 0

            # Draw the menu
            self.draw()

            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
    
    def screenSize(self, option):
        if option == 1:
            self.screen = pygame.display.set_mode((800, 600))
        elif option == 2:
            self.screen = pygame.display.set_mode((1000, 750))
        elif option == 3:
            self.screen = pygame.display.set_mode((1280, 960))
        self.config['window']['default'] = str(option)
    
    def configKeys(self, option):
        selKey = self.items[2][option] #Tuple of selected key

        text = self.font.render(
                f"{selKey[0]}: {pygame.key.name(selKey[1]).capitalize()}",
                True,
                (255, 255, 0)
            )
        self.screen.blit(
                text,
                (self.screen.get_width() // 5, self.screen.get_height() // 4 + option * 50)
            )
        pygame.display.update()

        getKey = True
        while getKey: # 무조건 key down 해서 설정키 바꾸게 함
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    for i, (name, key) in enumerate(self.keys.items()): # 키 중복 방지
                        if key == event.key and i != option: return
                    self.keys[selKey[0]] = event.key
                    self.items[2][option] = (selKey[0], event.key)
                    self.config['key'][selKey[0].lower()] = str(event.key)                      
                        
                    getKey = False

    def setVolume(self, option):
        pass

    def setBlindness(self, option):
        if option == 0:
            print("RG")
            self.config['color']['default'] = str(0)
        elif option == 1:
            print("YB")
            self.config['color']['default'] = str(1)

        elif option == 2:
            print("None")
            self.config['color']['default'] = str(2)
        return

    def reset(self):        
        # Screen size reset
        self.screen = pygame.display.set_mode((800, 600))
        self.config['window']['default'] = "1"
        self.config['color']['default'] = '2'

        # Game key reset
        for i, (name, key) in enumerate(self.keys.items()):
            self.keys[name] = pygame.key.key_code(name.lower())
            self.config['key'][name.lower()] = str(pygame.key.key_code(name.lower()))
        self.items[2] = list(self.keys.items())

        # Color mode reset

        #Volume reset
        sound.resetMusicVol()
        self.sounds.resetSoundVol()
        self.config['sound']['music'] = "6"
        self.config['sound']['sound'] = "2"