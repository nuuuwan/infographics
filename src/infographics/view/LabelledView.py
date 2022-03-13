from abc import ABC

from infographics.core import SVGPalette
from infographics.view import format


class LabelledView(ABC):
    def __init__(
        self,
        keys,
        get_label,
        get_label_value,
        get_label_xy,
        get_label_relative_font_size,
    ):

        self.keys = keys
        self.get_label = get_label
        self.get_label_value = get_label_value
        self.get_label_xy = get_label_xy
        self.get_label_relative_font_size = get_label_relative_font_size

        self.palette = SVGPalette()

    def __xml__(self):
        inner_list = []
        for id in self.keys():
            inner_list.append(
                self.palette.draw_g(
                    self.render_label(id),
                ),
            )
        return self.palette.draw_g(inner_list)

    def render_label(self, id):
        label_value = self.get_label_value(id)
        label = self.get_label(id)
        relative_font_size = self.get_label_relative_font_size(id)
        (x, y) = self.get_label_xy(id)
        return [
            self.palette.draw_text(
                format.as_number(label_value),
                (x, y + 0.025 * relative_font_size),
                relative_font_size,
                {'font-weight': 'bold'},
            ),
            self.palette.draw_text(
                label,
                (x, y - 0.025 * relative_font_size),
                relative_font_size * 0.8,
            ),
        ]
