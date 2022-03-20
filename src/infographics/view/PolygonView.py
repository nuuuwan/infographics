from infographics.base import xy


class PolygonView:
    def __init__(
        self,
        ids,
        get_id_to_norm_multipolygon,
        get_id_to_color,
        get_id_to_label,
    ):
        self.ids = ids
        self.get_id_to_norm_multipolygon = get_id_to_norm_multipolygon
        self.get_id_to_color = get_id_to_color
        self.get_id_to_label = get_id_to_label

    def get_id_to_cxcyrxry(self, palette, id):
        norm_multipolygon = self.get_id_to_norm_multipolygon(palette, id)
        (cx, cy), (rx, ry) = xy.get_cxcyrxry_for_multipolygon(norm_multipolygon)
        return (cx, cy), (rx, ry)

    def render_polygons(self, palette):
        rendered_polygons = []
        for id in self.ids:
            norm_multipolygon = self.get_id_to_norm_multipolygon(palette, id)

            rendered_polygons.append(
                palette.draw_multipolygon(
                    norm_multipolygon,
                    {'fill': self.get_id_to_color(id)},
                )
            )
        return rendered_polygons

    def render_labels(self, palette):
        rendered_labels = []
        for id in self.ids:
            (cx, cy), (rx, ry) = self.get_id_to_cxcyrxry(palette, id)
            rendered_labels.append(
                self.get_id_to_label(palette, id, (cx, cy), (rx, ry)),
            )
        return rendered_labels

    def __xml__(self, palette):

        return palette.draw_g(
            self.render_polygons(palette) +
            self.render_labels(palette)
        )
