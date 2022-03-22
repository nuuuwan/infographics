from functools import cached_property

from utils import colorx

from infographics.adaptors.ColorBase import ColorBase


class ColorHistogram(ColorBase):
    def __init__(
        self,
        ids,
        get_color_value,
    ):
        ColorBase.__init__(
            self,
            ids,
            get_color_value,
            self.get_color_value_to_color,
        )

    @cached_property
    def density_to_rank_p(self):
        n_ids = len(self.ids)
        sorted_color_values = sorted(list(map(
            lambda id: self.get_color_value(id),
            self.ids,
        )))
        return dict(list(map(
            lambda x: [x[1], x[0] / n_ids],
            enumerate(sorted_color_values),
        )))

    def get_color_value_to_color(self, color_value):
        rank_p = self.density_to_rank_p[color_value]
        hue = (1 - rank_p) * 240
        return colorx.random_hsl(hue=hue)
