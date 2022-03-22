
from infographics.adaptors import ColorBase, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKElectionsData, LKGeoData, gig_utils
from infographics.view import DorlingView, LegendView

if __name__ == '__main__':
    region_id = 'LK'
    subregion_type = 'pd'

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_election_data = LKElectionsData(
        'presidential_election_2019',
    )

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_election_data.id_to_most_common,
        lk_election_data.get_color_from_color_value,
    )

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, lk_election_data.table_name),
        lk_election_data.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[
            DorlingView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                color_base.get_id_to_color,
                SimpleLabel(lk_geodata.get_id_to_name).get_id_to_label,
                lk_election_data.get_id_to_total_population,
            ),
            LegendView(
                'Most Common',
                color_base.unique_color_values,
                lk_election_data.get_color_from_color_value,
                lk_election_data.get_color_value_to_label,
            )
        ]
    ).save('/tmp/infographics.example9.svg')
