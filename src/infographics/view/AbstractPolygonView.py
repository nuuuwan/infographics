"""
Renders a collection of polygons
"""
from abc import ABC, abstractproperty

from infographics.core import SVGPalette
from infographics.view.ColoredView import ColoredView


class AbstractPolygonView(ABC):
    DEFAULT_CLASS_COLORED_VIEW = ColoredView

    def __init__(
        self,
        legend_title,
        color_palette,
        class_colored_view=DEFAULT_CLASS_COLORED_VIEW,
    ):
        self.legend_title = legend_title
        self.color_palette = color_palette

        self.colored_view = class_colored_view(
            self.keys,
            self.get_color_value,
            self.legend_title,
            self.color_palette,
        )
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
            inner_child_list + [self.colored_view.__xml__()])

    # abstract methods
    @abstractproperty
    def id_to_multipolygon(self):
        pass
