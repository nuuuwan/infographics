from functools import cached_property

from geo import geodata

from infographics._utils import log
from infographics.base import pandax


class LKGeoData:
    def __init__(self, region_id, subregion_type):
        self.region_id = region_id
        self.subregion_type = subregion_type

    @cached_property
    def idx(self):
        log.debug('[expensive] geodata.get_region_geodata')
        df = geodata.get_region_geodata(
            self.region_id,
            self.subregion_type,
        )
        geodata_index = pandax.df_to_geodata_index(df)
        return geodata_index

    def __len__(self):
        return len(self.idx)

    def __getitem__(self, id):
        return self.idx[id]

    def keys(self):
        return self.idx.keys()

    def values(self):
        return self.idx.values()

    def __iter__(self):
        for id in self.keys():
            yield id
