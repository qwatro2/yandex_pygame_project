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

    def get_rect(self):
        return self.rect


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

        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self, left, right, up, tile_group):
        if left:
            self.vx = -constants.MOVE_SPEED

        if right:
            self.vx = constants.MOVE_SPEED

        if up:
            if self.on_ground:
                self.vy = -constants.JUMP_POWER

        if not (left or right):
            self.vx = 0

        if not self.on_ground:
            self.vy += constants.GRAVITY

        self.on_ground = False

        self.rect.x += self.vx
        self.collide(self.vx, 0, tile_group)

        self.rect.y += self.vy
        self.collide(0, self.vy, tile_group)

    def collide(self, vx, vy, tile_group):
        for tile in tile_group:
            if pygame.sprite.collide_rect(self, tile):

                if vx > 0:
                    self.rect.right = tile.get_rect().left

                if vx < 0:
                    self.rect.left = tile.get_rect().right

                if vy > 0:
                    self.rect.bottom = tile.get_rect().top
                    self.on_ground = True
                    self.vy = 0

                if vy < 0:
                    self.rect.top = tile.get_rect().bottom
                    self.vy = 0


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
