"""
Renders a collection of polygons
"""
from infographics.core import SVGPalette


class PolygonView:
    def __init__(self, multi2polygon=None, color_list=None):

        self.multi2polygon = multi2polygon if multi2polygon else []
        if color_list:
            self.color_list = color_list
        else:
            self.color_list = SVGPalette.get_random_color_list(len(self))

    def __len__(self):
        return len(self.multi2polygon)

    @property
    def xml(self):
        palette = SVGPalette()

        return palette.draw_g(
            list(map(
                lambda x: palette.draw_multipolygon(
                    x[1],
                    {'fill': self.color_list[x[0]]},
                ),
                enumerate(self.multi2polygon),
            )),
        )
