from abc import ABC

from infographics.base import xy
from infographics.core import ColorPaletteVaryHue
from infographics.view.AbstractLabelledView import AbstractLabelledView
from infographics.view.AbstractPolygonView import AbstractPolygonView


class AbstractLabelledPolygonView(
        AbstractLabelledView, AbstractPolygonView, ABC):
    def __init__(self):
        # LabelledView.__init__
        AbstractLabelledView.__init__(self)

        # AbstractPolygonView.__init__
        AbstractPolygonView.__init__(self)

        # other
        self.color_palette = ColorPaletteVaryHue()

    def __xml__(self):
        return self.palette.draw_g([
            AbstractPolygonView.__xml__(self),
            AbstractLabelledView.__xml__(self),
        ])

    # Implement LabelledView
    def get_label_xy(self, id):
        return xy.get_midxy(self.get_multipolygon(id))

    def get_label_relative_font_size(self, id):
        relative_font_width = self.palette.get_relative_font_width(
            self.get_multipolygon(id))
        return min(0.8, relative_font_width / len(self.get_label(id)))
