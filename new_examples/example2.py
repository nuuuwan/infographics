from infographics.core import ColorPaletteVaryHue, Infographic
from infographics.data_view import LKMap
from infographics.view import PolygonView
from new_examples.examples import example_svg_file_name


def main():
    infographic = Infographic(
        title='Population & Population Density',
        subtitle='Provinces of Sri Lanka',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKMap(
                region_id='LK',
                subregion_type='district',
                legend_title='Population Density',
                get_color_value=None,
                color_palette=ColorPaletteVaryHue(),
                get_label=None,
                get_label_value=None,
                class_view=PolygonView,
            )
        ]
    )
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
