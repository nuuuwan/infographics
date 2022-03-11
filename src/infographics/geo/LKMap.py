from geo import geodata
from utils import ds
from infographics.core import SVGPalette


class LKMap():
    @property
    def xml(self):
        palette = SVGPalette()
        df = geodata.get_region_geodata(
            'LK',
            'district',
        )
        latlng_list_list_list = []
        for row in df.itertuples():
            multi_polygon_list.append(row.geometry)

        return palette.draw_text('TODO')
