import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super(Sprite, self).__init__()
        size = (32, 32)  # This should match the size of the images.
        self.rect = pygame.Rect(position, size)
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, images):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        size = (32, 32)  # This should match the size of the images.

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.

        self.animation_time = 30
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


    def update(self, dt, x = None, y = None):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
        if x != None:
            self.rect.left = x
        if y != None:
            self.rect.top = y
        #self.update_frame_dependent()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
