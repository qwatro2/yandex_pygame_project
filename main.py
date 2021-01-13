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
    pygame.mixer.music.load('data\music\Toccata_et_Fugue.ogg')
    pygame.mixer.music.play(-1)
    sound_death = pygame.mixer.Sound('data\music\death.ogg')
    sound_death.set_volume(0.5)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    die_blocks_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    monsters_group = pygame.sprite.Group()
    checkpoints_group = pygame.sprite.Group()

    new_blocks_group = pygame.sprite.Group()

    hearth_image = first_state_funcs.load_image('hearth.png', constants.TILE_WIDTH // 2, constants.TILE_HEIGHT // 2)

    left, right, up = [False] * 3

    # TODO: изменить заголовок и иконку игры
    pygame.display.set_caption('caption')

    # генерация уровня
    level_map, entities = first_state_funcs.load_level('test_level.txt').values()
    sprite_groups = {
        'all': all_sprites,
        'tiles': tile_group,
        'traps': die_blocks_group,
        'player': player_group,
        'monsters': monsters_group,
        'checkpoints': checkpoints_group
    }
    player, level_width, level_height = second_state_funcs.generate_level(level_map, entities, sprite_groups)

    # добавляем камеру
    camera = classes.Camera(second_state_funcs.camera_configure, (level_width + 1) * constants.TILE_WIDTH,
                            (level_height + 1) * constants.TILE_HEIGHT)

    # игровой цикл
    is_dead = False
    x = 0
    while game_loop:
        if is_dead:
            x += 1
        if x > 22:
            x = 0
            is_dead = False
            sound_death.stop()

        # обработка событий
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_loop = False

            elif event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    left = True

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    right = True

                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    up = True

                if event.key == pygame.K_0:
                    player.die()
                    for n_block in new_blocks_group:
                        n_block.kill()

                    sound_death.play()

            elif event.type == pygame.KEYUP:

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    left = False

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    right = False

                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    up = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 3:

                    if player.get_number_of_blocks() > 0:

                        new_block_x, new_block_y = None, None

                        if player.get_direction() == 0:

                            new_block_x = player.get_rect().left - constants.TILE_WIDTH

                        else:

                            new_block_x = player.get_rect().right

                        new_block_y = player.get_rect().top - constants.TILE_HEIGHT + constants.PLAYER_HEIGHT

                        new_block = classes.BaseBlock(new_block_x,
                                                      new_block_y)

                        if pygame.sprite.spritecollideany(new_block, tile_group):
                            new_block.kill()
                        else:
                            player.add_number_of_blocks(-1)
                            tile_group.add(new_block)
                            all_sprites.add(new_block)
                            new_blocks_group.add(new_block)

                elif event.button == 1:

                    player.deal_damage(monsters_group)

        # обновление всех спрайтов
        player_group.update(left, right, up, tile_group)
        monsters_group.update(tile_group)

        for checkpoint in checkpoints_group:
            if pygame.sprite.collide_rect(player, checkpoint):

                if isinstance(checkpoint, classes.Checkpoint) and not checkpoint.get_is_on():
                    player.set_to_go_coords(*checkpoint.get_coords())
                    checkpoint.set_is_on()

                    player.set_refresh_blocks_number(player.get_number_of_blocks())
                    new_blocks_group.empty()

        if pygame.sprite.spritecollideany(player, die_blocks_group):
            is_dead = player.take_damage()
            if is_dead:

                for n_block in new_blocks_group:
                    n_block.kill()

                sound_death.play()

        for monster in monsters_group:

            if pygame.sprite.collide_rect(monster, player):

                is_dead = player.take_damage()
                if is_dead:
                    for n_block in new_blocks_group:
                        n_block.kill()
                    sound_death.play()

        checkpoints_group.update()
        die_blocks_group.update()

        # отрисовка всех спрайтов
        screen.fill('white')
        camera.update(player)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        for i in range(player.get_healthpoints()):
            screen.blit(hearth_image, (i * hearth_image.get_rect().w + constants.TILE_WIDTH // 4,
                                       constants.TILE_HEIGHT // 4,
                                       hearth_image.get_rect().w, hearth_image.get_rect().h))

        pygame.display.update()

        clock.tick(constants.FPS)
        pygame.display.flip()

    # закрытие библиотеки pygame
    pygame.quit()
