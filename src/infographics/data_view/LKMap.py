
from infographics.data import LKGeoData
from infographics.view import PointMap


class LKMap(LKGeoData, PointMap):
    def __init__(
        self,
        region_id='LK',
        subregion_type='province',
    ):
        LKGeoData.__init__(self, region_id, subregion_type)
        PointMap.__init__(self, self.data)
