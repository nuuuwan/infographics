
from infographics.base import xy
from infographics.core import ColorPaletteVaryHue
from infographics.data import LKGeoData
from infographics.view import PolygonView, format


class LKMap(LKGeoData, PolygonView):
    def __init__(
        self,
        region_id='LK',
        subregion_type='district',
        color_palette=ColorPaletteVaryHue(),
    ):
        LKGeoData.__init__(self, region_id, subregion_type)
        multi2polygon = xy.norm_multi2polygon(
            list(map(
                lambda geodata: geodata['multipolygon'],
                self.geodata_index.values(),
            )),
        )

        keys = list(self.geodata_index.keys())
        for i, id in enumerate(keys):
            self.geodata_index[id]['norm_multipolygon'] = multi2polygon[i]

        id_to_multipolygon = dict(list(map(
            lambda x: [x[0], x[1]['norm_multipolygon']],
            self.geodata_index.items(),
        )))

        PolygonView.__init__(
            self,
            id_to_multipolygon,
            self.func_id_to_color,
        )

        self.color_palette = color_palette

    def render_legend(self):
        color_value_list = sorted(list(map(
            self.func_id_to_color_value,
            self.geodata_index.keys(),
        )))

        x0, y0 = 0.8, 0.5
        inner_list = [
            self.palette.draw_text(
                'Density (people per km²)',
                (x0, y0),
                1,
            ),
        ]

        n = len(color_value_list)
        N_LEGEND = 7
        for j in range(0, N_LEGEND):
            i = (int)(j * (n - 1) / (N_LEGEND - 1))
            color_value = color_value_list[i]
            y = y0 - ((j + 1.5) * 0.05)
            color = self.color_palette.color(i / n)

            r = 0.01
            inner_list.append(self.palette.draw_g([
                self.palette.draw_text(
                    format.format_population(color_value),
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

    def render_labels(self):
        inner_list = []
        for id in self.geodata_index:
            inner_list.append(self.palette.draw_g(
                self.func_id_to_child_list(id),
            ))
        return inner_list

    def render_child_list(self):
        return [
            self.render_legend(),
        ] + self.render_labels()

    def func_id_to_color_value(self, id):
        d = self.geodata_index[id]
        d['population']
        return d['population'] / d['area']

    def func_id_to_label(self, id):
        d = self.geodata_index[id]
        return d['name']

    def func_id_to_label_value(self, id):
        d = self.geodata_index[id]
        return d['population']

    def func_id_to_color(self, id):
        color_value_list = sorted(list(map(
            self.func_id_to_color_value,
            self.geodata_index.keys(),
        )))

        n = len(color_value_list)
        color_value_to_i = dict(list(map(
            lambda x: (x[1], x[0]),
            enumerate(color_value_list),
        )))

        color_value = self.func_id_to_color_value(id)
        return self.color_palette.color(
            (color_value_to_i[color_value] / n))

    def func_id_to_polygon(self, id):
        d = self.geodata_index[id]
        return d['norm_multipolygon']

    def func_id_to_child_list(self, id):
        label_value = self.func_id_to_label_value(id)
        label = self.func_id_to_label(id)
        multipolygon = self.func_id_to_polygon(id)

        relative_font_width = self.palette.get_relative_font_width(
            multipolygon)
        relative_font_size = min(0.8, relative_font_width / len(label))

        (x, y) = xy.get_midxy(multipolygon)
        return [
            self.palette.draw_text(
                format.format_population(label_value),
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
