from infographics.adaptors import ColorBase, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKCensusEthnicityData, LKGeoData, gig_utils
from infographics.view import LegendView, PolygonView

if __name__ == '__main__':
    region_id = 'LK'
    subregion_type = 'dsd'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_census_ethnicity_data = LKCensusEthnicityData()

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_census_ethnicity_data.get_most_common_ethnicity,
        LKCensusEthnicityData.get_color_from_color_value,
    )

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, 'Most Common Ethnicity'),
        lk_census_ethnicity_data.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[
            PolygonView(
                lk_geodata.keys(),
                lk_geodata.get_norm_multipolygon,
                color_base.get_color,
                SimpleLabel(lk_geodata.get_name).get_label,
            ),
            LegendView(
                'Most Common Ethnicity',
                color_base.unique_color_values,
                LKCensusEthnicityData.get_color_from_color_value,
                LKCensusEthnicityData.get_label_from_color_value,
            ),
        ],
    ).save('/tmp/infographics.example3.svg')
