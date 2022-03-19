
from infographics.adaptors import (ColorBase, ColorPercentVaryLightness,
                                   SimpleLabel)
from infographics.core import Infographic
from infographics.data import LKCensusEthnicityData, LKGeoData, gig_utils
from infographics.view import LegendView, PolygonView
from new_examples.run_all_examples import save


def main():
    region_id = 'LK'
    subregion_type = 'dsd'
    field_list = ['sl_tamil', 'ind_tamil']

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_ethnicity_data = LKCensusEthnicityData()

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_census_ethnicity_data.get_get_id_to_p_population(field_list),
        ColorPercentVaryLightness(hue=30).get_color_value_to_color,
    )
    simple_label = SimpleLabel(lk_geodata.get_id_to_name)

    infographic = Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, 'Tamil Population'),
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
                '% of Population',
                color_base.get_color_values(),
                color_base.get_color_value_to_color,
                color_base.get_color_value_to_percent_label,
            )
        ]
    )
    save(infographic, __file__)


if __name__ == '__main__':
    main()
