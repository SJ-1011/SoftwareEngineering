import pygame

pygame.init()

screen_width = 640
screen_height = 480
scroll_amount = 20

font = pygame.font.SysFont('Arial', 20)
text_color = (255, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))

num_rows = 100
row_height = 30
row_spacing = 10

scroll_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                # 마우스 휠을 위로 굴릴 때
                scroll_y += scroll_amount
            elif event.button == 5:
                # 마우스 휠을 아래로 굴릴 때
                scroll_y -= scroll_amount

    screen.fill((0, 0, 0))

    # 스크롤 위치에 따라 숫자 위치 변경
    for i in range(num_rows):
        y = i * (row_height + row_spacing) - scroll_y
        if y + row_height < 0:
            continue
        if y > screen_height:
            break
        text = font.render(str(i), True, text_color)
        text_rect = text.get_rect()
        text_rect.left = 10
        text_rect.top = y
        screen.blit(text, text_rect)

    pygame.display.flip()
