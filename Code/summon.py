import pygame
import pygame.sprite

from .enemy import Enemy

class Summon(pygame.sprite.Sprite):
    """
    Magic spell that summons an entity
    """

    def __init__(self ,settings , owner, type ,current_pos):
        super().__init__()
        self.settings = settings
        self.owner = owner
        self.entity_type = type
        self.spawn_pos = current_pos
        self.id = "Summon"
        self.allys_spawned = 0

    def spawn_ally(self):
        if self.allys_spawned == 0:
            self.allys_spawned += 1
            if self.entity_type == "enemy":
                return Enemy(self.settings,(self.spawn_pos.x + 50), (self.spawn_pos.y + 50))
            else:
                print("mistake")
        else:
            print("hello")
    def summon_update(self):
        print("summon is being update")
        self.kill()
