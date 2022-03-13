from functools import cached_property

from infographics.base import xy
from infographics.core import SVGPalette
from infographics.data import LKGeoData
from infographics.view import PolygonView


class LKMap:
    DEFAULT_CLASS_DATA = LKGeoData
    DEFAULT_VIEW_DATA = PolygonView

    def __init__(
        self,
        region_id,
        subregion_type,
        legend_title,
        color_palette,
        class_data=DEFAULT_CLASS_DATA,
        class_view=DEFAULT_VIEW_DATA,
    ):
        self.region_id = region_id
        self.subregion_type = subregion_type
        self.legend_title = legend_title
        self.color_palette = color_palette
        self.palette = SVGPalette()

        self.class_data = class_data
        self.class_view = class_view

        self.data = self.class_data(
            self.region_id,
            self.subregion_type,
        )
        self.view = self.class_view(
            self.keys,
            self.get_color_value,
            self.legend_title,
            self.color_palette,

            self.get_label,
            self.get_label_value,

            self.id_to_multipolygon,
        )

    def __xml__(self):
        return self.view.__xml__()

    # For View
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

    def keys(self):
        return self.data.lk_geo_data.keys()

    def values(self):
        return self.data.lk_geo_data.values()

    def __getitem__(self, id):
        return self.data.lk_geo_data[id]

    def get_color_value(self, id):
        d = self[id]
        return d['population'] / d['area']

    # For LabelledView
    def get_label(self, id):
        return self[id]['name']

    def get_label_value(self, id):
        return self[id]['population']
