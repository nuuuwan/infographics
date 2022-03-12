from geo import geodata

from infographics.base import xy, pandax


class LKGeoData:
    def __init__(self, region_id, subregion_type):
        self.region_id = region_id
        self.subregion_type = subregion_type
        self.geodata_index = self.get_geodata_index()

    def get_geodata_index(self):
        df = geodata.get_region_geodata(
            self.region_id,
            self.subregion_type,
        )
        geodata_index = pandax.df_to_geodata_index(df)
        return geodata_index
