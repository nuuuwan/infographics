from geo import geodata

from infographics.core import SVGPalette
from infographics.math import latlng


class LKGeoData:
    def __init__(self, region_id, subregion_type):
        self.region_id = region_id
        self.subregion_type = subregion_type

    @property
    def data(self):
        palette = SVGPalette()
        df = geodata.get_region_geodata(
            self.region_id,
            self.subregion_type,
        )
        multi2polygon = latlng.df_to_multi2polygon(df)
        multi2polygon = latlng.norm_multi2polygon(
            multi2polygon,
            size=palette.size,
        )
        return multi2polygon
