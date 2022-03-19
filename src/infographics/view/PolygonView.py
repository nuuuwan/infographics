from infographics.base import xy
from infographics.core import SVGPalette


class PolygonView:
    def __init__(
        self,
        ids,
        get_id_to_norm_multipolygon,
        get_id_to_color,
        get_id_to_label,
        children=[],
    ):
        self.ids = ids
        self.get_id_to_norm_multipolygon = get_id_to_norm_multipolygon
        self.get_id_to_color = get_id_to_color
        self.get_id_to_label = get_id_to_label
        self.children = children
        self.palette = SVGPalette()

    def render_polygons(self):
        rendered_polygons = []
        for id in self.ids:
            norm_multipolygon = self.get_id_to_norm_multipolygon(id)

            rendered_polygons.append(
                self.palette.draw_multipolygon(
                    norm_multipolygon,
                    [],
                    {'fill': self.get_id_to_color(id)},
                )
            )
        return rendered_polygons

    def render_labels(self):
        rendered_labels = []
        for id in self.ids:
            norm_multipolygon = self.get_id_to_norm_multipolygon(id)
            (cx, cy), (rx, ry) = xy.get_cxcyrxry(norm_multipolygon)
            rendered_labels.append(
                self.get_id_to_label(id, (cx, cy), (rx, ry)),
            )
        return rendered_labels

    def __xml__(self):

        return self.palette.draw_g(
            self.render_polygons() + self.render_labels() + self.children,
        )
