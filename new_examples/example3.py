from gig import ent_types, ents

from infographics.base import xy
from infographics.core import Infographic
from infographics.core.SVGPalette import SVGPalette
from infographics.data import LKCensusData, LKGeoData
from infographics.view import LegendView, PolygonView
from new_examples.examples import example_svg_file_name


def main():
    region_id = 'LK-1'
    subregion_type = 'dsd'
    region_ent = ents.get_entity(region_id)
    region_name = region_ent['name']
    region_entity_type = ent_types.get_entity_type(region_id)
    title = f'{region_name} {region_entity_type.upper()}'
    subtitle = f'Population Density by {subregion_type.upper()}'

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

    color_value_to_color = {
        'sinhalese': 'maroon',
        'tamil': 'orange',
        'muslim': 'green',
    }

    id_to_color_value = {}
    for id in lk_geodata:
        d = lk_census_data[id]
        n_sinhala = d['sinhalese']
        n_tamil = d['sl_tamil'] + d['ind_tamil']
        n_muslim = d['sl_moor'] + d['malay']

        n_max = max(n_sinhala, n_tamil, n_muslim)
        max_color_value = 'unknown'
        if n_max == n_sinhala:
            max_color_value = 'sinhalese'
        elif n_max == n_muslim:
            max_color_value = 'muslim'
        elif n_max == n_tamil:
            max_color_value = 'tamil'
        id_to_color_value[id] = max_color_value

    def get_id_to_label(id, cxy, rxy):
        label = lk_geodata[id]['name']
        rx, ry = rxy
        font_size = palette.actual_width * rx / len(label) / 16
        return palette.draw_text(
            label,
            cxy,
            font_size,
        )

    def get_id_to_color(id):
        return id_to_color_value[id]

    color_values = color_value_to_color.keys()

    def get_color_value_to_color(color_value):
        return color_value_to_color[color_value]

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
            )
        ]
    )
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
