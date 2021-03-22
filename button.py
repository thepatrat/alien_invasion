import pygame.font
import pygame

class Button:

    def __init__(self, ai_game, msg):
        """ Initialize button attributes """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the button image and rect
        self.image = pygame.image.load("images/Play_button.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        
        # Set the font
        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (180, 180, 180)

        # Buttoan message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """ Turn msg into a rendered image and center text on the button image """
        self.msg_image = self.font.render(
            msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)