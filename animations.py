from sprite import AnimatedSprite
import pygame, os

cache = {}
def load_images(path):
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    for file_name in sorted(os.listdir(path)):
        file = path + os.sep + file_name
        if file in cache:
            image = cache[file]
        else:
            print(file_name)
            image = pygame.image.load(file).convert_alpha()
            # image.set_colorkey((128,255,128))
            cache[file] = image
        images.append(image)
    return images


def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return image

