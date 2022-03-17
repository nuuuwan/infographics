from infographics.core import Infographic
from infographics.data_view import LKCensusMap
from infographics.view import FlagDorlingView


def sub(region_id, subregion_type):

    svg_file_name = '/tmp/infographics.example6' + \
        f'-{region_id}-{subregion_type}.svg'

    Infographic(
        title='SL Population',
        subtitle=f'Flag Cartogram by {subregion_type.title()}',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKCensusMap(
                region_id='LK',
                subregion_type=subregion_type,
                legend_title='',
                table_id='ethnicity_religion',
                field='all',
                color_palette=None,
                class_view=FlagDorlingView,
            )]).save(svg_file_name)


def main():
    for region_id, subregion_type in [
        ['LK', 'country'],
        ['LK', 'province'],
        ['LK', 'district'],
        ['LK', 'pd'],
        ['LK-11', 'pd'],
        ['LK-12', 'pd'],
        ['LK-62', 'pd'],
        ['LK-52', 'pd'],
    ]:
        sub(region_id, subregion_type)


if __name__ == '__main__':
    main()
