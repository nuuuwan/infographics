from infographics.core import ColorPaletteVaryHue, Infographic
from infographics.data_view import LKMap


def main():
    Infographic(
        title='Population & Population Density',
        subtitle='Provinces of Sri Lanka',
        footer_text='visualization by @nuuuwan',
        child_list=[LKMap(
            region_id='LK',
            subregion_type='district',
            legend_title='Population Density',
            color_palette=ColorPaletteVaryHue(),
        )]
    ).save('/tmp/infographics.example2.svg')


if __name__ == '__main__':
    main()
