import math
from abc import ABC

from infographics.base import xy, dorling_compress
from infographics.core import SVGPalette
from infographics.view.ColoredView import ColoredView
from infographics.view.LabelledView import LabelledView

CIRLCE_RADIUS_MAX_LABEL_VALUE = 0.1


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
        self.colored_view = class_colored_view(
            keys,
            get_color_value,
            legend_title,
            color_palette,
        )

        self.get_label = get_label
        self.get_label_value = get_label_value
        self.labelled_view = class_labelled_view(
            keys,
            get_label,
            get_label_value,
            self.get_label_xy,
            self.get_label_relative_font_size,
        )
        self.id_to_multipolygon = id_to_multipolygon
        self.palette = SVGPalette()

    def __len__(self):
        return len(self.id_to_multipolygon)

    def get_multipolygon(self, id):
        return self.id_to_multipolygon[id]

    def __xml__(self):
        inner_child_list = []

        max_label_value = 0
        for id, multipolygon in self.id_to_multipolygon.items():
            max_label_value = max(max_label_value, self.get_label_value(id))

        xyrs = []
        for id, multipolygon in self.id_to_multipolygon.items():
            pr = math.sqrt(self.get_label_value(id) /
                           max_label_value) * CIRLCE_RADIUS_MAX_LABEL_VALUE
            px, py = self.get_label_xy(id)
            xyrs.append(dict(
                x=px,
                y=py,
                r=pr,
            ))

        xyrs = dorling_compress._compress(xyrs, [-1, -1, 1, 1])

        for i, (id, multipolygon) in enumerate(
                self.id_to_multipolygon.items()):
            attribs = {}
            attribs['fill'] = self.colored_view.get_color(id)

            xyr = xyrs[i]

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
        return xy.get_midxy(self.get_multipolygon(id))

    def get_label_relative_font_size(self, id):
        relative_font_width = self.palette.get_relative_font_width(
            self.get_multipolygon(id))
        return min(0.8, relative_font_width / len(self.get_label(id)))
