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

        x0, y0 = 0.5, 0.5
        inner_list = [
            self.palette.draw_text(
                'Population Density',
                (x0, y0),
                1,
            ),
        ]

        n = len(density_list)
        for i in range(0, n, (int)(n / 7)):
            density = density_list[i]
            y = y0 - ((i + 3.5) * 0.02)
            hue = (int)(240 * (1 - (i / n)))
            color = colorx.random_hsl(hue=hue)

            inner_list.append(self.palette.draw_g([
                self.palette.draw_cirle(
                    (x0 - 0.035, y),
                    0.01,
                    {'fill': color},
                ),
                self.palette.draw_text(
                    f'{density:0.0f}',
                    (x0 + 0.035, y),
                    1,
                    {'text-anchor': 'end'}
                ),
            ]))

        return inner_list

    def func_id_to_color(self, id):
        density_list = []
        for d0 in self.geodata_index.values():
            population0 = d0['population']
            area0 = d0['area']
            density0 = population0 / area0
            density_list.append(density0)
        density_list.sort()

        n = len(density_list)
        density_to_i = dict(list(map(
            lambda x: (x[1], x[0]),
            enumerate(density_list),
        )))

        d = self.geodata_index[id]
        population = d['population']
        area = d['area']
        density = population / area

        hue = (int)(240 * (1 - (density_to_i[density] / n)))
        return colorx.random_hsl(hue=hue)

    def func_id_to_child_list(self, id):
        d = self.geodata_index[id]
        multipolygon = d['norm_multipolygon']
        name = d['name']
        population = d['population']

        relative_font_width = self.palette.get_relative_font_width(
            multipolygon)
        relative_font_size = min(0.8, relative_font_width / len(name))

        (x, y) = xy.get_midxy(multipolygon)
        return [
            self.palette.draw_text(
                format.format_population(population),
                (x, y + 0.025 * relative_font_size),
                relative_font_size,
                {'font-weight': 'bold'},
            ),
            self.palette.draw_text(
                name,
                (x, y - 0.025 * relative_font_size),
                relative_font_size * 0.8,
            ),
        ]
