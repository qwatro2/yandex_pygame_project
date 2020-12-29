import pygame
import constants
import first_state_funcs
import second_state_funcs
import classes

if __name__ == '__main__':

    # инициализация библиотеки pygame
    pygame.init()

    # инициализация констант игры
    game_loop = True
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    all_sprites = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    # TODO: изменить заголовок и иконку игры
    pygame.display.set_caption('caption')

    # генерация уровня
    level_map = first_state_funcs.load_level('test_level.txt')
    player = second_state_funcs.generate_level(level_map, tile_group, player_group, all_sprites)
    screen.fill('white')

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
