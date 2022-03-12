
from infographics.data import LKGeoData
from infographics.view import PolygonView


class LKMap(LKGeoData, PolygonView):
    def __init__(
        self,
        region_id='LK',
        subregion_type='province',
    ):
        LKGeoData.__init__(self, region_id, subregion_type)
        PolygonView.__init__(self, self.data)
