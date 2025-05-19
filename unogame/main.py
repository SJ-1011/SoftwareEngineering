import pygame, configparser
import sys
from pygame.locals import *
from utils import *
# from single_play import start_single_play
from single_play import Game
import urllib.request
from utils.multiMenu import multiPlayMenu


config = configparser.ConfigParser()
config.read("setting_data.ini")


# Define the key_list
key_list = {
    "LEFT": int(config["key"]["left"]),
    "RIGHT": int(config["key"]["right"]),
    "UP": int(config["key"]["up"]),
    "DOWN": int(config["key"]["down"]),
    "RETURN": int(config["key"]["return"]),
    "ESCAPE": int(config["key"]["escape"]),
}


# Initialize pygame
pygame.init()

if config["window"]["default"] == "1":
    screen = pygame.display.set_mode((800, 600))
elif config["window"]["default"] == "2":
    screen = pygame.display.set_mode((1000, 750))
elif config["window"]["default"] == "3":
    screen = pygame.display.set_mode((1280, 960))


font = pygame.font.SysFont(None, 48)
soundFX = sound.SoundFX()
soundFX.soundIni(config)
sound.playMusic(1)

# Create the menu
menu = menu.Menu(key_list, font, screen, config)
multiplay = multiMenu.multiPlayMenu(key_list, font, screen, config, soundFX)
setting = settings.Setting(key_list, font, screen, soundFX, config)
storyModess = storyMode.StoryModes(screen, font, config, key_list, soundFX)
achieve = achieveMenu.achieveMenu(key_list, font, screen, config, soundFX)

# Main loop
while True:
    selected = menu.run()
    # Handle the selected menu item
    if selected == 0:
        # Start single player game
        print("Start Game")  # Replace with your game code
        soundFX.soundPlay(1)
        game = Game(screen, key_list, config, soundFX)
        selected = game.start_single_play()

    elif selected == 1:
        print("start MultiPlay")
        selected = multiplay.run()


    elif selected == 2:
        soundFX.soundPlay(1)
        screen.fill((0, 0, 0))
        selected = storyModess.run()

    elif selected == 3:
        selected = achieve.run()

    elif selected == 4:
        # Open settings menu
        soundFX.soundPlay(1)
        screen.fill((0, 0, 0))
        selected = setting.run()
    elif selected == 5:
        # Exit the program
        soundFX.soundPlay(1)
        pygame.quit()
        sys.exit()
