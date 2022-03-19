from gig import ent_types, ents

from infographics.adaptors import ColorHistogram, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKGeoData
from infographics.view import LegendView, PolygonView
from new_examples.examples import example_svg_file_name

LEGEND_SIZE = 7


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
    )

    def get_id_to_color_value(id):
        d = lk_geodata[id]
        return d['population'] / d['area']
    color_histogram = ColorHistogram(
        ids=lk_geodata.keys(),
        get_id_to_color_value=get_id_to_color_value,
    )
    simple_label = SimpleLabel(lk_geodata.get_id_to_name)

    infographic = Infographic(
        title=title,
        subtitle=subtitle,
        footer_text='visualization by @nuuuwan',
        children=[
            PolygonView(
                ids=lk_geodata.keys(),
                get_id_to_norm_multipolygon=(
                    lk_geodata.get_id_to_norm_multipolygon),
                get_id_to_color=color_histogram.get_id_to_color,
                get_id_to_label=simple_label.get_id_to_label,
                children=[],
            ),
            LegendView(
                legend_title='Persons per km²',
                color_values=color_histogram.get_legend_color_values(LEGEND_SIZE),
                get_color_value_to_color=(
                    color_histogram.get_color_value_to_color),
                get_color_value_to_label=(
                    color_histogram.get_color_value_to_label),
            )])
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
