import pygame

class Ship:
    """ A class to manage the ship """

    def __init__(self, ai_game):
        """ Initialize the shi and set its starting position. """
        # screen is assigned as an attribute to the ship
        self.screen = ai_game.screen
        # we get the screens rect and assign it as an attribute
        # allows to place the ship in the screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and assign in to self.image
        self.image = pygame.image.load('images/ship.png')
        # assign this image to a rectangle using get_rect 
        # and assigning it to self. rect
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        # we are matching the value of self.rect mitbottom
        # to the midbottom attribute of screens rect
    self.rect.midbottom = self.screen_rect.midbottom

# draws the image to the screen at the position 
# specified by self.rect
def blitme(self):
    """Draw the ship at its current location."""
    self.screen.blit(self.image, self.rect)
