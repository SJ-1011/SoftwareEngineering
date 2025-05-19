import pygame
from pygame.locals import *
import sys

class achieveMenu:
    def __init__(self, keys, font, screen, config, soundFX):
        self.font = font
        self.descriptionFont = pygame.font.SysFont(None, 20)
        self.screen = screen
        self.keys = keys
        self.key_font = pygame.font.SysFont(None, 76)
        self.visible = [False, 255]
        self.config = config
        self.window = int(self.config['window']['default'])
        self.soundFX = soundFX
        self.current = 0
        self.backImage = [pygame.image.load('./resources/images/achievement/background_S.png'), pygame.image.load('./resources/images/achievement/background.png'),
                          pygame.image.load('./resources/images/achievement/background_L.png')]
        self.achieveImage = [pygame.image.load('./resources/images/achievement/noAchieve.png'), pygame.image.load('./resources/images/achievement/achieve.png')]
        self.achieveImage_S = [pygame.image.load('./resources/images/achievement/noAchieve_S.png'), pygame.image.load('./resources/images/achievement/achieve_S.png')]
        self.achieveImage_L = [pygame.image.load('./resources/images/achievement/noAchieve_L.png'), pygame.image.load('./resources/images/achievement/achieve_L.png')]
        
        self.updown = [pygame.image.load('./resources/images/achievement/up.png'), pygame.image.load('./resources/images/achievement/down.png')]
        self.updown_S = [pygame.image.load('./resources/images/achievement/up_S.png'), pygame.image.load('./resources/images/achievement/down_S.png')]
        self.updown_L = [pygame.image.load('./resources/images/achievement/up_L.png'), pygame.image.load('./resources/images/achievement/down_L.png')]
        self.achieve_clear = [bool(int(self.config['Achievement']['singleclear'])), bool(int(self.config['Achievement']['stageaclear'])),
                            bool(int(self.config['Achievement']['stagebclear'])), bool(int(self.config['Achievement']['stagecclear'])),
                            bool(int(self.config['Achievement']['stagedclear'])), bool(int(self.config['Achievement']['stageallclear'])),
                            bool(int(self.config['Achievement']['in10turnwin'])), bool(int(self.config['Achievement']['onlynumbercardwin'])),
                            bool(int(self.config['Achievement']['onlyskillcardwin'])), bool(int(self.config['Achievement']['otherplayerunowin'])),
                            bool(int(self.config['Achievement']['grabover15card'])), bool(int(self.config['Achievement']['luckythree'])),
                            ]
        self.achieve_date = [self.config['date']['singleclear'], self.config['date']['stageaclear'],
                             self.config['date']['stagebclear'], self.config['date']['stagecclear'],
                             self.config['date']['stagedclear'], self.config['date']['stageallclear'],
                             self.config['date']['in10turnwin'], self.config['date']['onlynumbercardwin'],
                             self.config['date']['onlyskillcardwin'], self.config['date']['otherplayerunowin'],
                             self.config['date']['grabover15card'], self.config['date']['luckythree'],
        ]
        # 클리어 / 클리어 날짜 큐
        self.queue_clear = [bool(int(self.config['Achievement']['singleclear'])), bool(int(self.config['Achievement']['stageaclear'])),
                            bool(int(self.config['Achievement']['stagebclear'])),bool(int(self.config['Achievement']['stagecclear'])),]
        self.queue_clear_next = [bool(int(self.config['Achievement']['stagedclear'])), bool(int(self.config['Achievement']['stageallclear'])),
                            bool(int(self.config['Achievement']['in10turnwin'])), bool(int(self.config['Achievement']['onlynumbercardwin'])),
                            bool(int(self.config['Achievement']['onlyskillcardwin'])), bool(int(self.config['Achievement']['otherplayerunowin'])),
                            bool(int(self.config['Achievement']['grabover15card'])), bool(int(self.config['Achievement']['luckythree'])),]
        self.queue_date = [self.config['date']['singleclear'], self.config['date']['stageaclear'],
                             self.config['date']['stagebclear'], self.config['date']['stagecclear'],]
        self.queue_date_next = [self.config['date']['stagedclear'], self.config['date']['stageallclear'],
                             self.config['date']['in10turnwin'], self.config['date']['onlynumbercardwin'],
                             self.config['date']['onlyskillcardwin'], self.config['date']['otherplayerunowin'],
                             self.config['date']['grabover15card'], self.config['date']['luckythree'],]

        # 글씨
        self.items = ["Single Win", "Stage A Clear", "Stage B Clear", "Stage C Clear", "Stage D Clear",
                      "All Story Clear", "In 10 Truns Win", "Only NumberCard Win", "Only SkillCard Win", "Other Player UNO Win",
                      "Grab Over 15 Cards", "Lucky Three"]          # 12개
        self.queue_items = ["Single Win", "Stage A Clear", "Stage B Clear","Stage C Clear", ]
        self.queue_items_next = [ "Stage D Clear","All Story Clear", "In 10 Truns Win", "Only NumberCard Win", "Only SkillCard Win", "Other Player UNO Win",
                      "Grab Over 15 Cards", "Lucky Three",]
        self.queue_description = ['You must win the Single Player.', 'You must win Stage A.', 'You must win Stage B.','You must win Stage C.', ]
        self.queue_description_next = ['You must win Stage D.', 'You must win All Stages.',
                            'You must win in 10 turns.', 'You must win using only the Number Card.', 'You must win using only the Skill Card.',
                            'You must win after another player declares UNO.', 'You must grab more than 15 cards.', 'You must give three consecutive attack cards.',]
        self.description = ['You must win the Single Player.', 'You must win Stage A.', 'You must win Stage B.',
                            'You must win Stage C.', 'You must win Stage D.', 'You must win All Stages.',
                            'You must win in 10 turns.', 'You must win using only the Number Card.', 'You must win using only the Skill Card.',
                            'You must win after another player declares UNO.', 'You must grab more than 15 cards.', 'You must give three consecutive attack cards.'
                            ]
        # Clear the screen
        for i in range(3):
            if i+1 == int(self.config['window']['default']):
                self.screen.blit(self.backImage[i], (0, 0))

    def draw(self):
        for i in range(3):
            if i+1 == int(self.config['window']['default']):
                self.screen.blit(self.backImage[i], (0, 0))
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()
        self.window = int(self.config['window']['default'])
        
        if self.window == 1:
            # 업적 이미지
            for i in range(4):
                self.screen.blit(self.achieveImage_S[0] if not self.queue_clear[i] else self.achieveImage_S[1], (screenW // 20, screenH // 5 * i + 30))
            # BACK
            font = pygame.font.SysFont(None, 60).render("Back", True, (255, 255, 255) if self.current == 0 else (255, 0, 0))
            self.screen.blit(font, (screenW // 2 - font.get_width() // 2, screenH * 3.5 // 4))
            # 화살표
            self.screen.blit(self.updown_S[0], (710, 30))
            self.screen.blit(self.updown_S[1], (710, screenH // 3.4 * 2.35))
            # 업적 이름
            for i in range(4):
                text = pygame.font.SysFont(None, 40).render(self.queue_items[i] + ': ' + self.queue_date[i] if self.queue_clear[i] else self.queue_items[i], True, (255, 255, 20) if self.queue_clear[i] else (250, 250, 250))
                self.screen.blit(text, (screenW // 5, screenH // 5 * i + 60))
            # 업적 소개
            for i in range(4):
                text = pygame.font.SysFont(None, 30).render(self.queue_description[i], True, (250, 250, 250))
                self.screen.blit(text, (screenW // 5, screenH // 5 * i + 105))
        elif self.window == 2:
            # 업적 이미지
            for i in range(4):
                self.screen.blit(self.achieveImage[0] if not self.queue_clear[i] else self.achieveImage[1], (screenW // 20, screenH // 5 * i + 30))
            # BACK
            font = pygame.font.SysFont(None, 80).render("Back", True, (255, 255, 255) if self.current == 0 else (255, 0, 0))
            self.screen.blit(font, (screenW // 2 - font.get_width() // 2, screenH * 3.5 // 4))
            # 화살표
            self.screen.blit(self.updown[0], (890, 30))
            self.screen.blit(self.updown[1], (890, screenH // 3.4 * 2.35))
            # 업적 이름
            for i in range(4):
                text = pygame.font.SysFont(None, 50).render(self.queue_items[i] + ': ' + self.queue_date[i] if self.queue_clear[i] else self.queue_items[i], True, (255, 255, 20) if self.queue_clear[i] else (250, 250, 250))
                self.screen.blit(text, (screenW // 5, screenH // 5 * i + 60))
            # 업적 소개
            for i in range(4):
                text = pygame.font.SysFont(None, 30).render(self.queue_description[i], True, (250, 250, 250))
                self.screen.blit(text, (screenW // 5, screenH // 5 * i + 120))
        elif self.window == 3:
            # 업적 이미지
            for i in range(4):
                self.screen.blit(self.achieveImage_L[0] if not self.queue_clear[i] else self.achieveImage_L[1], (screenW // 20, screenH // 5 * i + 30))
            # BACK
            font = pygame.font.SysFont(None, 90).render("Back", True, (255, 255, 255) if self.current == 0 else (255, 0, 0))
            self.screen.blit(font, (screenW // 2 - font.get_width() // 2, screenH * 3.5 // 4))
            # 화살표
            self.screen.blit(self.updown_L[0], (1100, 30))
            self.screen.blit(self.updown_L[1], (1100, screenH // 3.4 * 2.35))
            # 업적 이름
            for i in range(4):
                text = pygame.font.SysFont(None, 60).render(self.queue_items[i] + ': ' + self.queue_date[i] if self.queue_clear[i] else self.queue_items[i], True, (255, 255, 20) if self.queue_clear[i] else (250, 250, 250))
                self.screen.blit(text, (screenW // 5, screenH // 5 * i + 70))
            # 업적 소개
            for i in range(4):
                text = pygame.font.SysFont(None, 48).render(self.queue_description[i], True, (250, 250, 250))
                self.screen.blit(text, (screenW // 5, screenH // 5 * i + 140))
        

        

    def run(self):
        clock = pygame.time.Clock()
        screenW = self.screen.get_width()
        screenH = self.screen.get_height()

        while True:
            # Handle events
            self.window = int(self.config['window']['default'])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == self.keys["ESCAPE"]:
                        pygame.quit()
                        sys.exit()

                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and self.queue_items[0] != 'Single Win':
                        # 마우스 휠을 위로 굴릴 때
                        self.queue_items_next.insert(0, self.queue_items.pop())
                        self.queue_items.insert(0, self.queue_items_next.pop())

                        self.queue_description_next.insert(0, self.queue_description.pop())
                        self.queue_description.insert(0, self.queue_description_next.pop())

                        self.queue_clear_next.insert(0, self.queue_clear.pop())
                        self.queue_clear.insert(0, self.queue_clear_next.pop())

                        self.queue_date_next.insert(0, self.queue_date.pop())
                        self.queue_date.insert(0, self.queue_date_next.pop())

                    elif event.button == 5 and self.queue_items[len(self.queue_items) - 1] != 'Lucky Three':
                        # 마우스 휠을 아래로 굴릴 때
                        self.queue_items_next.append(self.queue_items.pop(0))
                        self.queue_items.append(self.queue_items_next.pop(0))

                        self.queue_description_next.append(self.queue_description.pop(0))
                        self.queue_description.append(self.queue_description_next.pop(0))

                        self.queue_clear_next.append(self.queue_clear.pop(0))
                        self.queue_clear.append(self.queue_clear_next.pop(0))

                        self.queue_date_next.append(self.queue_date.pop(0))
                        self.queue_date.append(self.queue_date_next.pop(0))

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.window == 1:
                        text = pygame.font.SysFont(None, 60).render("Back", True, (255, 255, 255))
                    elif self.window == 2:
                        text = pygame.font.SysFont(None, 80).render("Back", True, (255, 255, 255))
                    elif self.window == 3:
                        text = pygame.font.SysFont(None, 90).render("Back", True, (255, 255, 255))

                    text_rect = text.get_rect()
                    text_rect.topleft = (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() * 3.5 // 4)
                    if text_rect.collidepoint(pos):
                        if event.type == MOUSEMOTION:
                            self.current = 1
                        if event.type == MOUSEBUTTONUP:
                            print("Go Back click!")
                            if self.current == 1:
                                self.screen.fill((0, 0, 0))
                                self.current = 0
                                return 0
                
            # Draw the menu
            self.draw()
            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)
