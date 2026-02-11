import pygame


class TileMap:
    """
    Handles map generation using a repeating pattern.
    """

    def __init__(self, settings):
        """
        Initialize map.
        """
        self.settings = settings
        self.tile_size = settings.tile_size

        # Base Pattern (10x7)
        # 1 = Wall, 0 = Floor
        self.base_pattern = [
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]
        ]

        self.map_data = self.build_full_map(settings.repeat_x, settings.repeat_y)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0]) if self.rows > 0 else 0

    def build_full_map(self, repeat_x, repeat_y):
        """
        Repeats the base pattern. Uses i, j for nested loops.
        """
        full_map = []
        for i in range(repeat_y):
            for row in self.base_pattern:
                new_row = []
                for j in range(repeat_x):
                    new_row.extend(row)

                full_map.append(new_row)

        return full_map

    def get_nearby_walls(self, rect):
        """
        Returns walls near the entity. Uses i, j for grid coordinates.
        """
        walls = []
        start_col = max(0, int(rect.left // self.tile_size) - 1)
        end_col = min(self.cols, int(rect.right // self.tile_size) + 2)
        start_row = max(0, int(rect.top // self.tile_size) - 1)
        end_row = min(self.rows, int(rect.bottom // self.tile_size) + 2)

        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                if self.map_data[i][j] == 1:
                    walls.append(pygame.Rect(j * self.tile_size, i * self.tile_size,
                                             self.tile_size, self.tile_size))

        return walls

    def draw(self, surface, cam_x, cam_y):
        """
        Draws visible tiles. Uses i, j for grid coordinates.
        """
        start_col = max(0, int(cam_x // self.tile_size))
        end_col = min(self.cols, int((cam_x + self.settings.screen_width) // self.tile_size) + 1)
        start_row = max(0, int(cam_y // self.tile_size))
        end_row = min(self.rows, int((cam_y + self.settings.screen_height) // self.tile_size) + 1)

        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                if self.map_data[i][j] == 1:
                    draw_x = j * self.tile_size - cam_x
                    draw_y = i * self.tile_size - cam_y
                    pygame.draw.rect(surface, self.settings.color_wall,
                                     (draw_x, draw_y, self.tile_size, self.tile_size))