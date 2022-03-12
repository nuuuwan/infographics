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

    def func_id_to_color(self, id):
        return colorx.random_hex()

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
            ),
            self.palette.draw_text(
                name,
                (x, y - 0.025 * relative_font_size),
                relative_font_size * 0.8,
            ),

        ]
