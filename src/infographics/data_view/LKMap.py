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

        # geodata_index
        self.geodata_index = self.get_geodata_index()
        multi2polygon = xy.norm_multi2polygon(
            list(map(
                lambda geodata: geodata['multipolygon'],
                self.geodata_index.values(),
            )),
        )

        keys = list(self.geodata_index.keys())
        for i, id in enumerate(keys):
            self.geodata_index[id]['norm_multipolygon'] = multi2polygon[i]

        id_to_multipolygon = dict(list(map(
            lambda x: [x[0], x[1]['norm_multipolygon']],
            self.geodata_index.items(),
        )))

        # AbstractLabelledPolygonView.__init__
        AbstractLabelledPolygonView.__init__(
            self, legend_title, id_to_multipolygon)

        # other
        self.color_palette = ColorPaletteVaryHue()

    # Implement AbstractColoredView
    def get_color_value(self, id):
        d = self.geodata_index[id]
        return d['population'] / d['area']

    # Implement LabelledView
    def get_label_ids(self):
        return list(self.geodata_index.keys())

    def get_label(self, id):
        d = self.geodata_index[id]
        return d['name']

    def get_label_value(self, id):
        d = self.geodata_index[id]
        return d['population']
