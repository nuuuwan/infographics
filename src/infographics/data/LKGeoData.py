from functools import cached_property

from geo import geodata

from infographics._utils import log
from infographics.base import pandax


class LKGeoData:
    DEFAULT_REGION_ID = 'LK'
    DEFAULT_SUBREGION_TYPE = 'province'

    def __init__(
        self,
        region_id=DEFAULT_REGION_ID,
        subregion_type=DEFAULT_SUBREGION_TYPE,
    ):
        self.region_id = region_id
        self.subregion_type = subregion_type

    @cached_property
    def lk_geo_data(self):
        log.debug('[expensive] geodata.get_region_geodata')
        df = geodata.get_region_geodata(
            self.region_id,
            self.subregion_type,
        )
        geodata_index = pandax.df_to_geodata_index(df)
        return geodata_index
