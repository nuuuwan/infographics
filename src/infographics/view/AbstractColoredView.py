from abc import ABC, abstractmethod, abstractproperty
from functools import cached_property

from infographics.core import ColorPaletteVaryHue, SVGPalette
from infographics.view import format

N_LEGEND = 7
CIRCLE_R_LEGEND = 0.01


class AbstractColoredView(ABC):
    def __init__(self, legend_title=''):
        self.color_palette = ColorPaletteVaryHue()
        self.palette = SVGPalette()
        self.legend_title = legend_title

    @cached_property
    def color_value_to_i(self):
        color_value_list = sorted(list(map(
            self.get_color_value,
            self.ids,
        )))
        return dict(list(map(
            lambda x: (x[1], x[0]),
            enumerate(color_value_list),
        )))

    def get_color(self, id):
        color_value = self.get_color_value(id)
        n = len(self.color_value_to_i)
        return self.color_palette.color(
            (self.color_value_to_i[color_value] / n))

    def render_row(self, color_value, color, xy):
        x, y = xy
        return self.palette.draw_g([
            self.palette.draw_text(
                format.as_number(color_value),
                (x - 0.01, y),
                1,
                {'text-anchor': 'end'}
            ),
            self.palette.draw_cirle(
                (x + 0.01, y + CIRCLE_R_LEGEND / 2),
                CIRCLE_R_LEGEND,
                {'fill': color},
            ),
        ])

    def __xml__(self):
        x0, y0 = 0.8, 0.5
        inner_list = [
            self.palette.draw_text(self.legend_title, (x0, y0))
        ]

        color_value_list = list(self.color_value_to_i.keys())
        n = len(color_value_list)
        for j in range(0, N_LEGEND):
            i = (int)(j * (n - 1) / (N_LEGEND - 1))
            color_value = color_value_list[i]
            color = self.color_palette.color(i / n)
            y = y0 - ((j + 1.5) * 0.05)
            inner_list.append(self.render_row(color_value, color, (x0, y)))

        return self.palette.draw_g(inner_list)

    # abstract methods

    @abstractproperty
    def ids(self):
        pass

    @abstractmethod
    def get_color_value(self, id):
        pass
