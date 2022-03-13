from infographics.core import ColorPaletteVaryLightness, Infographic
from infographics.data_view import LKCensusMap
from infographics.view import DorlingView


def main():
    Infographic(
        title='SL Moor Population',
        subtitle='Colombo Electoral District - Polling Divisions',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKCensusMap(
                region_id='LK',
                subregion_type='dsd',
                legend_title='% of Population',
                table_id='ethnicity_of_population',
                field='sl_moor',
                color_palette=ColorPaletteVaryLightness(
                    hue=140,
                    min_lightness=1,
                    max_lightness=0.4,
                ),
                class_view=DorlingView,
            )]).save('/tmp/infographics.example4.svg')


if __name__ == '__main__':
    main()
