
from infographics.base import xy
from infographics.core import ColorPaletteVaryHue
from infographics.data import LKGeoData
from infographics.view import LabelledView, ColoredView, PolygonView


class LKMap(LKGeoData, PolygonView, LabelledView, ColoredView):
    def __init__(
        self,
        region_id='LK',
        subregion_type='district',
        color_palette=ColorPaletteVaryHue(),
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

        # ColoredView.__init__
        ColoredView.__init__(self, 'Density (people per km²)')

        # PolygonView.__init__
        PolygonView.__init__(self, id_to_multipolygon)

        # other
        self.color_palette = color_palette

    def __xml__(self):
        return self.palette.draw_g([
            PolygonView.__xml__(self),
            self.render_labels(),
            self.render_legend(),
        ])
