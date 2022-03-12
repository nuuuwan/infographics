"""
Renders a collection of polygons
"""
from infographics.core import SVGPalette


class PolygonView:
    def __init__(
        self,
        id_to_multipolygon,
        child_list=[],
        func_id_to_color=None,
        func_id_to_child_list=None,
    ):
        self.id_to_multipolygon = id_to_multipolygon
        self.func_id_to_color = func_id_to_color
        self.func_id_to_child_list = func_id_to_child_list
        self.child_list = child_list
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

            multipolygon_child_list = []
            if self.func_id_to_child_list:
                multipolygon_child_list = self.func_id_to_child_list(id)

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    multipolygon_child_list,
                    attribs,
                )
            )

        return self.palette.draw_g(inner_child_list + self.child_list)
