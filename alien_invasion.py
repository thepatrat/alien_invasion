import sys
import pygame
from game_stats import GameStats
from settings import Settings
from ship import Ship
from laser import Laser
from alien import Alien
from button import Button

import os
from time import sleep


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        # gives the attribute setting to the instance and
        # uses the method Settings defined in the settings.py
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Give the alien invasion instance a attribute
        # called ai.background which we attach the
        # image of the background to
        self.background = pygame.image.load(
            os.path.join("images", "Space.png"))

        # now project the background on a rectangle
        # which we set as the ai.scree_rect attribute
        self.screen_rect = self.background.get_rect()

        # give stats
        self.stats = GameStats(self)

        # create a ship instance
        self.ship = Ship(self)

        # create a laser group
        self.lasers = pygame.sprite.Group()

        # create a alien group
        self.aliens = pygame.sprite.Group()

        # creates a fleet of alien
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Starts the main game loop."""
        while True:
            # function that manages events
            self._check_events()

            # fleur stupid
            if self.stats.game_active:
                # takes the event input and update the
                # ship position accordingly
                self.ship.update()
                # updating the bullets
                self._update_lasers()
                # update the aliens
                self._update_aliens()
                # function that manages the screen
            self._update_screen()
            # Make the most recently drawn screen visible.
            pygame.display.flip()

    def _check_events(self):
        """ Watch for keyboard and mouse events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Check if mouse button click is on the play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)

            # Get rid of any remaining aliens and lasers
            self.aliens.empty()
            self.lasers.empty()

            # put in the new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # update the ship image
            self.ship.update_ship_image(
                self.settings.ship_maxhp, self.stats.ship_hp)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # we are setting a movement flag of the
            # ship class, which keeps it moving t
            # the right side
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # quitit
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_laser()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_laser(self):
        """ Creates a new laser and adds it to the laser group """
        if len(self.lasers) < self.settings.laser_allowed:
            new_laser = Laser(self)
            self.lasers.add(new_laser)

    def _update_lasers(self):
        """ Update position of lasers and get rid of
        old lasers """
        self.lasers.update()

        # get rid of bullets that have dissapeared.
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

        self._check_laser_alien_collisions()


    def _check_laser_alien_collisions(self):
        """ Respond to laser alien collision """
        # detect collision with an alien
        collisions = pygame.sprite.groupcollide(
            self.lasers, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing lasers and create new fleet
            self.lasers.empty()
            self._create_fleet()
        
    def _create_fleet(self):
        """ Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # determines the number of aliens fitting in a row
        available_space_x = (
            self.settings.screen_width - (2 * alien_width))
        number_aliens_x = available_space_x // (2 * alien_width)

        # determines how many rows fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height - ship_height))
        number_rows = available_space_y // (2 * alien_height)

        # Create a full fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ Create an alien and place it in the row """    
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """ Respond to aliens reaching the edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """ Update the positions of all aliens in the fleet. """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # checks if alien hit the bottom
        self._check_aliens_bottom()

    def _ship_hit(self):
        """ Respond to the ship being hit by an alien. """
        if self.stats.ship_hp > 0:
            # Lower HP of the ship
            self.stats.ship_hp -= 1
        
            # Get rid remaining aliens and lasers
            self.aliens.empty()
            self.lasers.empty()

            # Create a new fleet, center, and damage the ship.
            self._create_fleet()
            self.ship.center_ship()
            self.ship.update_ship_image(self.settings.ship_maxhp, self.stats.ship_hp)

            # Pause.
            sleep(2)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """ Check if any aliens have reached the bottom of the screen. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen,
        and flip to the new screen."""
        # Redraw the screen during each pass through the
        # loop
        # draw the ai.background and its rectangle to the screen
        self.screen.blit(self.background, self.screen_rect)

        # blitme function draws the ship to the scree
        self.ship.blitme()

        # update the laser position
        for laser in self.lasers.sprites():
            laser.blit_laser()

        # update the aliens
        self.aliens.draw(self.screen)

        # Draw play button is ai_game.stats.game_active is False
        if not self.stats.game_active:
            self.play_button.draw_button()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    # game instance is called ai
    ai = AlienInvasion()
    ai.run_game()
