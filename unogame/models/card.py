import pygame


class Card:
    colors = ["red", "blue", "green", "yellow"]
    numbers = list(range(0, 10))
    skills = ["reverse", "block", "plus2", "change", "plus4"]

    def __init__(self, color, number, skill, wild, config):
        self.color = color
        self.number = number
        self.skill = skill  # block, plus2, reverse, change / change, plus4
        self.is_moving = False
        self.is_wild = wild
        self.file_path = ""
        self.width = 50
        self.height = 70
        self.config = config

        if self.config["color"]["default"] == str(2):  # 색맹모드 none
            if number is not None:  # 숫자카드
                self.file_path = f"resources/images/card/normalMode/{number}/{self.color}_{number}.png"
            elif (
                color is not None and number is None and skill is not None and self.skill not in ["all", "all4"]
            ):  # 색깔있는 스킬카드
                self.file_path = (
                    f"resources/images/card/normalMode/{skill}/{self.color}_{skill}.png"
                )
            elif color is None:
                if skill == "all":  # 색 바꾸는 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/change/all_change.png"
                    )
                elif skill == "all4":  # 공격 wild 카드
                    self.file_path = f"resources/images/card/normalMode/plus4/all_plus4.png"
            else:
                print("path error")

        elif self.config["color"]["default"] == str(0):  # 색맹모드 RG
            if number is not None:  # 숫자카드
                self.file_path = (
                    f"resources/images/card/RG/{number}/{self.color}_{number}.png"
                )
            elif (
                color is not None and number is None and skill is not None and self.skill not in ["all", "all4"]
            ):  # 색깔있는 스킬카드
                self.file_path = f"resources/images/card/RG/{skill}/{self.color}_{skill}.png"
            elif color is None:
                if skill == "all":  # 색 바꾸는 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/change/all_change.png"
                    )
                elif skill == "all4":  # 공격 wild 카드
                    self.file_path = f"resources/images/card/normalMode/plus4/all_plus4.png"

        elif self.config["color"]["default"] == str(1):
            if number is not None:  # 숫자카드
                self.file_path = (
                    f"resources/images/card/YB/{number}/{self.color}_{number}.png"
                )
            elif (
                color is not None and number is None and skill is not None and self.skill not in ["all", "all4"]
            ):  # 색깔있는 스킬카드
                self.file_path = f"resources/images/card/YB/{skill}/{self.color}_{skill}.png"
            elif color is None:
                if skill == "all":  # 색 바꾸는 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/change/all_change.png"
                    )
                elif skill == "all4":  # 공격 wild 카드
                    self.file_path = f"resources/images/card/normalMode/plus4/all_plus4.png"

        image_surface = pygame.image.load(self.file_path).convert_alpha()
        # image_surface = pygame.transform.rotozoom(image_surface, 0, 0.5)
        self.large_image_surface = pygame.transform.scale(
            image_surface, (self.width, self.height)
        )
        self.small_image_surface = pygame.transform.scale(
            image_surface, (self.width / 2, self.height / 2)
        )

        self.image = self.large_image_surface
        self.rect = self.image.get_rect(center=(0, 0))
        # print(f"width : {self.rect.width} / height : {self.rect.height}")
        self.initial_y = self.rect.y

        self.card_state = False  # 앞뒷면을 나타내는 변수, True = 앞면 / False = 뒷면

    # def draw_now_select(self, screen):
    def change_path(self, new_config):
        if new_config["color"]["default"] == '2':  # 색맹모드 none
            if self.number is not None:  # 숫자카드
                self.file_path = f"resources/images/card/normalMode/{self.number}/{self.color}_{self.number}.png"
            elif (
                self.color is not None
                and self.number is None
                and self.skill is not None
                and self.skill not in ["all", "all4"]
            ):  # 색깔있는 스킬카드
                self.file_path = f"resources/images/card/normalMode/{self.skill}/{self.color}_{self.skill}.png"
            elif self.color is None:
                if self.skill == "all":  # 색 바꾸는 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/change/all_change.png"
                    )
                elif self.skill == "all4":  # 공격 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/plus4/all_plus4.png"
                    )
            else:
                print("path error")

        elif new_config["color"]["default"] == '0':  # 색맹모드 RG
            if self.number is not None:  # 숫자카드
                self.file_path = f"resources/images/card/RG/{self.number}/{self.color}_{self.number}.png"
            elif (
                self.color is not None
                and self.number is None
                and self.skill is not None
                and self.skill not in ["all", "all4"]
            ):  # 색깔있는 스킬카드
                self.file_path = f"resources/images/card/RG/{self.skill}/{self.color}_{self.skill}.png"
            elif self.color is None:
                if self.skill == "all":  # 색 바꾸는 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/change/all_change.png"
                    )
                elif self.skill == "all4":  # 공격 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/plus4/all_plus4.png"
                    )

        elif new_config["color"]["default"] == '1':
            if self.number is not None:  # 숫자카드
                self.file_path = f"resources/images/card/YB/{self.number}/{self.color}_{self.number}.png"
            elif (
                self.color is not None
                and self.number is None
                and self.skill is not None
                and self.skill not in ["all", "all4"]
            ):  # 색깔있는 스킬카드
                self.file_path = f"resources/images/card/YB/{self.skill}/{self.color}_{self.skill}.png"
            elif self.color is None:
                if self.skill == "all":  # 색 바꾸는 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/change/all_change.png"
                    )
                elif self.skill == "all4":  # 공격 wild 카드
                    self.file_path = (
                        f"resources/images/card/normalMode/plus4/all_plus4.png"
                    )

        image_surface = pygame.image.load(self.file_path).convert_alpha()
        # image_surface = pygame.transform.rotozoom(image_surface, 0, 0.5)
        self.large_image_surface = pygame.transform.scale(
            image_surface, (self.width, self.height)
        )
        self.small_image_surface = pygame.transform.scale(
            image_surface, (self.width / 2, self.height / 2)
        )

        self.image = self.large_image_surface
        self.rect = self.image.get_rect(center=(0, 0))
