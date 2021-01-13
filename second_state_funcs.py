import pygame
import constants
import classes


def generate_level(level_map: list, entities: list, sprite_groups: dict) -> tuple:
    new_player, x, y = [None] * 3

    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '0':
                # TODO: спрайт пустоты
                pass
            elif level_map[y][x] == '1':
                classes.BaseBlock(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT,
                                  sprite_groups['tiles'], sprite_groups['all'])
            elif level_map[y][x] == '2':
                classes.DieBlock(x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT,
                                 sprite_groups['traps'], sprite_groups['all'])

    for entity in entities:
        if entity['name'] == 'player':
            new_player = classes.Player(entity['x'], entity['y'], entity['hp'], entity['blocks'],
                                        sprite_groups['player'], sprite_groups['all'])
        elif entity['name'] == 'enemy':
            classes.BaseMonster(entity['x'], entity['y'], entity['v'], entity['max'], entity['hp'],
                                sprite_groups['monsters'], sprite_groups['all'])
        elif entity['name'] == 'checkpoint':
            classes.Checkpoint(entity['x'], entity['y'], entity['id'],
                               sprite_groups['checkpoints'], sprite_groups['all'])

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
