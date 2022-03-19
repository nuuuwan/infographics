
from infographics.adaptors import ColorHistogram, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKGeoData, gig_utils
from infographics.view import LegendView, PolygonView
from new_examples.examples import example_svg_file_name

LEGEND_SIZE = 7


def main():
    region_id = 'LK'
    subregion_type = 'district'

    title = gig_utils.get_region_full_name(region_id)
    subtitle = f'Population Density by {subregion_type.upper()}'

    lk_geodata = LKGeoData(region_id, subregion_type)
    color_histogram = ColorHistogram(
        lk_geodata.keys(),
        lk_geodata.get_id_to_population_density,
    )
    simple_label = SimpleLabel(lk_geodata.get_id_to_name)

    infographic = Infographic(
        title,
        subtitle,
        'visualization by @nuuuwan',
        [
            PolygonView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                color_histogram.get_id_to_color,
                simple_label.get_id_to_label,
                [],
            ),
            LegendView(
                'Persons per km²',
                color_histogram.get_color_values(LEGEND_SIZE),
                color_histogram.get_color_value_to_color,
                color_histogram.get_color_value_to_label,
            )
        ])
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
