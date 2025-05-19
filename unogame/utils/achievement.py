import datetime
import pygame

#config  = configparser.ConfigParser()
#config.read("../setting_data.ini")
class achievement:
    def __init__(self, config):
        self.message = "Default"
        self.messages = [
            "Achievement Unlocked: Single Mode Clear",
            "Achievement Unlocked: Stage A Clear",
            "Achievement Unlocked: Stage D Clear",
            "Achievement Unlocked: Stage C Clear",
            "Achievement Unlocked: Stage D Clear",
            "Achievement Unlocked: Stage All Clear",
            "Achievement Unlocked: In 10 Turn Win",
            "Achievement Unlocked: Only Number Card Win",
            "Achievement Unlocked: Only Skill Card Win",
            "Achievement Unlocked: Other Player UNO Win",
            "Achievement Unlocked: Grab Over 15 Card",
            "Achievement Unlocked: Lucky Three"
        ]
        self.visible = False
        self.timer_started = False
        self.timer_start_time = 0
        self.x = 5
        self.y = 5

        #config = configparser.ConfigParser()
        #config.read("../setting_data.ini")
        self.config = config
        self.configKeys = list(self.config["Achievement"].keys())
        self.dateKeys = list(self.config["date"].keys())
        self.font = pygame.font.SysFont(None, 48)

    def showMessage(self):
        self.visible = True
        self.timer_started = True
        self.timer_start_time = pygame.time.get_ticks()

    def hideMessage(self):
        self.visible = False

    def update(self, screen):
        if self.visible:
            # Draw the achievement message
            text = self.font.render(self.message, True, (255, 255, 255))
            surface = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            surface.fill((0,0,0))
            surface.set_alpha(128)
            screen.blit(surface, (self.x, self.y))
            screen.blit(text, (self.x, self.y))
            # Move the message upward
            if self.y > -50 and self.tickCalcular(self.timer_start_time) > 1500:
                self.y -= 1
            # Check if the timer has expired
            if self.timer_started and self.tickCalcular(self.timer_start_time) > 3000:
                self.hideMessage()
                self.timer_started = False
                self.y = 20

    def tickCalcular(self, ticks):
        return pygame.time.get_ticks() - ticks

    def accomplish(self, index):
        self.message = self.messages[index]
        date = str(datetime.date.today())
        self.config["date"][self.dateKeys[index]] = date
        self.config["Achievement"][self.configKeys[index]] = "1"
        with open('setting_data.ini', 'w') as f:
            self.config.write(f)
        self.showMessage()
