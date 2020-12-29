import pygame
import constants
import first_state_funcs


class BaseBlock(pygame.sprite.Sprite):
    '''
    Класс Базового Блока.
    Родительский класс для других блоков.
    '''

    image = first_state_funcs.load_image('base_block.png', constants.TILE_WIDTH, constants.TILE_HEIGHT)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = BaseBlock.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    '''
    Класс Игрока.
    '''

    image = first_state_funcs.load_image('base_player.png', constants.TILE_WIDTH, constants.TILE_HEIGHT)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
