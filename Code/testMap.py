from settings import Settings
from tileMap import TileMap

if __name__ == '__main__':
    settings = Settings()
    tile_map = TileMap(settings)
    # print map size and a small preview
    print(f"Map cols: {tile_map.cols}, rows: {tile_map.rows}")
    # show top-left 20x10 as text
    for r in range(min(10, tile_map.rows)):
        print(''.join(str(x) for x in tile_map.map[r][:20]))
