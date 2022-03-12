from functools import cached_property

from infographics.base import xy
from infographics.data import LKGeoData
from infographics.view import AbstractColoredView, AbstractLabelledPolygonView


class LKMap(LKGeoData, AbstractLabelledPolygonView):
    DEFAULT_LEGEND_TITLE = 'Population Density (people per km²)'

    def __init__(
        self,
        region_id=LKGeoData.DEFAULT_REGION_ID,
        subregion_type=LKGeoData.DEFAULT_SUBREGION_TYPE,
        legend_title=AbstractColoredView.DEFAULT_LEGEND_TITLE,
        color_palette=AbstractColoredView.DEFAULT_COLOR_PALETTE,
    ):
        # LKGeoData.__init__
        LKGeoData.__init__(self, region_id, subregion_type)

        # AbstractLabelledPolygonView.__init__
        AbstractLabelledPolygonView.__init__(self, legend_title, color_palette)

    # Implement AbstractPolygonView
    @cached_property
    def id_to_multipolygon(self):
        multi2polygon = xy.norm_multi2polygon(
            list(map(
                lambda geodata: geodata['multipolygon'],
                self.values(),
            )),
        )
        id_to_multipolygon = {}
        for i, id in enumerate(self.keys()):
            id_to_multipolygon[id] = multi2polygon[i]
        return id_to_multipolygon

    # Implement AbstractColoredView
    def keys(self):
        return self.lk_geo_data.keys()

    def values(self):
        return self.lk_geo_data.values()

    def __getitem__(self, id):
        return self.lk_geo_data[id]    

    def get_color_value(self, id):
        d = self[id]
        return d['population'] / d['area']

    # Implement AbstractLabelledView
    def get_label(self, id):
        return self[id]['name']

    def get_label_value(self, id):
        return self[id]['population']
