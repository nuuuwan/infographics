import math
from functools import cache

from infographics._utils import log
from infographics.base import dorling_compress, xy
from infographics.view.PolygonView import PolygonView


class DorlingView(PolygonView):
    def __init__(
        self,
        ids,
        get_id_to_norm_multipolygon,
        get_id_to_color_cartogram,
        get_id_to_label,
        get_id_to_cartogram_value,
        children,
    ):
        def get_id_to_color(id):
            return 'white'

        PolygonView.__init__(
            self,
            ids,
            get_id_to_norm_multipolygon,
            get_id_to_color,
            get_id_to_label,
            children,
        )
        self.get_id_to_color_cartogram = get_id_to_color_cartogram
        self.get_id_to_cartogram_value = get_id_to_cartogram_value

    @cache
    def get_id_to_cxcyrxry_all(self, palette):
        log.debug('[expensive] DorlingView.id_to_cxcyrxry')
        total_cartogram_value = 0
        for id in self.ids:
            cartogram_value = self.get_id_to_cartogram_value(id)
            total_cartogram_value += cartogram_value

        id_to_cxcyrxry = {}
        for id in self.ids:
            norm_multipolygon = self.get_id_to_norm_multipolygon(palette, id)
            cartogram_value = self.get_id_to_cartogram_value(id)
            (cx, cy), ____ = xy.get_cxcyrxry_for_multipolygon(norm_multipolygon)
            pr = 0.2 * math.sqrt(cartogram_value / total_cartogram_value)

            id_to_cxcyrxry[id] = [[cx, cy], [pr, pr]]

        xyrs = list(id_to_cxcyrxry.values())
        xyrs = dorling_compress._compress(xyrs, [-1, -1, 1, 1])
        id_to_cxcyrxry = dict(zip(id_to_cxcyrxry.keys(), xyrs))
        return id_to_cxcyrxry

    def get_id_to_cxcyrxry(self, palette, id):
        return self.get_id_to_cxcyrxry_all(palette).get(id)

    def render_dorling_object(self, palette, id, cxcy, rxry):
        return palette.draw_ellipse(
            cxcy,
            rxry,
            {'fill': self.get_id_to_color_cartogram(id)},
        )

    def render_dorling_objects(self, palette):
        rendered_dorling_objects = []
        for id in self.ids:
            [cx, cy], [rx, ry] = self.get_id_to_cxcyrxry(palette, id)
            rendered_dorling_objects.append(
                self.render_dorling_object(
                    palette,
                    id,
                    (cx, cy),
                    (rx, ry),
                )
            )
        return rendered_dorling_objects

    def __xml__(self, palette):
        return palette.draw_g(
            self.render_polygons(palette) +
            self.render_dorling_objects(palette) +
            self.render_labels(palette),
        )
