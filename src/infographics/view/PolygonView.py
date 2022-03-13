from abc import ABC

from infographics.base import xy
from infographics.core import SVGPalette
from infographics.view.ColoredView import ColoredView
from infographics.view.LabelledView import LabelledView


class PolygonView(ABC):
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
        for id, multipolygon in self.id_to_multipolygon.items():
            attribs = {}
            attribs['fill'] = self.colored_view.get_color(id)

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    [],
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
