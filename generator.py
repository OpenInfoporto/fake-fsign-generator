from PIL import Image, ImageDraw
import random

class FCodeGenerator:

    def __init__(self, image_size=None, image_border=None, density=None):
        self.IMAGE_SIZE = image_size or 4
        self.RESERVED_SPACE = image_border or 1
        self.DENSITY = density or 5

        self.usable_area = self.calculate_spaces()

    def calculate_spaces(self):
        RESERVED_SPACE = self.RESERVED_SPACE
        IMAGE_SIZE = self.IMAGE_SIZE
        spaces = list()

        pixels = [(x,y) for x in range(0,IMAGE_SIZE) for y in range(0,IMAGE_SIZE)]

        imagebox = (IMAGE_SIZE-(RESERVED_SPACE*2), IMAGE_SIZE-(RESERVED_SPACE*2))
        noprint = [(x,y) for x in range(0+RESERVED_SPACE,imagebox[0]+RESERVED_SPACE) for y in range(0+RESERVED_SPACE,imagebox[1]+RESERVED_SPACE)]
        noprint += [(x,y) for x in range(0,RESERVED_SPACE) for y in (0,RESERVED_SPACE)]

        spaces = [i for i in pixels if i not in noprint]

        return spaces

    def make(self):
        image = Image.new('RGBA', (self.IMAGE_SIZE, self.IMAGE_SIZE), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        i = 0

        while i < self.DENSITY:
            coord = self.usable_area.pop(random.randint(0,len(self.usable_area)-1))
            draw.point(coord, fill="black")
            i += 1

        del draw
        return image

    @staticmethod
    def merge_pictures(background, foreground, outimage):
        background = Image.open(background)
        foreground = Image.open(foreground)

        background.paste(foreground, (0, 0), foreground)
        background.save(outimage)


if __name__ == '__main__':
    g = FCodeGenerator(image_size=50, image_border=4, density=100)

    filepath = 'test.png'

    image = g.make()
    image.save(filepath)

    img = Image.open(filepath).resize((500,500))
    img.save(filepath)

    g.merge_pictures(filepath, "finger.png", "out.png")
