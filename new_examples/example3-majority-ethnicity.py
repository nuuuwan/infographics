
from infographics.adaptors import ColorBase, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKCensusEthnicityData, LKGeoData, gig_utils
from infographics.view import LegendView, PolygonView
from new_examples.run_all_examples import example_svg_file_name


def main():
    region_id = 'LK'
    subregion_type = 'dsd'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_ethnicity_data = LKCensusEthnicityData()

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_census_ethnicity_data.id_to_most_common_ethnicity,
        LKCensusEthnicityData.get_color_value_to_color,
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
                LKCensusEthnicityData.get_color_value_to_color,
                LKCensusEthnicityData.get_color_value_to_label,
            )
        ]
    )
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
