class Settings:
    """ A class to store all settings for alien invasion."""

    def __init__(self):
        """ Initialize the games settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800


        # laser settings
        self.laser_speed = 15
        self.laser_allowed = 3

        # Alien settings
        self.alien_speed = 5
        self.fleet_direction = 1
        self.fleet_drop_speed = 10

        # Ship settings
        self.ship_maxhp = 2
        self.ship_speed = 10