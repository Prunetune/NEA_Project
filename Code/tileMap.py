import pygame

class TileMap:
    """Represents the world as a grid of tiles (0 = floor, 1 = wall)."""

    def __init__(self, settings):
        self.settings = settings
        self.tileSize = self.settings.tileSize

        # base pattern (small hardcoded example). This is easy to edit.
        # 1 = wall, 0 = floor.
        self.basePattern = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,0,0,1,1,1,0,0,0,1],
            [1,0,0,1,0,1,0,0,0,1],
            [1,0,0,1,1,1,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]

        # build the full map by repeating basePattern
        self.map = self.build_full_map(self.settings.repeatX, self.settings.repeatY)

        # derived sizes
        self.rows = len(self.map)
        self.cols = len(self.map[0]) if self.map else 0
        self.pixelWidth = self.cols * self.tileSize
        self.pixelHeight = self.rows * self.tileSize

    def build_full_map(self, repeatX, repeatY):
        """Repeat the base pattern to create a larger level."""
        out = []
        for ry in range(repeatY):
            for row in self.basePattern:
                newRow = []
                for rx in range(repeatX):
                    newRow.extend(row)
                out.append(newRow)
        return out

    def get_tile_at_pixel(self, px, py):
        """Return tile value at given pixel coordinates. Out-of-range returns wall (1).
        This is used for collision checks.
        """
        tx = px // self.tileSize
        ty = py // self.tileSize
        if ty < 0 or ty >= len(self.map) or tx < 0 or tx >= len(self.map[0]):
            # treat out-of-bounds as wall to stop player from leaving the world
            return 1
        return self.map[ty][tx]

    def get_all_wall_rects(self):
        """Return a list of pygame.Rect for all wall tiles in world coordinates."""
        rects = []
        for r, row in enumerate(self.map):
            for c, t in enumerate(row):
                if t == 1:
                    rects.append(pygame.Rect(c * self.tileSize, r * self.tileSize, self.tileSize, self.tileSize))
        return rects

    def draw(self, surface, cameraX, cameraY):
        """Draw the entire tile map to the surface. This is intentionally brute-force and inefficient.
           Each tile is drawn regardless of whether it is visible on-screen.
           This is inefficient and i need to change it
        """
        ts = self.tileSize
        for rowIndex, row in enumerate(self.map):
            for colIndex, tile in enumerate(row):
                px = colIndex * ts - cameraX
                py = rowIndex * ts - cameraY
                color = self.settings.colorWall if tile == 1 else self.settings.colorFloor
                # draw rectangle tile
                pygame.draw.rect(surface, color, (px, py, ts, ts))