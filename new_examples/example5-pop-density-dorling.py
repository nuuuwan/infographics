
from infographics.adaptors import (ColorBase, ColorPercentVaryLightness,
                                   SimpleLabel)
from infographics.core import Infographic
from infographics.data import LKCensusEthnicityData, LKGeoData, gig_utils
from infographics.view import DorlingView, LegendView
from new_examples.common import save


def build_infographic():
    region_id = 'LK'
    subregion_type = 'district'
    field_list = ['sl_moor', 'malay']

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_ethnicity_data = LKCensusEthnicityData()

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_census_ethnicity_data.get_get_id_to_p_population(field_list),
        ColorPercentVaryLightness(hue=130).get_color_value_to_color,
    )
    simple_label = SimpleLabel(lk_geodata.get_id_to_name)

    return Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, 'Muslim/Malay Population'),
        'visualization by @nuuuwan',
        children=[
            DorlingView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                color_base.get_id_to_color,
                simple_label.get_id_to_label,
                lk_census_ethnicity_data.get_get_id_to_population(field_list),
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



if __name__ == '__main__':
    save(build_infographic(), __file__)
