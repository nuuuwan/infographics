from functools import cache, cached_property


class ColorBase:
    def __init__(
        self,
        ids,
        get_id_to_color_value,
        get_color_value_to_color,
    ):
        self.ids = ids
        self.get_id_to_color_value = get_id_to_color_value
        self.get_color_value_to_color = get_color_value_to_color

    @cached_property
    def color_values(self):
        return list(map(
            lambda id: self.get_id_to_color_value(id),
            self.ids,
        ))

    @cached_property
    def sorted_color_values(self):
        return sorted(self.color_values)

    @cached_property
    def unique_color_values(self):
        return list(set(self.color_values))

    @cache
    def get_color_values(self, legend_size):
        sorted_color_values = self.sorted_color_values
        n = len(sorted_color_values)
        legend_color_values = []
        for i in range(0, legend_size):
            j = (int)(i * (n - 1) / (legend_size - 1))
            legend_color_values.append(sorted_color_values[j])
        return legend_color_values

    def get_id_to_color(self, id):
        color_value = self.get_id_to_color_value(id)
        return self.get_color_value_to_color(color_value)

    def get_color_value_to_int_label(self, color_value):
        color_value = (int)(round(color_value, 0))
        return f'{color_value:,}'
