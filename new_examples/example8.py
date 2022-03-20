
from infographics.adaptors import (ColorBase, ColorPercentVaryLightness,
                                   SimpleLabel)
from infographics.core import Infographic
from infographics.data import LKCensusData, LKGeoData, gig_utils
from infographics.view import DorlingView, LegendView

if __name__ == '__main__':
    region_id = 'LK'
    subregion_type = 'district'
    field = 'bowser'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_data = LKCensusData(
        'source_of_drinking_water_of_household',
    )

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_census_data.get_get_id_to_p_population([field]),
        ColorPercentVaryLightness(hue=0).get_color_value_to_color,
    )

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(
            subregion_type,
            lk_census_data.get_field_name(
                [field])),
        lk_census_data.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[
            DorlingView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                color_base.get_id_to_color,
                SimpleLabel(
                    lk_geodata.get_id_to_name).get_id_to_label,
                lk_census_data.get_get_id_to_population(
                    [field]),
            ),
            LegendView(
                'Most Common',
                color_base.get_color_values(),
                color_base.get_color_value_to_color,
                color_base.get_color_value_to_percent_label,
            )]).save('/tmp/infographics.example8.svg')
