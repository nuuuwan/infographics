from utils import colorx


class ColorPaletteVaryHue:
    def __init__(self, min_hue=240, max_hue=0, n=1):
        self.min_hue = min_hue
        self.max_hue = max_hue
        self.n = n

    def color(self, p):
        hue_span = self.max_hue - self.min_hue
        hue = self.min_hue + (int)(hue_span * p / self.n)
        return colorx.random_hsl(hue=hue)
