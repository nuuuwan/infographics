import math
from abc import ABC
from functools import cached_property

from infographics._utils import log
from infographics.base import dorling_compress, xy
from infographics.core import SVGPalette


class DorlingView(ABC):
    def __init__(
        self,
        ids,
        get_id_to_norm_multipolygon,
        get_id_to_color,
        get_id_to_label,
        get_id_to_cartogram_value,
        children=[],
    ):

        self.ids = ids
        self.get_id_to_norm_multipolygon = get_id_to_norm_multipolygon
        self.get_id_to_color = get_id_to_color
        self.get_id_to_label = get_id_to_label
        self.get_id_to_cartogram_value = get_id_to_cartogram_value
        self.children = children
        self.palette = SVGPalette()

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
            pr = 0.3 * math.sqrt(cartogram_value / total_cartogram_value)

            id_to_cxcyrxry[id] = [[cx, cy], [pr, pr]]

        xyrs = list(id_to_cxcyrxry.values())
        xyrs = dorling_compress._compress(xyrs, [-1, -1, 1, 1])
        id_to_cxcyrxry = dict(zip(id_to_cxcyrxry.keys(), xyrs))
        return id_to_cxcyrxry

    def __xml__(self):
        inner_child_list = []
        for id in self.ids:
            norm_multipolygon = self.get_id_to_norm_multipolygon(id)

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    norm_multipolygon,
                    [],
                    {'fill': 'white'},
                )
            )

        for id in self.ids:
            [cx, cy], [rx, ry] = self.id_to_cxcyrxry[id]
            inner_child_list.append(
                self.render_dorling_object(
                    id,
                    (cx, cy),
                    (rx, ry),
                )
            )

        for id in self.ids:
            [cx, cy], [rx, ry] = self.id_to_cxcyrxry[id]
            inner_child_list.append(
                self.get_id_to_label(id, (cx, cy), (rx, ry))
            )

        return self.palette.draw_g(
            inner_child_list,
            self.children,
        )

    def render_dorling_object(self, id, cxcy, rxry):
        return self.palette.draw_ellipse(
            cxcy,
            rxry,
            {'fill': self.get_id_to_color(id)},
        )
