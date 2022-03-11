from geo import geodata

from infographics.core import SVGPalette
from infographics.math import latlng


class LKMap():
    @property
    def xml(self):
        palette = SVGPalette()
        df = geodata.get_region_geodata(
            'LK-11',
            'dsd',
        )
        latlng_list_list_list = latlng.df_to_latlng_list_list(df)
        p_list_list_list = latlng.norm_latlng_list_list_list(
            latlng_list_list_list,
            size=palette.size,
        )
        return palette.draw_p_list_list_list(p_list_list_list)
