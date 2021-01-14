import time
import pygame
import constants
import first_state_funcs


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = first_state_funcs.load_image(image_file, constants.WIDTH, constants.HEIGHT)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


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


class DieBlock(BaseBlock):
    '''
    Класс Блока Ловушки.
    При коллайде с ним, герой получает урон.
    '''

    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        sheet = first_state_funcs.load_image('12_nebula_spritesheet.png', 800, 800)
        self.frames = self.cut_sheet(sheet, 8, 8, 20, 20)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def get_rect(self):
        return self.rect

    def cut_sheet(self, sheet, columns, rows, width, height):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                if i + j < 10:
                    frame_location = (self.rect.w * i + width, self.rect.h * j + height)
                    frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, (self.rect.size[0] - width, self.rect.size[1] - height))))
                    if frames[-1].get_width() != constants.TILE_WIDTH or frames[
                        -1].get_height() != constants.TILE_HEIGHT:
                        frames[-1] = pygame.transform.scale(frames[-1],
                                                            (constants.TILE_WIDTH,
                                                             constants.TILE_HEIGHT))
        return frames

    def update(self):
        self.cur_frame += 1
        self.cur_frame %= len(self.frames)
        self.image = self.frames[self.cur_frame]


class Checkpoint(pygame.sprite.Sprite):
    '''
    Класс Чекпоинта.
    '''

    def __init__(self, x, y, id, *groups):
        super().__init__(*groups)
        sheet = first_state_funcs.load_image('11_fire_spritesheet.png', 800, 800)
        self.frames = self.cut_sheet(sheet, 8, 8, 43, 20)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.x = x
        self.y = y
        self.id = id
        self.is_on = False

    def cut_sheet(self, sheet, columns, rows, width, height):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                if i + j < 10:
                    frame_location = (self.rect.w * i + width, self.rect.h * j + height)
                    frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, (self.rect.size[0] - width, self.rect.size[1] - height))))
                    if frames[-1].get_width() != constants.TILE_WIDTH or frames[
                        -1].get_height() != constants.TILE_HEIGHT:
                        frames[-1] = pygame.transform.scale(frames[-1],
                                                            (constants.TILE_WIDTH,
                                                             constants.TILE_HEIGHT))
        return frames

    def get_is_on(self):
        return self.is_on

    def set_is_on(self):
        self.is_on = True
        sheet = first_state_funcs.load_image('16_sunburn_spritesheet.png', 800, 800)
        self.frames = self.cut_sheet(sheet, 8, 8, 25, 25)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def get_coords(self):
        return self.rect.left, self.rect.top

    def update(self):
        self.cur_frame += 1
        self.cur_frame %= len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    '''
    Класс Игрока.
    '''

    rimage = first_state_funcs.load_image('Stone_Golem.png', constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT)
    limage = first_state_funcs.load_image('Stone_Golem-.png', constants.PLAYER_WIDTH, constants.PLAYER_HEIGHT)

    def __init__(self, x, y, hp, blocks, *groups):
        super().__init__(*groups)
        self.image = Player.rimage
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.number_of_blocks = blocks
        self.direction = 1  # 1, если смотрим направо, иначе 0
        self.healthpoints = hp
        self.immortality = False
        self.immortality_timer = 0
        self.number_of_deaths = 0

        self.to_go_x = x
        self.to_go_y = y

        self.vx = 0
        self.vy = 0
        self.on_ground = False

        self.rwalk = [
            first_state_funcs.load_image(f'Stone_Walking\Stone_Golem_Walking_{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH,
                                         constants.PLAYER_HEIGHT) for i in range(24)]
        self.rwalk_number = 0
        self.lwalk = [
            first_state_funcs.load_image(f'Stone_Walking\Stone_Golem_Walking_-{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH,
                                         constants.PLAYER_HEIGHT) for i in range(24)]
        self.lwalk_number = 0

        self.rjump = first_state_funcs.load_image('Stone_Golem_Jumping_000.png', constants.PLAYER_WIDTH,
                                                  constants.PLAYER_HEIGHT)
        self.ljump = first_state_funcs.load_image('Stone_Golem_Jumping_-000.png', constants.PLAYER_WIDTH,
                                                  constants.PLAYER_HEIGHT)

        self.dead = False
        self.slash = False
        self.hurt = False

        self.rdying = [
            first_state_funcs.load_image(f'Stone_Dying\Stone_Golem_Dying_{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH,
                                         constants.PLAYER_HEIGHT) for i in range(15)]
        self.rdying_number = 0
        self.ldying = [
            first_state_funcs.load_image(f'Stone_Dying\Stone_Golem_Dying_-{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH,
                                         constants.PLAYER_HEIGHT) for i in range(15)]
        self.ldying_number = 0

        self.rslash = [
            first_state_funcs.load_image(f'Stone_Slashing\Stone_Slashing_{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH + 40,
                                         constants.PLAYER_HEIGHT) for i in range(12)]
        self.rslash_number = 0
        self.lslash = [
            first_state_funcs.load_image(f'Stone_Slashing\Stone_Slashing_-{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH + 40,
                                         constants.PLAYER_HEIGHT) for i in range(12)]
        self.lslash_number = 0

        self.rhurt = first_state_funcs.load_image(f'Stone_Hurt_000.png',
                                                  constants.PLAYER_WIDTH,
                                                  constants.PLAYER_HEIGHT)
        self.rhurt_number = 0
        self.lhurt = first_state_funcs.load_image(f'Stone_Hurt_-000.png',
                                                  constants.PLAYER_WIDTH,
                                                  constants.PLAYER_HEIGHT)
        self.lhurt_number = 0

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
        elif self.slash:
            self.lwalk_number = 0
            self.rwalk_number = 0
            if self.direction == 1:
                self.image = self.rslash[self.rslash_number]
                self.rslash_number += 1
                self.rslash_number %= len(self.rslash)
                if self.rslash_number == 0:
                    self.slash = False
            else:
                self.image = self.lslash[self.lslash_number]
                self.lslash_number += 1
                self.lslash_number %= len(self.lslash)
                if self.lslash_number == 0:
                    self.slash = False
        elif self.hurt:
            self.lwalk_number = 0
            self.rwalk_number = 0
            if self.direction == 1:
                self.image = self.rhurt
                self.rhurt_number += 1
                self.rhurt_number %= 5
                if self.rhurt_number == 0:
                    self.hurt = False
            else:
                self.image = self.lhurt
                self.lhurt_number += 1
                self.lhurt_number %= 5
                if self.lhurt_number == 0:
                    self.hurt = False
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
        if self.immortality_timer > 0:
            self.immortality_timer -= 1

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

    def get_deaths(self):
        return self.number_of_deaths

    def die(self):
        self.number_of_deaths += 1
        self.dead = True
        self.number_of_blocks = 5
        self.healthpoints = 2
        self.immortality_timer = 40
        self.vx = 0
        self.vy = 0

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

    def get_healthpoints(self):
        return self.healthpoints

    def take_damage(self):
        if not self.immortality:
            self.healthpoints -= 1

            self.immortality = True
            self.immortality_timer = 45
            if self.healthpoints == 0:
                self.die()
                return True
            else:
                self.hurt = True
            return False
        else:
            if self.immortality_timer == 0:
                self.immortality = False

    def deal_damage(self, monsters: pygame.sprite.Group):
        self.slash = True
        is_kill = False
        s_rect = self.rect
        damage_rect = pygame.Rect(s_rect.right if self.direction == 1 else s_rect.left,
                                  s_rect.top,
                                  s_rect.w // 2,
                                  s_rect.h)

        for monster in monsters:
            if isinstance(monster, BaseMonster) and damage_rect.colliderect(monster.get_rect()):
                is_kill = monster.take_damage()
        return is_kill


