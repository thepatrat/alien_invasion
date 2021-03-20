class Settings:
    """ A class to store all settings for alien invasion."""

    def __init__(self):
        """ Initialize the games settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.ship_speed = 10

        # laser settings
        self.laser_speed = 15
        self.laser_allowed = 3
