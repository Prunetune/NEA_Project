import pygame

class CooldownTimer:
    """
    Generic timer class for handling cooldowns.
    """

    def __init__(self, cooldown_ms):
        """
        Initialize the timer.
        """
        self.cooldown_ms = cooldown_ms
        self.last_trigger_time = -cooldown_ms

    def trigger(self):
        """
        Start the timer.
        """
        self.last_trigger_time = pygame.time.get_ticks()

    def is_ready(self):
        """
        Check if the timer is finished.
        """
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_trigger_time) >= self.cooldown_ms

    def reset(self):
        """
        Reset the timer so it is ready immediately.
        """
        self.last_trigger_time = -self.cooldown_ms