from abc import ABC

from infographics.base import xy
from infographics.view.AbstractPolygonView import AbstractPolygonView
from infographics.view.LabelledView import LabelledView


class AbstractLabelledPolygonView(AbstractPolygonView, ABC):
    DEFAULT_CLASS_LABELLED_VIEW = LabelledView

    def __init__(
        self,
        legend_title,
        color_palette,
        class_labelled_view=DEFAULT_CLASS_LABELLED_VIEW,
    ):
        AbstractPolygonView.__init__(self, legend_title, color_palette)

        self.labelled_view = class_labelled_view(
            self.keys,
            self.get_label,
            self.get_label_value,
            self.get_label_xy,
            self.get_label_relative_font_size,
        )

    def __xml__(self):
        return self.palette.draw_g([
            AbstractPolygonView.__xml__(self),
            self.labelled_view.__xml__(),
        ])

    # Implement LabelledView
    def get_label_xy(self, id):
        return xy.get_midxy(self.get_multipolygon(id))

    def get_label_relative_font_size(self, id):
        relative_font_width = self.palette.get_relative_font_width(
            self.get_multipolygon(id))
        return min(0.8, relative_font_width / len(self.get_label(id)))
