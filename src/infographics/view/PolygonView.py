"""
Renders a collection of polygons
"""
from infographics.core import SVGPalette


class PolygonView:
    def __init__(
        self,
        id_to_multipolygon,
        get_color=None,
    ):
        self.id_to_multipolygon = id_to_multipolygon
        self.get_color = get_color
        self.palette = SVGPalette()

    def __len__(self):
        return len(self.id_to_multipolygon)

    def get_multipolygon(self, id):
        return self.id_to_multipolygon[id]

    def __xml__(self):
        inner_child_list = []
        for id, multipolygon in self.id_to_multipolygon.items():
            attribs = {}
            if self.get_color:
                attribs['fill'] = self.get_color(id)

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    [],
                    attribs,
                )
            )
        return self.palette.draw_g(inner_child_list)
