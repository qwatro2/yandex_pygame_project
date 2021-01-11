import time
import pygame
import constants
import first_state_funcs


class BaseBlock(pygame.sprite.Sprite):
    '''
    Класс Базового Блока.
    Родительский класс для других блоков.
    '''

    image = first_state_funcs.load_image('Stone.png', constants.TILE_WIDTH, constants.TILE_HEIGHT)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = BaseBlock.image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def get_rect(self):
        return self.rect


class Checkpoint(pygame.sprite.Sprite):
    '''
    Класс Чекпоинта.
    '''

    image_off = first_state_funcs.load_image('base_checkpoint_off.png', constants.CHECKPOINT_WIDTH,
                                             constants.CHECKPOINT_HEIGHT)

    image_on = first_state_funcs.load_image('base_checkpoint_on.png', constants.CHECKPOINT_WIDTH,
                                            constants.CHECKPOINT_HEIGHT)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Checkpoint.image_off
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.is_on = False

    def get_is_on(self):
        return self.is_on

    def set_is_on(self):
        self.is_on = True
        self.image = Checkpoint.image_on

    def get_coords(self):
        return self.rect.left, self.rect.top


class Player(pygame.sprite.Sprite):
    '''
    Класс Игрока.
    '''

    rimage = first_state_funcs.load_image('Stone_Golem.png', constants.TILE_WIDTH, constants.TILE_HEIGHT)
    limage = first_state_funcs.load_image('Stone_Golem-.png', constants.TILE_WIDTH, constants.TILE_HEIGHT)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Player.rimage
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.number_of_blocks = 10
        self.direction = 1  # 1, если смотрим направо, иначе 0

        self.to_go_x = x
        self.to_go_y = y

        self.vx = 0
        self.vy = 0
        self.on_ground = False

        self.rwalk = [
            first_state_funcs.load_image(f'Stone_Walking\Stone_Golem_Walking_{str(i).rjust(3, "0")}.png',
                                         constants.TILE_WIDTH,
                                         constants.TILE_HEIGHT) for i in range(24)]
        self.rwalk_number = 0
        self.lwalk = [
            first_state_funcs.load_image(f'Stone_Walking\Stone_Golem_Walking_-{str(i).rjust(3, "0")}.png',
                                         constants.TILE_WIDTH,
                                         constants.TILE_HEIGHT) for i in range(24)]
        self.lwalk_number = 0

        self.rjump = first_state_funcs.load_image('Stone_Golem_Jumping_000.png', constants.TILE_WIDTH,
                                                  constants.TILE_HEIGHT)
        self.ljump = first_state_funcs.load_image('Stone_Golem_Jumping_-000.png', constants.TILE_WIDTH,
                                                  constants.TILE_HEIGHT)

        self.dead = False
        self.rdying = [
            first_state_funcs.load_image(f'Stone_Dying\Stone_Golem_Dying_{str(i).rjust(3, "0")}.png',
                                         constants.TILE_WIDTH,
                                         constants.TILE_HEIGHT) for i in range(15)]
        self.rdying_number = 0
        self.ldying = [
            first_state_funcs.load_image(f'Stone_Dying\Stone_Golem_Dying_-{str(i).rjust(3, "0")}.png',
                                         constants.TILE_WIDTH,
                                         constants.TILE_HEIGHT) for i in range(15)]
        self.ldying_number = 0

    def update(self, left, right, up, tile_group):
        if self.dead:
            if self.direction == 1:
                self.image = self.rdying[self.rdying_number]
                self.rdying_number += 1
            else:
                self.image = self.ldying[self.ldying_number]
                self.ldying_number += 1
            if self.rdying_number == len(self.rdying) - 1 or self.ldying_number == len(self.ldying) - 1:
                self.dead = False
                self.move(self.to_go_x, self.to_go_y)
                self.ldying_number = 0
                self.rdying_number = 0
            pygame.time.wait(100)
        else:
            if left:
                self.vx = -constants.MOVE_SPEED
                self.direction = 0

            if right:
                self.vx = constants.MOVE_SPEED
                self.direction = 1

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
            if not (-1 < self.vy < 1):
                self.lwalk_number = 0
                self.rwalk_number = 0
                if self.direction == 1:
                    self.image = self.rjump
                else:
                    self.image = self.ljump
            elif left or right:
                if self.direction == 1:
                    self.lwalk_number = 0
                    self.image = self.rwalk[self.rwalk_number]
                    self.rwalk_number += 1
                    self.rwalk_number %= len(self.rwalk)
                else:
                    self.rwalk_number = 0
                    self.image = self.lwalk[self.lwalk_number]
                    self.lwalk_number += 1
                    self.lwalk_number %= len(self.lwalk)
            else:
                if self.direction == 1:
                    self.image = Player.rimage
                else:
                    self.image = Player.limage
                self.rwalk_number = 0
                self.lwalk_number = 0

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

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def die(self):
        self.dead = True

    def set_to_go_coords(self, x, y):
        self.to_go_x = x
        self.to_go_y = y

    def add_number_of_blocks(self, value):
        self.number_of_blocks += value

    def get_number_of_blocks(self):
        return self.number_of_blocks

    def get_rect(self):
        return self.rect

    def get_direction(self):
        return self.direction


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
