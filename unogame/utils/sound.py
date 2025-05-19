import pygame
import os

def playMusic(num): #배경음악 재생
    pygame.mixer.init() #mixer 초기화
    path = os.getcwd() #원래 작업 디렉토리 임시 저장
    module_path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(module_path+"/../resources/music") #파일 경로 탐색 용이하게 한번 바꾸기

    pygame.mixer.music.stop()
    pygame.mixer.music.load("music"+str(num)+".mp3")
    pygame.mixer.music.play(-1) #반복재생
    os.chdir(path) # 경로 원위치

def pauseMusic(): #배경음악 일시정지
    pygame.mixer.music.pause()
def unpauseMusic(): #배경음악 다시 재생
    pygame.mixer.music.unpause()

def musicDown():
    currentVol = getMusicVol()
    pygame.mixer.music.set_volume((currentVol-1)/10)
    if pygame.mixer.music.get_volume() <= 0.05: pygame.mixer.music.set_volume(0)
def musicUp():
    currentVol = getMusicVol()
    pygame.mixer.music.set_volume((currentVol+1)/10)
def getMusicVol(): #floating-point error mitigation
    vol = (pygame.mixer.music.get_volume() + 0.04) * 10 // 1
    return int(vol)
def resetMusicVol():
    pygame.mixer.music.set_volume(0.6)

class SoundFX:
    def __init__(self) :
        pygame.mixer.init() #mixer 초기화
        path = os.getcwd() #원래 작업 디렉토리 임시 저장
        module_path = os.path.abspath(os.path.dirname(__file__)) 
        os.chdir(module_path+"/../resources/sounds") #파일 경로 탐색 용이하게 한번 바꾸기

        self.soundEffects = [
            pygame.mixer.Sound("short_blip.mp3"),
            pygame.mixer.Sound("coin.mp3"),
            pygame.mixer.Sound("bleep.mp3"),
            pygame.mixer.Sound("flipcard.mp3"),
            pygame.mixer.Sound("winsquare.mp3")
        ]

        os.chdir(path) # 경로 원위치
        print(os.getcwd())

        for sound in self.soundEffects:
            sound.set_volume(0.2)
    
    def soundPlay(self, num):
        self.soundEffects[num-1].play()
    def soundIni(self, config): # 저장된 소리 크기로 불러오기
        pygame.mixer.music.set_volume(int(config['sound']['music']) / 10)
        for sound in self.soundEffects:
            sound.set_volume(int(config['sound']['sound']) / 10)
    
    def soundDown(self):
        currentVol = self.getSoundVol()
        set = (currentVol-1)/10
        if currentVol <= 0.05: set = 0
        for sound in self.soundEffects:
            sound.set_volume(set)
        self.soundPlay(1)
    def soundUp(self):
        currentVol = self.getSoundVol()
        set = (currentVol+1)/10
        for sound in self.soundEffects:
            sound.set_volume(set)
        self.soundPlay(1)
    def getSoundVol(self): #floating-point error mitigation
        vol = (self.soundEffects[0].get_volume() + 0.04) * 10 // 1
        return int(vol)
    def resetSoundVol(self):
        for sound in self.soundEffects:
            sound.set_volume(0.2)
        self.soundPlay(1)
