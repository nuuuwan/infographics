
from infographics.core import SVGPalette


class PolygonView:
    def __init__(self, multimultipolygon=[]):
        self.multimultipolygon = multimultipolygon

    @property
    def xml(self):
        palette = SVGPalette()
        return palette.draw_multimultipolygon(self.multimultipolygon)
