import pygame


class TileMap:
    """Represents the world as a grid of tiles (0 = floor, 1 = wall)."""

    def __init__(self, settings):
        self.settings = settings
        self.tile_size = self.settings.tile_size

        # base pattern (small hardcoded example). This is easy to edit.
        # 1 = wall, 0 = floor.
        self.base_pattern = [
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        ]

        # build the full map by repeating base_pattern
        self.map = self.build_full_map(self.settings.repeat_x, self.settings.repeat_y)

        # derived sizes
        self.rows = len(self.map)
        self.cols = len(self.map[0]) if self.map else 0
        self.pixel_width = self.cols * self.tile_size
        self.pixel_height = self.rows * self.tile_size

    def build_full_map(self, repeat_x, repeat_y):
        """Repeat the base pattern to create a larger level."""
        out = []
        for ry in range(repeat_y):
            for row in self.base_pattern:
                new_row = []
                for rx in range(repeat_x):
                    new_row.extend(row)
                out.append(new_row)
        return out

    def get_tile_at_pixel(self, px, py):
        """Return tile value at given pixel coordinates. Out-of-range returns wall (1).

        This is used for collision checks.
        """
        tx = px // self.tile_size
        ty = py // self.tile_size
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
                    rects.append(pygame.Rect(c * self.tile_size, r * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def draw(self, surface, camera_x, camera_y):
        """Draw the entire tile map to the surface. This is intentionally brute-force and inefficient.

        Each tile is drawn regardless of whether it is visible on-screen.
        This is inefficient and should be improved later.
        """
        ts = self.tile_size
        for row_index, row in enumerate(self.map):
            for col_index, tile in enumerate(row):
                px = col_index * ts - camera_x
                py = row_index * ts - camera_y
                color = self.settings.color_wall if tile == 1 else self.settings.color_floor
                # draw rectangle tile
                pygame.draw.rect(surface, color, (px, py, ts, ts))
