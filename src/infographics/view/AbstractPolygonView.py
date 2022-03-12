"""
Renders a collection of polygons
"""
from abc import ABC, abstractproperty

from infographics.core import ColorPaletteVaryHue, SVGPalette
from infographics.view.AbstractColoredView import AbstractColoredView


class AbstractPolygonView(AbstractColoredView, ABC):
    def __init__(self, legend_title='', color_palette=ColorPaletteVaryHue()):
        # AbstractColoredView.__init__
        AbstractColoredView.__init__(self, legend_title, color_palette)

        # other
        self.palette = SVGPalette()

    def __len__(self):
        return len(self.id_to_multipolygon)

    def get_multipolygon(self, id):
        return self.id_to_multipolygon[id]

    def __xml__(self):
        inner_child_list = []
        for id, multipolygon in self.id_to_multipolygon.items():
            attribs = {}
            if self.get_color:
                attribs['fill'] = self.get_color(id)

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    [],
                    attribs,
                )
            )
        return self.palette.draw_g(
            inner_child_list + [AbstractColoredView.__xml__(self)])

    # abstract methods
    @abstractproperty
    def id_to_multipolygon(self):
        pass
