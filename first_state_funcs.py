import pygame


def load_image(filename: str, width: int, height: int, colorkey=None) -> pygame.Surface:
    '''

    :param filename: имя файла в папке
    :param width: требуемая ширина изображения
    :param height: требуемая высота изображения
    :param colorkey: цвет, который станет прозрачным, None, если изображение заведомо прозрачное
    :return: изображение нужного размера без фона
    '''

    # получаем полный путь к файлу
    fullname = f'data/sprites/{filename}'

    # загружаем имеющееся изображение
    image = pygame.image.load(fullname)

    # делаем фон прозрачным
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    # делаем изображение нужные размеры
    im_width = image.get_width()
    im_height = image.get_height()
    if im_width != width or im_height != height:
        image = pygame.transform.scale(image, (width, height))

    return image


def load_level(filename: str) -> list:
    '''

    :param filename: имя файла в папке
    :return: двумерный список, который представляет собой карту уровня
    '''

    # получаем полный путь к файлу
    fullname = f'data/levels/{filename}'

    # читаем карту уровня из файла
    with open(fullname, 'r') as file:
        level_map = list(map(lambda x: list(x.rstrip('\n')), file.readlines()))

    return level_map