class BaseMonster(pygame.sprite.Sprite):

    def __init__(self, x, y, vx, max_left, hp, *groups):
        super().__init__(*groups)
        self.rwalk = [
            first_state_funcs.load_image(f'Enemy_Walking\Enemy_Walking_{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH * hp // 2,
                                         constants.PLAYER_HEIGHT * hp // 2) for i in range(18)]
        self.rwalk_number = 0
        self.lwalk = [
            first_state_funcs.load_image(f'Enemy_Walking\Enemy_Walking_-{str(i).rjust(3, "0")}.png',
                                         constants.PLAYER_WIDTH * hp // 2,
                                         constants.PLAYER_HEIGHT * hp // 2) for i in range(18)]
        self.lwalk_number = 0
        self.image = self.rwalk[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.start_x = x
        self.start_y = y
        self.vx = vx
        self.vy = 0
        self.max_left = max_left
        self.on_ground = True

        self.healthpoints = hp
        self.immortality = False
        self.immortality_timer = 0

    def update(self, platforms):
        self.rect.x += self.vx
        self.collide(self.vx, 0, platforms)

        if not self.on_ground:
            self.vy += constants.GRAVITY

        self.on_ground = False
        self.rect.y += self.vy
        self.collide(0, self.vy, platforms)

        if abs(self.start_x - self.rect.x) > self.max_left:
            self.vx = -self.vx
        if self.vx < 0:
            self.rwalk_number = 0
            self.image = self.lwalk[self.lwalk_number]
            self.lwalk_number += 1
            self.lwalk_number %= len(self.lwalk)
        elif self.vx > 0:
            self.lwalk_number = 0
            self.image = self.rwalk[self.rwalk_number]
            self.rwalk_number += 1
            self.rwalk_number %= len(self.rwalk)

        if self.immortality_timer > 0:
            self.immortality_timer -= 1

    def collide(self, vx, vy, platforms):

        for platform in platforms:

            if pygame.sprite.collide_rect(self, platform) and self != platform:

                if vx > 0:
                    self.rect.right = platform.get_rect().left
                    self.vx = -vx

                if vx < 0:
                    self.rect.left = platform.get_rect().right
                    self.vx = -vx

                if vy > 0:
                    self.rect.bottom = platform.get_rect().top
                    self.on_ground = True
                    self.vy = 0

    def die(self):
        self.kill()

    def get_rect(self):
        return self.rect

    def take_damage(self):
        if not self.immortality:
            self.healthpoints -= 1
            self.immortality = True
            self.immortality_timer = 40
            if self.healthpoints == 0:
                self.die()
                return True
            return False
        else:
            if self.immortality_timer == 0:
                self.immortality = False


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
