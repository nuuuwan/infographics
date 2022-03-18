from infographics.core import ColorPaletteVaryLightness, Infographic
from infographics.data_view import LKCensusMap
from infographics.view import DorlingView
from new_examples.examples import example_svg_file_name


def main():
    infographic = Infographic(
        title='SL Moor Population',
        subtitle='Colombo Electoral District - Polling Divisions',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKCensusMap(
                region_id='EC-01',
                subregion_type='pd',
                legend_title='% of Population',
                table_id='ethnicity_of_population',
                field='sl_moor',
                color_palette=ColorPaletteVaryLightness(
                    hue=140,
                    min_lightness=1,
                    max_lightness=0.4,
                ),
                class_view=DorlingView,
            )])
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
