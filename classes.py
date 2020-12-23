import pygame
import funcs


class BaseBlock(pygame.sprite.Sprite):
    '''
    Класс Базового Блока.
    Родительский класс для других блоков.
    '''

    image = funcs.load_image('base_block.png', 50, 50)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = BaseBlock.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_rect(self):
        return self.rect


class Player(pygame.sprite.Sprite):
    '''
    Класс Игрока.
    '''

    image = funcs.load_image('base_player.png', 50, 50)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_rect(self):
        return self.rect
