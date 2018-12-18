from sprite import AnimatedSprite
import pygame, os

def load_images(path):
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert_alpha()
        # image.set_colorkey((128,255,128))
        images.append(image)
    return images


def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return image

