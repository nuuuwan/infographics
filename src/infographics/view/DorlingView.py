import math
from abc import ABC

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
        get_label,
        get_label_value,

        # For PolygonView
        id_to_multipolygon,

        # classes
        class_colored_view=DEFAULT_CLASS_COLORED_VIEW,
        class_labelled_view=DEFAULT_CLASS_LABELLED_VIEW,
    ):

        self.get_label = get_label
        self.get_label_value = get_label_value
        self.id_to_multipolygon = id_to_multipolygon
        self.id_to_xyr = self.build_id_to_xyr()

        self.colored_view = class_colored_view(
            keys,
            get_color_value,
            legend_title,
            color_palette,
        )

        self.labelled_view = class_labelled_view(
            keys,
            get_label,
            get_label_value,
            self.get_label_xy,
            self.get_label_relative_font_size,
        )

        self.palette = SVGPalette()

    def build_id_to_xyr(self):
        total_label_value = 0
        for id, multipolygon in self.id_to_multipolygon.items():
            total_label_value += self.get_label_value(id)

        id_to_xyr = {}
        for id, multipolygon in self.id_to_multipolygon.items():
            pr = math.sqrt(
                self.get_label_value(id) /
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
                self.palette.draw_circle(
                    [xyr['x'], xyr['y']],
                    xyr['r'],
                    attribs,
                )
            )

        return self.palette.draw_g(
            inner_child_list + [
                self.colored_view.__xml__(),
                self.labelled_view.__xml__(),
            ])

    # For LabelledView
    def get_label_xy(self, id):
        xyr = self.id_to_xyr[id]
        return (xyr['x'], xyr['y'])

    def get_label_relative_font_size(self, id):
        xyr = self.id_to_xyr[id]
        relative_font_width = xyr['r'] * 2 * \
            self.palette.actual_width / SVGPalette.DEFAULT_BASE_FONT_SIZE
        relative_font_size = min(
            0.8, relative_font_width / len(self.get_label(id)))
        if relative_font_size < 0.5:
            relative_font_size = 0
        return relative_font_size
