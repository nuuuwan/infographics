import math
from abc import ABC
from functools import cached_property

from infographics._utils import log
from infographics.base import dorling_compress, xy
from infographics.core import SVGPalette
from infographics.view.ColoredView import ColoredView
from infographics.view.LabelledView import LabelledView

CIRLCE_RADIUS_MAX_LABEL_VALUE = 0.2


class DorlingView(ABC):
    DEFAULT_CLASS_COLORED_VIEW = ColoredView
    DEFAULT_CLASS_LABELLED_VIEW = LabelledView

    def __init__(
        self,
        # For ColoredView
        keys,
        get_color_value,
        legend_title,
        color_palette,

        # For LabelledView
        get_label_data,

        # For PolygonView
        id_to_multipolygon,

        # For DorlingView

        # classes
        class_colored_view=DEFAULT_CLASS_COLORED_VIEW,
        class_labelled_view=DEFAULT_CLASS_LABELLED_VIEW,
    ):

        self.get_label_data = get_label_data
        self.id_to_multipolygon = id_to_multipolygon

        self.colored_view = class_colored_view(
            keys,
            self.get_color_value,
            legend_title,
            color_palette,
        )

        self.labelled_view = class_labelled_view(
            keys,
            get_label_data,
            self.get_label_xy,
            self.get_label_r,
        )

        self.palette = SVGPalette()

    @cached_property
    def id_to_xyr(self):
        log.debug('[expensive] DorlingView.id_to_xyr')
        total_label_value = 0
        for id, multipolygon in self.id_to_multipolygon.items():
            label_data = self.get_label_data(id)
            total_label_value += label_data['label_value']

        id_to_xyr = {}
        for id, multipolygon in self.id_to_multipolygon.items():
            label_data = self.get_label_data(id)
            pr = math.sqrt(
                label_data['label_value'] /
                total_label_value
            ) * CIRLCE_RADIUS_MAX_LABEL_VALUE
            px, py = xy.get_midxy(multipolygon)

            id_to_xyr[id] = dict(
                x=px,
                y=py,
                r=pr,
            )

        xyrs = list(id_to_xyr.values())
        xyrs = dorling_compress._compress(xyrs, [-1, -1, 1, 1])
        id_to_xyr = dict(zip(id_to_xyr.keys(), xyrs))
        return id_to_xyr

    def __len__(self):
        return len(self.id_to_multipolygon)

    def get_multipolygon(self, id):
        return self.id_to_multipolygon[id]

    def __xml__(self):
        inner_child_list = []

        for id, multipolygon in self.id_to_multipolygon.items():
            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    [],
                    {},
                )
            )

        for id, multipolygon in self.id_to_multipolygon.items():
            attribs = {'fill': self.colored_view.get_color(id)}

            xyr = self.id_to_xyr[id]
            inner_child_list.append(
                self.render_dorling_object(
                    id,
                    (xyr['x'], xyr['y']),
                    xyr['r'],
                    attribs,
                )
            )

        return self.palette.draw_g(
            inner_child_list + [
                self.colored_view.__xml__(),
                self.labelled_view.__xml__(),
            ])

    def render_dorling_object(self, id, xy, r, attribs):
        return self.palette.draw_circle(
            xy,
            r,
            attribs,
        )

    # For LabelledView
    def get_label_xy(self, id):
        xyr = self.id_to_xyr[id]
        return (xyr['x'], xyr['y'])

    def get_label_r(self, id):
        xyr = self.id_to_xyr[id]
        return xyr['r']

    def get_color_value(self, id):
        return ''
