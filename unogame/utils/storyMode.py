import pygame, configparser
import sys
from pygame.locals import *
from single_play import Game
from utils import menu, settings, sound, stageA, stageC, stageD, stageB
import pygame, configparser
import sys
from pygame.locals import *
from single_play import Game

class StoryModes:

    def __init__(self, screen, font, config, key, soundFX):
        self.screen = screen                                                        # 게임의 스크린
        self.soundFX = soundFX
        self.current_stage = 0                                                      # 현재 커서의 가로 위치
        self.config = config
        self.stages = ['stageA', 'stageB', 'stageC', 'stageD']
        self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])),
                            bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4']))]
        self.stage_open = [bool(int(self.config['open']['stage1'])), bool(int(self.config['open']['stage2'])),
                            bool(int(self.config['open']['stage3'])), bool(int(self.config['open']['stage4']))]
        self.key = key
        self.window = int(self.config['window']['default'])
        self.visible = 'main'

        # 노멀 사이즈 이미지
        self.background = [pygame.image.load('./resources/images/storymode/stageA.png'), pygame.image.load('./resources/images/storymode/stageB.png'),
                           pygame.image.load('./resources/images/storymode/stageC.png'), pygame.image.load('./resources/images/storymode/stageD.png')]
        self.memo = [pygame.image.load('./resources/images/storymode/memoA.png'), pygame.image.load('./resources/images/storymode/memoB.png'),
                    pygame.image.load('./resources/images/storymode/memoC.png'), pygame.image.load('./resources/images/storymode/memoD.png')]
        self.check = pygame.image.load('./resources/images/storymode/check.png')
        self.game_start = pygame.image.load('./resources/images/storymode/gamestart.png')

        # 스몰 사이즈 이미지
        self.background_S = [pygame.image.load('./resources/images/storymode/stageA_S.png'), pygame.image.load('./resources/images/storymode/stageB_S.png'),
                           pygame.image.load('./resources/images/storymode/stageC_S.png'), pygame.image.load('./resources/images/storymode/stageD_S.png')]
        self.memo_S = [pygame.image.load('./resources/images/storymode/memoA_S.png'), pygame.image.load('./resources/images/storymode/memoB_S.png'),
                    pygame.image.load('./resources/images/storymode/memoC_S.png'), pygame.image.load('./resources/images/storymode/memoD_S.png')]
        self.check_S = pygame.image.load('./resources/images/storymode/check_S.png')
        self.game_start_S = pygame.image.load('./resources/images/storymode/gamestart_S.png')

        # 라지 사이즈 이미지
        self.background_L = [pygame.image.load('./resources/images/storymode/stageA_L.png'), pygame.image.load('./resources/images/storymode/stageB_L.png'),
                           pygame.image.load('./resources/images/storymode/stageC_L.png'), pygame.image.load('./resources/images/storymode/stageD_L.png')]
        self.memo_L = [pygame.image.load('./resources/images/storymode/memoA_L.png'), pygame.image.load('./resources/images/storymode/memoB_L.png'),
                    pygame.image.load('./resources/images/storymode/memoC_L.png'), pygame.image.load('./resources/images/storymode/memoD_L.png')]
        self.check_L = pygame.image.load('./resources/images/storymode/check_L.png')
        self.game_start_L = pygame.image.load('./resources/images/storymode/gamestart_L.png')


        self.ratio = 1
        
        self.latestClear = 0                                # 제일 마지막으로 깬 단계

        for i in range(4):
            if self.stage_clear[i] == False:
                self.latestClear = i
                break
        
        self.window = int(self.config['window']['default'])

        # small
        if self.window == 1:
            self.x0, self.x1, self.x2, self.x3 = 100.0, 233.6, 456.0, 676.8
            self.y0, self.y1, self.y2, self.y3 = 150.4, 280.0, 158.4, 208.0
            self.back_x, self.back_y = 22.4, 532.8
            self.gameStart_x, self.gameStart_y = 85.6, 378.4
            self.gameStartW, self.gameStartH = 151.2, 91.2
            self.backW, self.backH = 80, 40
            self.memo_x, self.memo_y = 521.6, 400.8
            self.start_x, self.start_y = 172, 424
            self.screen.blit(self.background_S[self.latestClear], (0, 0))
        # middle
        elif self.window == 2:
            self.x0, self.x1, self.x2, self.x3 = 125, 292, 570, 846
            self.y0, self.y1, self.y2, self.y3 = 188, 350, 198, 260
            self.back_x, self.back_y = 28, 666
            self.gameStart_x, self.gameStart_y = 107, 473
            self.gameStartW, self.gameStartH = 216, 114
            self.backW, self.backH = 100, 50
            self.memo_x, self.memo_y = 652, 501
            self.start_x, self.start_y = 215, 530
            self.screen.blit(self.background[self.latestClear], (0, 0))
        # large
        elif self.window == 3:
            self.x0, self.x1, self.x2, self.x3 = 160.0, 373.76, 729.6, 1082.9
            self.y0, self.y1, self.y2, self.y3 = 240.6, 448.0, 253.4, 332.8
            self.back_x, self.back_y = 35.8, 852.5
            self.gameStart_x, self.gameStart_y = 137, 605.4
            self.gameStartW, self.gameStartH = 276.5, 145.9
            self.backW, self.backH = 128, 64
            self.memo_x, self.memo_y = 834.6, 641.3
            self.start_x, self.start_y = 275.2, 678.4
            self.screen.blit(self.background_L[self.latestClear], (0, 0))

        self.radius = 40
        self.x_pos_list = [self.x0, self.x1, self.x2, self.x3]
        self.y_pos_list = [self.y0, self.y1, self.y2, self.y3]

        
    def draw(self):

        # 배경화면
        for i in range(4):
            if self.stage_clear[i] == False:
                self.latestClear = i
                break
            elif self.stage_clear[3] == True:
                self.latestClear = 3
                
        self.window = int(self.config['window']['default'])
        # small
        if self.window == 1:
            self.x0, self.x1, self.x2, self.x3 = 100.0, 233.6, 456.0, 676.8
            self.y0, self.y1, self.y2, self.y3 = 150.4, 280.0, 158.4, 208.0
            self.back_x, self.back_y = 22.4, 532.8
            self.gameStart_x, self.gameStart_y = 85.6, 378.4
            self.gameStartW, self.gameStartH = 151.2, 91.2
            self.backW, self.backH = 80, 40
            self.memo_x, self.memo_y = 521.6, 400.8
            self.start_x, self.start_y = 172, 424
            self.screen.blit(self.background_S[self.latestClear], (0, 0))
            self.x_pos_list = [self.x0, self.x1, self.x2, self.x3]
            self.y_pos_list = [self.y0, self.y1, self.y2, self.y3]
            # 체크 표시
            for i in range(4):
                if self.stage_clear[i] == True:
                    self.screen.blit(self.check_S, (self.x_pos_list[i] - self.check_S.get_width() // 2, self.y_pos_list[i] - self.check_S.get_height() // 2.3))
            # 게임 시작, 메모 표시
            if self.visible != 'main':
                self.screen.blit(self.memo_S[self.visible], (self.memo_x - self.memo_S[self.visible].get_width() // 2, self.memo_y - self.memo_S[self.visible].get_height() // 2))
                self.screen.blit(self.game_start_S, (self.start_x - self.game_start_S.get_width() // 2, self.start_y - self.game_start_S.get_height() // 2))  


        # middle
        elif self.window == 2:
            self.x0, self.x1, self.x2, self.x3 = 125, 292, 570, 846
            self.y0, self.y1, self.y2, self.y3 = 188, 350, 198, 260
            self.back_x, self.back_y = 28, 666
            self.gameStart_x, self.gameStart_y = 107, 473
            self.gameStartW, self.gameStartH = 216, 114
            self.backW, self.backH = 100, 50
            self.memo_x, self.memo_y = 652, 501
            self.start_x, self.start_y = 215, 530
            self.screen.blit(self.background[self.latestClear], (0, 0))
            self.x_pos_list = [self.x0, self.x1, self.x2, self.x3]
            self.y_pos_list = [self.y0, self.y1, self.y2, self.y3]
            # 체크 표시
            for i in range(4):
                if self.stage_clear[i] == True:
                    self.screen.blit(self.check, (self.x_pos_list[i] - self.check.get_width() // 2, self.y_pos_list[i] - self.check.get_height() // 2.3))
            # 게임 시작, 메모 표시
            if self.visible != 'main':
                self.screen.blit(self.memo[self.visible], (self.memo_x - self.memo[self.visible].get_width() // 2, self.memo_y - self.memo[self.visible].get_height() // 2))
                self.screen.blit(self.game_start, (self.start_x - self.game_start.get_width() // 2, self.start_y - self.game_start.get_height() // 2))  


        # large
        elif self.window == 3:
            self.x0, self.x1, self.x2, self.x3 = 160.0, 373.76, 729.6, 1082.9
            self.y0, self.y1, self.y2, self.y3 = 240.6, 448.0, 253.4, 332.8
            self.back_x, self.back_y = 35.8, 852.5
            self.gameStart_x, self.gameStart_y = 137, 605.4
            self.gameStartW, self.gameStartH = 276.5, 145.9
            self.backW, self.backH = 128, 64
            self.memo_x, self.memo_y = 834.6, 641.3
            self.start_x, self.start_y = 275.2, 678.4
            self.screen.blit(self.background_L[self.latestClear], (0, 0))
            self.x_pos_list = [self.x0, self.x1, self.x2, self.x3]
            self.y_pos_list = [self.y0, self.y1, self.y2, self.y3]
            # 체크 표시
            for i in range(4):
                if self.stage_clear[i] == True:
                    self.screen.blit(self.check_L, (self.x_pos_list[i] - self.check_L.get_width() // 2, self.y_pos_list[i] - self.check_L.get_height() // 2.3))
            # 게임 시작, 메모 표시
            if self.visible != 'main':
                self.screen.blit(self.memo_L[self.visible], (self.memo_x - self.memo_L[self.visible].get_width() // 2, self.memo_y - self.memo_L[self.visible].get_height() // 2))
                self.screen.blit(self.game_start_L, (self.start_x - self.game_start_L.get_width() // 2, self.start_y - self.game_start_L.get_height() // 2))  

    def run(self):
        # 메인 루프
        clock = pygame.time.Clock()
        running = True
        while running:
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                elif event.type == MOUSEMOTION or MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    back_rect = pygame.Rect(self.back_x, self.back_y, self.backW, self.backH)
                    if back_rect.collidepoint(pos):
                        if event.type == MOUSEBUTTONUP:
                            print("Go Back click!")
                            self.visible = 'main'
                            return 0
                    for i in range(4):
                        circle_rect = pygame.Rect(self.x_pos_list[i] - self.radius, self.y_pos_list[i] - self.radius, self.radius * 2, self.radius * 2)
                        if circle_rect.collidepoint(pos) and self.stage_open[i]:
                            if event.type == MOUSEMOTION:
                                self.current_stage = i
                            elif event.type == MOUSEBUTTONUP:
                                print(f"{self.stages[self.current_stage]} click!")
                                self.visible = self.current_stage
                    
                    if self.visible != 'main':
                        start_rect = pygame.Rect(self.gameStart_x, self.gameStart_y, self.gameStartW, self.gameStartH)
                        if start_rect.collidepoint(pos):
                            if event.type == MOUSEBUTTONUP:
                                print(f"{self.stages[self.current_stage]} start!")
                                if self.current_stage == 0:             # 스테이지 A 선택 + Play
                                    print("임의로 게임 clear")
                                    stage = stageA.stage_A(self.screen, self.key, self.config, self.soundFX)
                                    win = stage.start_single_play()
                                    if win != 0:
                                        return
                                    
                                elif self.current_stage == 1:          # 스테이지 B 선택 + Play
                                    print("임의로 게임 clear")
                                    stage = stageB.stage_B(self.screen, self.key, self.config, self.soundFX)
                                    win = stage.start_single_play()
                                    if win != 0:
                                        return

                                elif self.current_stage == 2:          # 스테이지 C 선택 + Play
                                    print("임의로 게임 clear")
                                    stage = stageC.stage_C(self.screen, self.key, self.config, self.soundFX)
                                    win = stage.start_single_play()
                                    if win != 0:
                                        return

                                elif self.current_stage == 3:          # 스테이지 D 선택 + Play
                                    print("임의로 게임 clear")
                                    stage = stageD.stage_D(self.screen, self.key, self.config, self.soundFX)
                                    win = stage.start_single_play()
                                    if win != 0:
                                        return
                                
                                self.config['clear'][f'stage{self.current_stage + 1}'] = '1'
                                self.config['open'][f'stage{self.current_stage + 2}'] = '1'
                                with open('setting_data.ini', 'w') as f:
                                    self.config.write(f)
                                self.stage_clear = [bool(int(self.config['clear']['stage1'])), bool(int(self.config['clear']['stage2'])), bool(int(self.config['clear']['stage3'])), bool(int(self.config['clear']['stage4']))]
                                self.stage_open = [bool(int(self.config['open']['stage1'])), bool(int(self.config['open']['stage2'])), bool(int(self.config['open']['stage3'])), bool(int(self.config['open']['stage4']))]
                                
                                self.visible = 'main'
                                return
            
            # 화면 채우기
            self.draw()
            
            # Update the screen
            pygame.display.update()

            # Limit the frame rate
            clock.tick(60)