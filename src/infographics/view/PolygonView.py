
from infographics.core import SVGPalette


class PolygonView:
    def __init__(self, multi2polygon=[]):
        self.multi2polygon = multi2polygon

    @property
    def xml(self):
        palette = SVGPalette()
        return palette.draw_multi2polygon(self.multi2polygon)
