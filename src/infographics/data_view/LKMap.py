
from infographics.base import xy
from infographics.core import ColorPaletteVaryHue
from infographics.data import LKGeoData
from infographics.view import LabelledView, PolygonView, format


class LKMap(LKGeoData, PolygonView, LabelledView):
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

        # PolygonView.__init__
        PolygonView.__init__(
            self,
            id_to_multipolygon,
            self.get_polygon_color,
        )

        # other
        self.color_palette = color_palette

        # pre-processing
        color_value_list = sorted(list(map(
            self.get_polygon_color_value,
            self.geodata_index.keys(),
        )))

        self.color_value_to_i = dict(list(map(
            lambda x: (x[1], x[0]),
            enumerate(color_value_list),
        )))

    def get_multipolygon(self, id):
        d = self.geodata_index[id]
        return d['norm_multipolygon']

    # polygon labels
    def get_label(self, id):
        d = self.geodata_index[id]
        return d['name']

    def get_label_value(self, id):
        d = self.geodata_index[id]
        return d['population']

    # polygon colors
    def get_polygon_color_value(self, id):
        d = self.geodata_index[id]
        d['population']
        return d['population'] / d['area']

    def get_polygon_color(self, id):
        color_value = self.get_polygon_color_value(id)
        n = len(self.color_value_to_i)
        return self.color_palette.color(
            (self.color_value_to_i[color_value] / n))

    def render_legend(self):
        x0, y0 = 0.8, 0.5
        inner_list = [
            self.palette.draw_text(
                'Density (people per km²)',
                (x0, y0),
                1,
            ),
        ]

        color_value_list = list(self.color_value_to_i.keys())
        n = len(color_value_list)
        N_LEGEND = 7
        for j in range(0, N_LEGEND):
            i = (int)(j * (n - 1) / (N_LEGEND - 1))
            color_value = color_value_list[i]
            y = y0 - ((j + 1.5) * 0.05)
            color = self.color_palette.color(i / n)

            r = 0.01
            inner_list.append(self.palette.draw_g([
                self.palette.draw_text(
                    format.as_number(color_value),
                    (x0 - 0.01, y),
                    1,
                    {'text-anchor': 'end'}
                ),
                self.palette.draw_cirle(
                    (x0 + 0.01, y + r / 2),
                    r,
                    {'fill': color},
                ),
            ]))
        return self.palette.draw_g(inner_list)

    def __xml__(self):
        return self.palette.draw_g([
            PolygonView.__xml__(self),
            self.render_labels(),
            self.render_legend(),
        ])
