import pygame


def load_image(filename, width, height, colorkey=None):
    '''

    :param filename: имя файла в папке
    :param width: требуемая ширина изображения
    :param height: требуемая высота изображения
    :param colorkey: цвет, который станет прозрачным, None, если изображение заведомо прозрачное
    :return: изображение нужного размера без фона
    '''

    # получаем полный путь к файлу
    fullname = f'data/scripts/{filename}'

    # загружаем имеющееся изображение
    image = pygame.image.load(fullname)

    # делаем фон прозрачным
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    # делаем изображение нужные размеры
    im_width = image.get_width()
    im_height = image.get_height()
    if im_width != width or im_height != height:
        image = pygame.transform.scale(image, (width, height))

    return image
