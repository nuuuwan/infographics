from abc import ABC, abstractmethod

from infographics.core import ColorPaletteVaryHue, SVGPalette
from infographics.view import format

N_LEGEND = 7


class AbstractColoredView(ABC):
    def __init__(self, legend_title=''):
        self.color_palette = ColorPaletteVaryHue()
        self.legend_title = legend_title
        self.palette = SVGPalette()

        # pre-processing
        color_value_list = sorted(list(map(
            self.get_color_value,
            self.geodata_index.keys(),
        )))

        self.color_value_to_i = dict(list(map(
            lambda x: (x[1], x[0]),
            enumerate(color_value_list),
        )))

    def get_color(self, id):
        color_value = self.get_color_value(id)
        n = len(self.color_value_to_i)
        return self.color_palette.color(
            (self.color_value_to_i[color_value] / n))

    def __xml__(self):
        x0, y0 = 0.8, 0.5
        inner_list = [
            self.palette.draw_text(
                self.legend_title,
                (x0, y0),
                1,
            ),
        ]

        color_value_list = list(self.color_value_to_i.keys())
        n = len(color_value_list)
        for j in range(0, N_LEGEND):
            i = (int)(j * (n - 1) / (N_LEGEND - 1))
            color_value = color_value_list[i]
            y = y0 - ((j + 1.5) * 0.05)
            color = self.color_palette.color(i / n)

            r = 0.01
            inner_list.append(self.palette.draw_g([
                self.palette.draw_text(
                    format.as_number(color_value),
                    (x0 - 0.01, y),
                    1,
                    {'text-anchor': 'end'}
                ),
                self.palette.draw_cirle(
                    (x0 + 0.01, y + r / 2),
                    r,
                    {'fill': color},
                ),
            ]))
        return self.palette.draw_g(inner_list)

    @abstractmethod
    def get_color_value(self, id):
        pass
