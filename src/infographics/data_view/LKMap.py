from utils import colorx

from infographics.base import xy
from infographics.data import LKGeoData
from infographics.view import PolygonView, format


class LKMap(LKGeoData, PolygonView):
    def __init__(
        self,
        region_id='LK',
        subregion_type='district',
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
            self.func_id_to_child_list,
        )

    def get_child_list(self):
        density_list = []
        for d0 in self.geodata_index.values():
            population0 = d0['population']
            area0 = d0['area']
            density0 = population0 / area0
            density_list.append(density0)
        density_list.sort()

        x0, y0 = 0.8, 0.5
        inner_list = [
            self.palette.draw_text(
                'Density (people per km²)',
                (x0, y0),
                1,
            ),
        ]

        n = len(density_list)
        N_LEGEND = 7
        for j in range(0, N_LEGEND):
            i = (int)(j * (n - 1) / (N_LEGEND - 1))
            density = density_list[i]
            y = y0 - ((j + 1.5) * 0.05)
            hue = (int)(240 * (1 - (i / n)))
            color = colorx.random_hsl(hue=hue)

            inner_list.append(self.palette.draw_g([
                self.palette.draw_text(
                    format.format_population(density),
                    (x0 - 0.01, y),
                    1,
                    {'text-anchor': 'end'}
                ),
                self.palette.draw_cirle(
                    (x0 + 0.01, y),
                    0.01,
                    {'fill': color},
                ),
            ]))

        return inner_list

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
        hue = (int)(240 * (1 - (color_value_to_i[color_value] / n)))
        return colorx.random_hsl(hue=hue)

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
