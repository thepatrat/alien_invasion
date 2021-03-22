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

        # in alien_invasions a settings instance is created
        # from the Settings class, which we are calling
        self.settings = ai_game.settings

        self.ship_images = (
            pygame.image.load('images/Ship1.png'),
            pygame.image.load('images/Ship2.png'),
            pygame.image.load('images/Ship3.png')
            )

        # Load the ship image and assign in to self.image
        self.image = self.ship_images[0]

        # assign this image to a rectangle using get_rect
        # and assigning it to self. rect
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        # we are matching the value of self.rect mitbottom
        # to the midbottom attribute of screens rect
        self.rect.midbottom = self.screen_rect.midbottom

        # store x pos of the ship to ai.ship.x
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update ships x value, not the rect x
        if (self.moving_right and self.rect.right
                < self.screen_rect.right):
            self.x += self.settings.ship_speed
        if (self.moving_left and self.rect.left
                > 0):
            self.x -= self.settings.ship_speed

        # update the x position of the ship rectangle
        self.rect.x = self.x

# draws the image to the screen at the position
# specified by self.rect

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    
    def update_ship_image(self, max_hp, hp):
        """ Changes image of the ship depending on the ship hp"""
        try:
            self.image = self.ship_images[max_hp - hp]
        except(IndexError):
            pass
