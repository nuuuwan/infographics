
from infographics.adaptors import ColorBase, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKCensusData, LKGeoData, gig_utils
from infographics.view import DorlingView, LegendView

if __name__ == '__main__':
    region_id = 'LK'
    subregion_type = 'dsd'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_data = LKCensusData(
        'cooking_fuel_of_household',
    )

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_census_data.get_most_common,
        lk_census_data.get_color_from_color_value,
    )

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, lk_census_data.table_name),
        lk_census_data.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[
            DorlingView(
                lk_geodata.keys(),
                lk_geodata.get_norm_multipolygon,
                color_base.get_color,
                SimpleLabel(lk_geodata.get_name).get_label,
                lk_census_data.get_total_population,
            ),
            LegendView(
                'Most Common',
                color_base.unique_color_values,
                lk_census_data.get_color_from_color_value,
                lk_census_data.get_label_from_color_value,
            )
        ]
    ).save('/tmp/infographics.example7.svg')
