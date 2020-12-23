import pygame
import funcs
import classes

if __name__ == '__main__':

    # инициализация библиотеки pygame
    pygame.init()

    # инициализация констант игры
    width = 800
    height = 600
    game_loop = True
    screen = pygame.display.set_mode((width, height))
    all_sprites = pygame.sprite.Group()

    # TODO: изменить заголовок и иконку игры
    pygame.display.set_caption('caption')

    # игровой цикл
    while game_loop:

        # обработка событий
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_loop = False

        # обновление всех спрайтов
        all_sprites.update()

        # отрисовка всех спрайтов
        all_sprites.draw(screen)

        pygame.display.flip()

    # закрытие библиотеки pygame
    pygame.quit()
