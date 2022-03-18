from infographics.core import Infographic
from infographics.data_view import LKCensusMap
from infographics.view import FlagDorlingView


def sub(region_id, subregion_type):

    svg_file_name = '/tmp/infographics.example6' + \
        f'-{region_id}-{subregion_type}.svg'

    Infographic(
        title=f'{region_id}',
        subtitle=f'Flag Cartogram by {subregion_type.title()}',
        footer_text='visualization by @nuuuwan',
        child_list=[
            LKCensusMap(
                region_id=region_id,
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
        ['EC-01', 'pd'],
        ['EC-02', 'pd'],
        ['EC-14', 'pd'],
        ['EC-16', 'pd'],
    ]:
        sub(region_id, subregion_type)


if __name__ == '__main__':
    main()
