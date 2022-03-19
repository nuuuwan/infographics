from gig import ent_types, ents
from utils import colorx

from infographics.base import xy
from infographics.core import Infographic
from infographics.core.SVGPalette import SVGPalette
from infographics.data import LKCensusData, LKGeoData
from infographics.view import LegendView, PolygonView
from new_examples.examples import example_svg_file_name


def main():
    region_id = 'LK'
    subregion_type = 'dsd'
    region_ent = ents.get_entity(region_id)
    region_name = region_ent['name']
    region_entity_type = ent_types.get_entity_type(region_id)
    # current_hue = 120
    current_hue = 30
    # ethnicity_fields = ['sl_moor', 'malay']
    ethnicity_fields = ['sl_tamil', 'ind_tamil']
    title = f'{region_name} {region_entity_type.upper()}'
    ethnicity_fields_label = '/'.join(list(map(
        lambda x: ' '.join(list(map(
            lambda x2: x2.title(),
            x.split('_'),
        ))),
        ethnicity_fields,
    )))
    subtitle = f'{ethnicity_fields_label}' + \
        f' Population by {subregion_type.upper()}'

    palette = SVGPalette()
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
    lk_census_data = LKCensusData(
        table_id='ethnicity_of_population',
    ).data

    color_metadata = [
        (0.9, None, 0.2),
        (0.7, 0.9, 0.36),
        (0.5, 0.7, 0.52),
        (0.3, 0.5, 0.68),
        (0.1, 0.3, 0.84),
        (None, 0.1, 1),
    ]

    def get_id_to_color(id):
        d = lk_census_data[id]
        pop_current = sum(list(map(
            lambda field: d.get(field, 0),
            ethnicity_fields,
        )))
        pop_total = d['total_population']
        p = pop_current / pop_total
        for min_value, max_value, lightness in color_metadata:
            if min_value and min_value > p:
                continue
            if max_value and max_value <= p:
                continue
            return colorx.random_hsl(hue=current_hue, lightness=lightness)
        return 'gray'

    def get_id_to_label(id, cxy, rxy):
        label = lk_geodata[id]['name']
        rx, ry = rxy
        font_size = palette.actual_width * rx / len(label) / 16
        return palette.draw_text(
            label,
            cxy,
            font_size,
        )

    def get_color_value(x):
        min_value, max_value, color = x
        connector = ' - ' if (min_value and max_value) else ' '
        min_value = min_value if min_value else '<'
        max_value = max_value if max_value else '<'
        return f'{min_value}{connector}{max_value}'

    color_value_to_color = dict(list(map(
        lambda x: (
            get_color_value(x),
            colorx.random_hsl(hue=current_hue, lightness=x[2]),
        ),
        color_metadata,
    )))
    color_values = color_value_to_color.keys()

    def get_color_value_to_color(color_value):
        return color_value_to_color[color_value]

    def get_color_value_to_label(color_value):
        return color_value

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
