from gig import ent_types, ents
from utils import colorx

from infographics.base import xy
from infographics.core import Infographic
from infographics.core.SVGPalette import SVGPalette
from infographics.data import LKGeoData
from infographics.view import LegendView, PolygonView
from new_examples.examples import example_svg_file_name


def main():
    region_id = 'LK'
    subregion_type = 'district'
    region_ent = ents.get_entity(region_id)
    region_name = region_ent['name']
    region_entity_type = ent_types.get_entity_type(region_id)
    title = f'{region_name} {region_entity_type.upper()}'
    subtitle = f'Population Density by {subregion_type.upper()}'

    lk_geodata = LKGeoData(
        region_id=region_id,
        subregion_type=subregion_type,
    ).data
    multi2polygon = list(map(lambda d: d['multipolygon'], lk_geodata.values()))
    norm_multi2polygon = xy.get_norm_multi2polygon(multi2polygon)
    for i, id in enumerate(list(lk_geodata.keys())):
        lk_geodata[id]['norm_multipolygon'] = norm_multi2polygon[i]

    def get_id_to_norm_multipolygon(id):
        return lk_geodata[id]['norm_multipolygon']

    ids = lk_geodata.keys()
    n_ids = len(ids)
    sorted_density_list = sorted(list(map(
        lambda id: lk_geodata[id]['population'] / lk_geodata[id]['area'],
        ids,
    )))
    density_to_rank_p = dict(list(map(
        lambda x: [x[1], x[0] / n_ids],
        enumerate(sorted_density_list),
    )))

    def get_id_to_color(id):
        d = lk_geodata[id]
        density = d['population'] / d['area']
        rank_p = density_to_rank_p[density]
        hue = (1 - rank_p) * 240
        return colorx.random_hsl(hue=hue)

    palette = SVGPalette()        
    def get_id_to_label(id, cxy, rxy):
        label = lk_geodata[id]['name']
        rx, ry = rxy
        font_size = palette.actual_width * rx / len(label) / 16
        return palette.draw_text(
            label,
            cxy,
            font_size,
        )

    color_values = []
    LEGEND_SIZE = 7
    for i in range(0, LEGEND_SIZE):
        j = (int)(i * (n_ids - 1) / (LEGEND_SIZE - 1))
        color_values.append(sorted_density_list[j])

    def get_color_value_to_color(color_value):
        rank_p = density_to_rank_p[color_value]
        hue = (1 - rank_p) * 240
        return colorx.random_hsl(hue=hue)

    def get_color_value_to_label(color_value):
        color_value = (int)(round(color_value, 0))
        return f'{color_value:,}'

    infographic = Infographic(
        title=title,
        subtitle=subtitle,
        footer_text='visualization by @nuuuwan',
        children=[
            PolygonView(
                ids=lk_geodata.keys(),
                get_id_to_norm_multipolygon=get_id_to_norm_multipolygon,
                get_id_to_color=get_id_to_color,
                get_id_to_label=get_id_to_label,
                children=[],
            ),
            LegendView(
                legend_title='Persons per km²',
                color_values=color_values,
                get_color_value_to_color=get_color_value_to_color,
                get_color_value_to_label=get_color_value_to_label,
            )
        ]
    )
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
