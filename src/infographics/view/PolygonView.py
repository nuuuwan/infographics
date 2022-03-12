
from infographics.core import SVGPalette


class PolygonView:
    def __init__(self, p_list_list_list=[]):
        self.p_list_list_list = p_list_list_list

    @property
    def xml(self):
        palette = SVGPalette()
        return palette.draw_p_list_list_list(self.p_list_list_list)
