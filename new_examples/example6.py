from infographics.core import Infographic
from infographics.data_view import LKCensusMap
from infographics.view import FlagDorlingView


def main():
    Infographic(
        title='SL Population',
        subtitle='"Flags"',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKCensusMap(
                region_id='LK',
                subregion_type='ed',
                legend_title='',
                table_id='ethnicity_religion',
                field='all',
                color_palette=None,
                class_view=FlagDorlingView,
            )]).save('/tmp/infographics.example6.svg')


if __name__ == '__main__':
    main()
