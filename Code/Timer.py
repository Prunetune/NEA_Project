import pygame


class CooldownTimer:
    """Generic timer class for handling cooldowns."""

    def __init__(self, cooldown_ms):
        # total cooldown duration in milliseconds
        self.cooldown_ms = cooldown_ms
        # timestamp when the timer was last triggered
        self.last_trigger_time = -cooldown_ms

    def trigger(self):
        """Start the cooldown timer."""
        self.last_trigger_time = pygame.time.get_ticks()

    def is_ready(self):
        """Return True if the cooldown has finished."""
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_trigger_time) >= self.cooldown_ms

    def get_remaining_time(self):
        """Return remaining cooldown time in milliseconds (never below 0)."""
        current_time = pygame.time.get_ticks()
        remaining = self.cooldown_ms - (current_time - self.last_trigger_time)
        return max(0, remaining)

    def reset(self):
        """Reset the timer so it is immediately ready."""
        self.last_trigger_time = -self.cooldown_ms