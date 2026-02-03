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
        x = self.settings.hud_offset_x
        y_hp = self.settings.hud_offset_y_hp
        y_mana = self.settings.hud_offset_y_mana

        # Draw Health
        pygame.draw.rect(surface, self.settings.color_hp_bg, (x, y_hp, w, h))

        if hp_ratio > 0:
            pygame.draw.rect(surface, self.settings.color_hp, (x, y_hp, w * hp_ratio, h))

        pygame.draw.rect(surface, self.settings.color_border, (x, y_hp, w, h), 2)

        # Draw Mana
        pygame.draw.rect(surface, self.settings.color_hud_bg, (x, y_mana, w, h))

        if mana_ratio > 0:
            pygame.draw.rect(surface, self.settings.color_mana, (x, y_mana, w * mana_ratio, h))

        pygame.draw.rect(surface, self.settings.color_border, (x, y_mana, w, h), 2)