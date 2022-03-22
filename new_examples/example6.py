
from infographics.adaptors import SimpleLabel
from infographics.core import Infographic
from infographics.data import (LKCensusEthnicityData, LKCensusReligionData,
                               LKGeoData, gig_utils)
from infographics.view import FlagDorlingView, LegendView

if __name__ == '__main__':
    region_id = 'LK'
    subregion_type = 'province'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_ethnicity_data = LKCensusEthnicityData()
    lk_census_religion_data = LKCensusReligionData()

    def get_id_to_flag_data(id):
        d_eth = lk_census_ethnicity_data[id]
        d_rel = lk_census_religion_data[id]

        n_sinhala = d_eth['sinhalese']
        n_muslim = d_eth['sl_moor'] + d_eth['malay']
        n_tamil = d_eth['sl_tamil'] + d_eth['ind_tamil']
        n_buddhist = d_rel['buddhist']

        return {
            'muslim': n_muslim,
            'tamil': n_tamil,
            'buddhist': n_buddhist,
            'sinhalese': n_sinhala,
        }

    def get_label_from_color_value(color_value):
        if color_value == 'sinhalese':
            return 'Sinhalese (Non-Buddhist)'
        return color_value.title()

    def get_color_from_color_value(color_value):
        color = LKCensusEthnicityData.get_color_from_color_value(color_value)
        if color:
            return color
        return LKCensusReligionData.get_color_from_color_value(color_value)

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, 'Flag Cartogram'),
        lk_census_ethnicity_data.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        [
            FlagDorlingView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                SimpleLabel(lk_geodata.get_id_to_name).get_label,
                lk_geodata.get_population,
                get_id_to_flag_data,
            ),
            LegendView(
                'Ethnicity & Religion',
                ['muslim', 'tamil', 'buddhist', 'sinhalese'],
                get_color_from_color_value,
                get_label_from_color_value,
            )
        ],
        (800, 900, 10),
        15,
    ).save('/tmp/infographics.example6.svg')
