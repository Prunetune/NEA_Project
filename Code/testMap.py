from settings import Settings
from tileMap import TileMap

if __name__ == '__main__':
    s = Settings()
    tm = TileMap(s)
    # print map size and a small preview
    print(f"Map cols: {tm.cols}, rows: {tm.rows}")
    # show top-left 20x10 as text
    for r in range(min(10, tm.rows)):
        print(''.join(str(x) for x in tm.map[r][:20]))
