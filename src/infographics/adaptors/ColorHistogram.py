from functools import cache, cached_property

from utils import colorx


class ColorHistogram:
    def __init__(
        self,
        ids,
        get_id_to_color_value,
        get_color_value_to_label=None,
    ):
        self.ids = ids
        self.get_id_to_color_value = get_id_to_color_value
        self.get_color_value_to_label_specified = get_color_value_to_label

    @cached_property
    def sorted_color_values(self):
        return sorted(list(map(
            lambda id: self.get_id_to_color_value(id),
            self.ids,
        )))

    @cache
    def get_color_values(self, legend_size):
        sorted_color_values = self.sorted_color_values
        n = len(sorted_color_values)
        legend_color_values = []
        for i in range(0, legend_size):
            j = (int)(i * (n - 1) / (legend_size - 1))
            legend_color_values.append(sorted_color_values[j])
        return legend_color_values

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

    def get_color_value_to_color(self, color_value):
        rank_p = self.density_to_rank_p[color_value]
        hue = (1 - rank_p) * 240
        return colorx.random_hsl(hue=hue)

    def get_id_to_color(self, id):
        color_value = self.get_id_to_color_value(id)
        return self.get_color_value_to_color(color_value)

    def get_color_value_to_label(self, color_value):
        if self.get_color_value_to_label_specified:
            return self.get_color_value_to_label_specified(color_value)

        color_value = (int)(round(color_value, 0))
        return f'{color_value:,}'
