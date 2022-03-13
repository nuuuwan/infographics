from functools import cached_property

from infographics.core import SVGPalette
from infographics.view import format

N_LEGEND = 7
CIRCLE_R_LEGEND = 0.01

DEFAULT_COLOR = 'lightgray'
KEY_TO_COLOR_VALUE = {
    'sinhalese': '#8d153a',
    'sl_tamil': '#eb7400',
    'sl_moor': '#00534e',
    'buddhist': '#ffbe29',
}


class ColoredView:
    def __init__(
        self,
        keys,
        get_color_value,
        legend_title,
        color_palette,

    ):
        self.keys = keys
        self.get_color_value = get_color_value
        self.legend_title = legend_title
        self.color_palette = color_palette

        self.palette = SVGPalette()

    @cached_property
    def color_value_to_i(self):
        color_value_list = sorted(list(map(
            self.get_color_value,
            self.keys(),
        )))

        if isinstance(color_value_list[0], str):
            color_value_list = list(set(color_value_list))

        return dict(list(map(
            lambda x: (x[1], x[0]),
            enumerate(color_value_list),
        )))

    def get_color(self, id):
        color_value = self.get_color_value(id)

        if isinstance(color_value, str):
            return KEY_TO_COLOR_VALUE.get(color_value, DEFAULT_COLOR)

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
            self.palette.draw_circle(
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
        prev_i = None
        k = 0
        for j in range(0, N_LEGEND):
            i = (int)(j * (n - 1) / (N_LEGEND - 1))
            if i == prev_i:
                continue
            color_value = color_value_list[i]
            if isinstance(color_value, str):
                color = KEY_TO_COLOR_VALUE.get(color_value, DEFAULT_COLOR)
            else:
                color = self.color_palette.color(i / n)

            y = y0 - ((k + 1.5) * 0.05)
            inner_list.append(self.render_row(color_value, color, (x0, y)))
            prev_i = i
            k += 1

        return self.palette.draw_g(inner_list)
