import pygame
import constants
import classes


def generate_level(level_map: list, tile_group: pygame.sprite.Group, player_group: pygame.sprite.Group,
                   all_sprites: pygame.sprite.Group) -> tuple:
    '''

    :param level_map: двумерный список - карта уровня
    :param tile_group: группа тайлов
    :param player_group: группа игрока
    :param all_sprites: группа всех спрайтов
    :return: экземпляр класса classes.Player, ширину и высоту уровня
    '''

    new_player = None

    # циклом проходимся по всем элементам карты, создавая спрайты
    for y in range(len(level_map)):

        for x in range(len(level_map[y])):

            if level_map[y][x] == '1':
                classes.BaseBlock(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT, tile_group, all_sprites)

            elif level_map[y][x] == '0':
                # TODO: добавить спрайт пустоты
                pass

            elif level_map[y][x] == '2':
                # TODO: добавить спрайт пустоты
                new_player = classes.Player(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT, player_group,
                                            all_sprites)

    return new_player, x, y
