import pygame

if __name__ == '__main__':
    # инициализация библиотеки pygame
    pygame.init()

    # инициализация констант игры
    width = 800
    height = 600
    game_loop = True
    screen = pygame.display.set_mode((width, height))

    # TODO: изменить заголовок и иконку игры
    pygame.display.set_caption('caption')

    # игровой цикл
    while game_loop:

        # обработка событий
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_loop = False

    # закрытие библиотеки pygame
    pygame.quit()
