from functools import cached_property

from infographics.base import xy
from infographics.core import ColorPaletteVaryHue
from infographics.data import LKGeoData
from infographics.view import AbstractLabelledPolygonView


class LKMap(LKGeoData, AbstractLabelledPolygonView):
    def __init__(
        self,
        region_id='LK',
        subregion_type='district',
        legend_title='Population Density (people per km²)',
    ):
        # LKGeoData.__init__
        LKGeoData.__init__(self, region_id, subregion_type)

        # AbstractLabelledPolygonView.__init__
        AbstractLabelledPolygonView.__init__(self)

        # other
        self.legend_title = legend_title
        self.color_palette = ColorPaletteVaryHue()

    # Implement AbstractColoredView
    def get_color_value(self, id):
        d = self.get_geodata(id)
        return d['population'] / d['area']

    def get_legend_title(self):
        return self.legend_title

    # Implement AbstractLabelledView
    @property
    def ids(self):
        return list(self.geodata_index.keys())

    def get_label(self, id):
        return self.get_geodata(id)['name']

    def get_label_value(self, id):
        return self.get_geodata(id)['population']

    # Implement AbstractPolygonView
    @cached_property
    def id_to_multipolygon(self):
        multi2polygon = xy.norm_multi2polygon(
            list(map(
                lambda geodata: geodata['multipolygon'],
                self.geodata_index.values(),
            )),
        )
        id_to_multipolygon = {}
        keys = list(self.geodata_index.keys())
        for i, id in enumerate(keys):
            id_to_multipolygon[id] = multi2polygon[i]
        return id_to_multipolygon
