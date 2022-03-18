from gig import ent_types, ents

from infographics.base import xy
from infographics.core import Infographic
from infographics.core.SVGPalette import SVGPalette
from infographics.data import LKGeoData
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

    color_metadata = [
        (2000, None, 'maroon'),
        (1000, 2000, 'red'),
        (500, 1000, 'orange'),
        (250, 500, 'yellow'),
        (125, 250, 'green'),
        (None, 125, 'blue'),
    ]

    def get_id_to_color(id):
        d = lk_geodata[id]
        density = d['population'] / d['area']
        for min_value, max_value, color in color_metadata:
            if min_value and min_value > density:
                continue
            if max_value and max_value <= density:
                continue
            return color
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
        lambda x: (get_color_value(x), x[2]),
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
