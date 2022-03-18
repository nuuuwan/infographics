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
        ids,
        get_id_to_multipolygon,
        get_id_to_color,
        get_id_to_label,
        children=[],
    ):
        self.ids = ids
        self.get_id_to_multipolygon = get_id_to_multipolygon
        self.get_id_to_color = get_id_to_color
        self.get_id_to_label = get_id_to_label
        self.children = children
        self.palette = SVGPalette()

    def __xml__(self):
        inner_child_list = []
        for id in self.ids:
            multipolygon = self.get_id_to_multipolygon(id)
            attribs = {'fill': self.get_id_to_color(id)}

            inner_child_list.append(
                self.palette.draw_multipolygon(
                    multipolygon,
                    [],
                    attribs,
                )
            )

        for id in self.ids:
            multipolygon = self.get_id_to_multipolygon(id)
            (cx, cy), (rx, ry) = xy.get_cxcyrxry(multipolygon)
            inner_child_list.append(
                self.get_id_to_label(id, (cx, cy), (rx, ry)),
            )

        return self.palette.draw_g(
            inner_child_list,
            self.children,
        )
