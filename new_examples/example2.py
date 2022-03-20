
from infographics.adaptors import ColorHistogram, SimpleLabel
from infographics.core import Infographic
from infographics.data import LKGeoData, gig_utils
from infographics.view import LegendView, PolygonView

if __name__ == '__main__':
    region_id = 'LK'
    subregion_type = 'dsd'

    lk_geodata = LKGeoData(region_id, subregion_type)
    color_histogram = ColorHistogram(
        lk_geodata.keys(),
        lk_geodata.get_id_to_population_density,
    )

    Infographic(
        gig_utils.get_full_name(region_id),
        gig_utils.get_by_name(subregion_type, 'Population Density'),
        lk_geodata.source_text,
        Infographic.DEFAULT_FOOTER_TEXT,
        [
            PolygonView(
                lk_geodata.keys(),
                lk_geodata.get_id_to_norm_multipolygon,
                color_histogram.get_id_to_color,
                SimpleLabel(lk_geodata.get_id_to_name).get_id_to_label,
            ),
            LegendView(
                'Persons per km²',
                color_histogram.get_color_values(),
                color_histogram.get_color_value_to_color,
                color_histogram.get_color_value_to_int_label,
            )
        ]).save('/tmp/infographics.example2.svg')
