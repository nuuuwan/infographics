import math
from functools import cached_property

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

    @cached_property
    def id_to_cxcyrxry(self):
        log.debug('[expensive] DorlingView.id_to_cxcyrxry')
        total_cartogram_value = 0
        for id in self.ids:
            cartogram_value = self.get_id_to_cartogram_value(id)
            total_cartogram_value += cartogram_value

        id_to_cxcyrxry = {}
        for id in self.ids:
            norm_multipolygon = self.get_id_to_norm_multipolygon(id)
            cartogram_value = self.get_id_to_cartogram_value(id)
            (cx, cy), ____ = xy.get_cxcyrxry(norm_multipolygon)
            pr = 0.2 * math.sqrt(cartogram_value / total_cartogram_value)

            id_to_cxcyrxry[id] = [[cx, cy], [pr, pr]]

        xyrs = list(id_to_cxcyrxry.values())
        xyrs = dorling_compress._compress(xyrs, [-1, -1, 1, 1])
        id_to_cxcyrxry = dict(zip(id_to_cxcyrxry.keys(), xyrs))
        return id_to_cxcyrxry

    def render_dorling_object(self, id, cxcy, rxry):
        return self.palette.draw_ellipse(
            cxcy,
            rxry,
            {'fill': self.get_id_to_color_cartogram(id)},
        )

    def render_labels(self):
        rendered_labels = []
        for id in self.ids:
            [cx, cy], [rx, ry] = self.id_to_cxcyrxry[id]
            rendered_labels.append(
                self.get_id_to_label(id, (cx, cy), (rx, ry)),
            )
        return rendered_labels

    def render_dorling_objects(self):
        rendered_dorling_objects = []
        for id in self.ids:
            [cx, cy], [rx, ry] = self.id_to_cxcyrxry[id]
            rendered_dorling_objects.append(
                self.render_dorling_object(
                    id,
                    (cx, cy),
                    (rx, ry),
                )
            )
        return rendered_dorling_objects

    def __xml__(self):

        return self.palette.draw_g(
            self.render_polygons() +
            self.render_dorling_objects() +
            self.render_labels(),
        )
