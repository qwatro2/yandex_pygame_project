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
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    left, right, up = [False] * 3

    # TODO: изменить заголовок и иконку игры
    pygame.display.set_caption('caption')

    # генерация уровня
    level_map = first_state_funcs.load_level('test_level.txt')
    player, level_width, level_height = second_state_funcs.generate_level(level_map, tile_group, player_group,
                                                                          all_sprites)

    # игровой цикл
    while game_loop:

        # обработка событий
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_loop = False

            elif event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    left = True

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    right = True

                if event.key == pygame.K_SPACE:
                    up = True

            elif event.type == pygame.KEYUP:

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    left = False

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    right = False

                if event.key == pygame.K_SPACE:
                    up = False

        # обновление всех спрайтов
        all_sprites.update(left, right, up, tile_group)

        # отрисовка всех спрайтов
        screen.fill('white')
        all_sprites.draw(screen)

        clock.tick(constants.FPS)
        pygame.display.flip()

    # закрытие библиотеки pygame
    pygame.quit()
