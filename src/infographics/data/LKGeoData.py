from functools import cache

from geo import geodata

from infographics._utils import log
from infographics.base import pandax, xy

log.debug('[?expensive] from geo import geodata...')


class LKGeoData:
    def __init__(
        self,
        region_id,
        subregion_type,
    ):
        self.region_id = region_id
        self.subregion_type = subregion_type

    @cache
    def get_data(self):
        log.debug('[expensive] geodata.get_region_geodata...')
        df = geodata.get_region_geodata(
            self.region_id,
            self.subregion_type,
        )
        geodata_index = pandax.df_to_geodata_index(df)
        return geodata_index

    @cache
    def get_norm_data(self):
        data = self.get_data()
        multi2polygon = list(map(lambda d: d['multipolygon'], data.values()))
        norm_multi2polygon = xy.get_norm_multi2polygon(multi2polygon)
        for i, id in enumerate(list(data.keys())):
            data[id]['norm_multipolygon'] = norm_multi2polygon[i]
        return data
