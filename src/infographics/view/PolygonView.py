"""
Renders a collection of polygons
"""
from infographics.core import SVGPalette


class PolygonView:
    def __init__(
        self,
        id_to_multipolygon,
        func_id_to_color=None,
    ):
        self.id_to_multipolygon = id_to_multipolygon
        self.func_id_to_color = func_id_to_color
        self.palette = SVGPalette()

    def __len__(self):
        return len(self.id_to_multipolygon)

    @property
    def xml(self):

        inner_child_list = []
        for id, multipolygon in self.id_to_multipolygon.items():
            attribs = {}
            if self.func_id_to_color:
                attribs['fill'] = self.func_id_to_color(id)

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    [],
                    attribs,
                )
            )

        return self.palette.draw_g(inner_child_list + self.get_child_list())
