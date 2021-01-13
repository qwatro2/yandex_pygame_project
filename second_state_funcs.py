import pygame
import constants
import classes


def generate_level(level_map: list, tile_group: pygame.sprite.Group, player_group: pygame.sprite.Group,
                   checkpoints_group: pygame.sprite.Group, die_blocks_group: pygame.sprite.Group,
                   monsters_group: pygame.sprite.Group, all_sprites: pygame.sprite.Group) -> tuple:
    '''
    :param level_map: двумерный список - карта уровня
    :param tile_group: группа тайлов
    :param player_group: группа игрока
    :param all_sprites: группа всех спрайтов
    :return: экземпляр класса classes.Player, ширину и высоту уровня
    '''

    new_player, x, y = [None] * 3
    player_x, player_y = None, None

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
                player_x = x
                player_y = y

            elif level_map[y][x] == '3':
                # TODO: добавить спрайт пустоты
                classes.Checkpoint(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT, checkpoints_group,
                                   all_sprites)

            elif level_map[y][x] == '4':
                classes.DieBlock(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT, die_blocks_group,
                                 all_sprites)

            elif level_map[y][x] == '5':
                classes.BaseMonster(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT,
                                    constants.MONSTER_SPEED_X, constants.TILE_WIDTH * 5,
                                    monsters_group, all_sprites)

    new_player = classes.Player(player_x * constants.TILE_WIDTH, player_y * constants.TILE_HEIGHT,
                                player_group, all_sprites)

    return new_player, x, y


def camera_configure(camera, target_rect) -> pygame.Rect:
    left, top, _, _ = target_rect
    _, _, w, h = camera
    left, top = -left + constants.WIDTH // 2, -top + constants.HEIGHT // 2

    left = min(0, left)  # камера не движется дальше левой границы
    left = max(-(camera.width - constants.WIDTH), left)  # камера не движется дальше правой границы
    top = max(-(camera.height - constants.HEIGHT), top)  # камера не движется дальше нижней границы
    top = min(0, top)  # камера не движется дальше верхней границы

    return pygame.Rect(left, top, w, h)
