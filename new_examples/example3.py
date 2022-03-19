
from infographics.adaptors import ColorBase, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKCensusData, LKGeoData, gig_utils
from infographics.view import LegendView, PolygonView
from new_examples.examples import example_svg_file_name


def main():
    region_id = 'LK'
    subregion_type = 'dsd'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_data = LKCensusData('ethnicity_of_population')

    MAJORITY_LIMIT = 0.55

    def id_to_most_common_ethnicity(id):
        d = lk_census_data[id]
        n_total = d['total_population']
        for color_value, fields in [
            ['sinhalese', ['sinhalese']],
            ['tamil', ['sl_tamil', 'ind_tamil']],
            ['muslim', ['sl_moor', 'malay']],
        ]:
            n = sum([d[field] for field in fields])
            if n > n_total * MAJORITY_LIMIT:
                return color_value
        return 'none'

    def get_color_value_to_color(color_value):
        return {
            'sinhalese': 'maroon',
            'tamil': 'orange',
            'muslim': 'green',
            'none': 'cyan',
        }.get(color_value)

    def get_color_value_to_label(color_value):
        if color_value == 'none':
            return f'No ethnicity with > {MAJORITY_LIMIT:.0%}'
        return color_value.title()

    color_base = ColorBase(
        lk_geodata.keys(),
        id_to_most_common_ethnicity,
        get_color_value_to_color,
    )
    simple_label = SimpleLabel(lk_geodata.get_id_to_name)

    infographic = Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, 'Population Density'),
        'visualization by @nuuuwan',
        children=[
            PolygonView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                color_base.get_id_to_color,
                simple_label.get_id_to_label,
                [],
            ),
            LegendView(
                'Most Common Ethnicity',
                color_base.unique_color_values,
                get_color_value_to_color,
                get_color_value_to_label,
            )
        ]
    )
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
