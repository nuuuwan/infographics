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
        latlng_list_list_list = latlng.df_to_latlng_list_list_list(df)
        p_list_list_list = latlng.norm_latlng_list_list_list(
            latlng_list_list_list,
            size=palette.size,
        )
        return p_list_list_list
