from infographics.base import xy
from infographics.core import SVGPalette
from infographics.view import format


class LabelledView:
    def __init__(self):
        self.palette = SVGPalette()

    def render_labels(self):
        inner_list = []
        for id in self.get_label_ids():
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

    # abstract methods
    def get_label_ids(self):
        return list(self.geodata_index.keys())

    def get_label(self, id):
        d = self.geodata_index[id]
        return d['name']

    def get_label_value(self, id):
        d = self.geodata_index[id]
        return d['population']

    def get_label_xy(self, id):
        multipolygon = self.get_multipolygon(id)
        return xy.get_midxy(multipolygon)

    def get_label_relative_font_size(self, id):
        label = self.get_label(id)
        multipolygon = self.get_multipolygon(id)
        relative_font_width = self.palette.get_relative_font_width(
            multipolygon)
        return min(0.8, relative_font_width / len(label))
