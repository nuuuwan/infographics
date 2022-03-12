from utils import colorx


class ColorPaletteVaryLightness:
    def __init__(self, hue=0, min_lightness=0.9, max_lightness=0.1, n=1):
        self.hue = hue
        self.min_lightness = min_lightness
        self.max_lightness = max_lightness
        self.n = n

    def color(self, p):
        lightness_span = self.max_lightness - self.min_lightness
        lightness = self.min_lightness + lightness_span * p / self.n
        color = colorx.random_hsl(hue=self.hue, lightness=lightness)
        return color
