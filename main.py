from PIL import Image
import random
import sys
from pathlib import Path

TILE_WIDTH = 200
TILE_PATH = sys.argv[1]

# A canvas consists of multiple rows
# A Row consist of multiple tiles
# A tile is randomly chosen from the tilepath

class Tile:
    def __init__(self):
        self.img = Image.open(
            random.choice(
                [x.absolute() for x in Path(f"{TILE_PATH}").glob("*.png")]
            )
        ).rotate(random.choice([0,90,180, 270]))
        if random.random() > 0.5:
            self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        if random.random() > 0.5:
            self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)

class Row:
    def __init__(self, tiles):
        self.tiles = tiles
        self.img = self.mk_img()
    
    def mk_img(self):
        img = self.tiles[0].img
        for tile in self.tiles[1:]:
            img = concat_horizontally(img, tile.img)
        return img
        

class Canvas:
    def __init__(self, rows):
        self.rows = rows
        self.img = self.mk_img()
    
    def mk_img(self):
        img = self.rows[0].img
        for row in self.rows[1:]:
            img = concat_vertically(img, row.img)
        return img

def concat_horizontally(img1, img2):
    new = Image.new("RGBA", (img1.width + img2.width, img1.height))
    new.paste(img1, (0,0))
    new.paste(img2, (img1.width, 0))
    return new

def concat_vertically(img1, img2):
    new = Image.new("RGBA", (img1.width, img2.height + img1.height))
    new.paste(img1, (0,0))
    new.paste(img2, (0, img1.height))
    return new

def main(size, outfile):
    n_tiles = sum([1 for n in range(0,size,TILE_WIDTH)]) # amount of tiles per row and column
    Canvas([Row([Tile() for n in range(n_tiles)]) for n in range(n_tiles)]).img.save(f"{outfile}.png")

if __name__ == "__main__":
    size = 2000
    outfile = "test"
    main(size, outfile)
    
