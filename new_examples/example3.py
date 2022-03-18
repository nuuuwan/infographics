from infographics.core import ColorPaletteVaryLightness, Infographic
from infographics.data_view import LKCensusMap
from infographics.view import PolygonView
from new_examples.examples import example_svg_file_name


def main():
    infographic = Infographic(
        title='Buddhist Population',
        subtitle='Colombo Electoral District - Polling Divisions',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKCensusMap(
                region_id='EC-01',
                subregion_type='pd',
                legend_title='% of Population',
                table_id='religious_affiliation_of_population',
                field='buddhist',
                color_palette=ColorPaletteVaryLightness(
                    hue=60,
                    min_lightness=1,
                    max_lightness=0.4,
                ),
                class_view=PolygonView,
            )])
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
