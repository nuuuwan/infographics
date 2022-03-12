from utils import colorx

from infographics.data import LKGeoData
from infographics.math import latlng
from infographics.view import PolygonView


class LKMap(LKGeoData, PolygonView):
    def __init__(
        self,
        region_id='LK',
        subregion_type='province',
    ):
        LKGeoData.__init__(self, region_id, subregion_type)
        multi2polygon = latlng.norm_multi2polygon(
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
        (x, y) = latlng.get_midlatlng(multipolygon)
        return [self.palette.draw_text(
            name,
            (x, y),
        )]
