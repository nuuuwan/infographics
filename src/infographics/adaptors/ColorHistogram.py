from functools import cached_property

from utils import colorx


class ColorHistogram:
    def __init__(self, ids, get_id_to_color_value):
        self.ids = ids
        self.get_id_to_color_value = get_id_to_color_value

    @cached_property
    def density_to_rank_p(self):
        n_ids = len(self.ids)
        sorted_color_values = sorted(list(map(
            lambda id: self.get_id_to_color_value(id),
            self.ids,
        )))
        return dict(list(map(
            lambda x: [x[1], x[0] / n_ids],
            enumerate(sorted_color_values),
        )))

    def get_id_to_color(self, id):
        color_value = self.get_id_to_color_value(id)
        rank_p = self.density_to_rank_p[color_value]
        hue = (1 - rank_p) * 240
        return colorx.random_hsl(hue=hue)
