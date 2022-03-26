
from infographics.adaptors import (ColorBase, ColorPercentVaryLightness,
                                   SimpleLabel)
from infographics.core import Infographic
from infographics.data import LKElectionsData, LKGeoData, gig_utils
from infographics.view import DorlingView, LegendView

if __name__ == '__main__':

    region_id = 'LK'
    subregion_type = 'pd'
    field_list = ['JJB']

    lk_geodata = LKGeoData(region_id, subregion_type)
    lk_election_data = LKElectionsData(
        'parliamentary_election_2020',
    )

    color_base = ColorBase(
        lk_geodata.keys(),
        lk_election_data.get_get_p_population(field_list),
        ColorPercentVaryLightness(hue=0).get_color_from_color_value,
    )

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, '/'.join(field_list) + ' Votes'),
        lk_election_data.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[
            DorlingView(
                lk_geodata.keys(),
                lk_geodata.get_norm_multipolygon,
                color_base.get_color,
                SimpleLabel(lk_geodata.get_name).get_label,
                lk_election_data.get_get_population(field_list),
                DorlingView.render_ellipse_object,
            ),
            LegendView(
                '% of Population',
                color_base.get_color_values(),
                color_base.get_color_from_color_value,
                color_base.get_percent_label_from_color_value,
            )
        ]
    ).save('/tmp/infographics.example10.svg')
