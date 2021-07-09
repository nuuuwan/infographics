from elections_lk import presidential

from infographics.DorlingCartogram import DorlingCartogram
from infographics.examples import example3
from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = example3.year

pd_to_result = presidential.get_election_data_index(year)


def _func_get_radius_value(row):
    result = pd_to_result[row.id]
    return result['summary']['valid']


def _func_format_radius_value(radius_value):
    return '{:,.0f}\nvalid votes'.format(radius_value)


if __name__ == '__main__':
    Infographic(
        title='%d Sri Lankan Presidential Election' % year,
        subtitle='By Winning Party',
        footer_text='\n'.join(
            [
                'data from https://elections.gov.lk',
                'visualizaiton by @nuuuwan',
            ]
        ),
        children=[
            LKMap(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='a) True-Area Map',
                func_get_color_value=example3._func_get_color_value,
                func_value_to_color=example3._func_value_to_color,
                func_format_color_value=example3._func_format_color_value,
                func_render_label=example3._func_render_label,
                left_bottom=(0.05, 0.1),
                width_height=(0.4, 0.8),
            ),
            DorlingCartogram(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='b) Dorling Cartogram',
                func_get_color_value=example3._func_get_color_value,
                func_value_to_color=example3._func_value_to_color,
                func_format_color_value=example3._func_format_color_value,
                func_render_label=example3._func_render_label,
                func_get_radius_value=_func_get_radius_value,
                func_format_radius_value=_func_format_radius_value,
                left_bottom=(0.55, 0.1),
                width_height=(0.4, 0.8),
            ),
        ],
    ).save('/tmp/infographics.example4.%d.png' % year)
