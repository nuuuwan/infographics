from utils import colorx

from infographics.core import SVGPalette
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

        geodata_list = self.geodata_list
        SVGPalette().size

        multi2polygon = latlng.norm_multi2polygon(list(map(
            lambda geodata: geodata['multipolygon'],
            geodata_list,
        )))

        id_to_multipolygon = dict(list(map(
            lambda x: [
                x[1]['id'],
                multi2polygon[x[0]],
            ],
            enumerate(geodata_list),
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
        return []
