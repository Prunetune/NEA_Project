import pygame


class HUD:
    """
    Heads-Up Display. Draws UI elements.
    """

    def __init__(self, settings):
        """
        Initialize settings.
        """
        self.settings = settings

    def draw(self, surface, player):
        """
        Draws the health and mana bars using settings variables.
        """
        hp_ratio = player.health / self.settings.max_health
        mana_ratio = player.mana / self.settings.player_max_mana

        w = self.settings.hud_bar_width
        h = self.settings.hud_bar_height
        x = self.settings.hud_offset_x  # sets the x coordinates for the health and mana bar
        y_hp = self.settings.hud_offset_y_hp # sets the y coord for its respective bar
        y_mana = self.settings.hud_offset_y_mana # sets the y coord for its respective bar

        # Draw Health
        pygame.draw.rect(surface, self.settings.color_hp_bg, (x, y_hp, w, h)) # creates the black background for the
                                                                                   # bar to be pasted over

        pygame.draw.rect(surface, self.settings.color_hp, (x, y_hp, w * hp_ratio, h))  # draws the fill over the
                                                                                            # black  background for hp

        pygame.draw.rect(surface, self.settings.color_border, (x, y_hp, w, h), 2) # provides a white border
                                                                                             # to surround the hp bar

        # Draw Mana - sequence is the same as for hp
        pygame.draw.rect(surface, self.settings.color_hud_bg, (x, y_mana, w, h))

        pygame.draw.rect(surface, self.settings.color_mana, (x, y_mana, w * mana_ratio, h))

        pygame.draw.rect(surface, self.settings.color_border, (x, y_mana, w, h), 2)





