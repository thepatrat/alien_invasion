import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """ A class to manage bullets fired from ship"""

    def __init__(self, ai_game):
        """ Creates a bullet object at ships position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/laser.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet up the screen """
        self.y -= self.settings.laser_speed
        self.rect.y = self.y

    def blit_laser(self):
        """Draw the laser to the screen."""
        self.screen.blit(self.image, self.rect)
