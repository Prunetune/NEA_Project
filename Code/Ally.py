import pygame
from .enemy import Enemy

class Ally(Enemy):

    def calculate_path(self, start, target, tile_map):
