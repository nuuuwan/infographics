from infographics.base import xy
from infographics.core import Infographic
from infographics.core.SVGPalette import SVGPalette
from infographics.data import LKGeoData
from infographics.view import PolygonView
from new_examples.examples import example_svg_file_name


def main():
    palette = SVGPalette()
    lk_geodata = LKGeoData(
        region_id='LK',
        subregion_type='district',
    ).data
    multi2polygon = list(map(lambda d: d['multipolygon'], lk_geodata.values()))
    norm_multi2polygon = xy.get_norm_multi2polygon(multi2polygon)
    for i, id in enumerate(list(lk_geodata.keys())):
        lk_geodata[id]['norm_multipolygon'] = norm_multi2polygon[i]

    def get_id_to_norm_multipolygon(id):
        return lk_geodata[id]['norm_multipolygon']

    def get_id_to_color(id):
        d = lk_geodata[id]
        density = d['population'] / d['area']
        if density > 1000:
            return 'red'
        if density > 500:
            return 'orange'
        if density > 250:
            return 'yellow'
        if density > 125:
            return 'green'
        return 'blue'

    def get_id_to_label(id, cxy, rxy):
        label = lk_geodata[id]['name']
        rx, ry = rxy
        font_size = palette.actual_width * rx / len(label) / 16
        return palette.draw_text(
            label,
            cxy,
            font_size,
        )

    infographic = Infographic(
        title='Population & Population Density',
        subtitle='Provinces of Sri Lanka',
        footer_text='visualization by @nuuuwan',
        children=[
            PolygonView(
                ids=lk_geodata.keys(),
                get_id_to_norm_multipolygon=get_id_to_norm_multipolygon,
                get_id_to_color=get_id_to_color,
                get_id_to_label=get_id_to_label,
                children=[],
            )
        ]
    )
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
