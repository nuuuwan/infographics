from elections_lk import presidential

from infographics.DorlingCartogram import DorlingCartogram
from infographics.examples import example3, example4, example5
from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = example3.year
pd_to_result = presidential.get_election_data_index(year)


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
                figure_text='a) True Area Map',
                func_get_color_value=example3._func_get_color_value,
                func_value_to_color=example3._func_value_to_color,
                func_format_color_value=example3._func_format_color_value,
                func_render_label=example3._func_render_label,
                left_bottom=(0.025, 0.1),
                width_height=(0.2, 0.8),
            ),
            DorlingCartogram(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='b) Dorling Cartogram',
                func_get_color_value=example3._func_get_color_value,
                func_value_to_color=example3._func_value_to_color,
                func_format_color_value=example3._func_format_color_value,
                func_render_label=example3._func_render_label,
                func_get_radius_value=example4._func_get_radius_value,
                func_format_radius_value=example4._func_format_radius_value,
                left_bottom=(0.275, 0.1),
                width_height=(0.2, 0.8),
            ),
            LKMap(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='c) True Area Map with Progressive Coloring',
                func_get_color_value=example5._func_get_color_value,
                func_value_to_color=example5._func_value_to_color,
                func_format_color_value=example5._func_format_color_value,
                func_render_label=example5._func_render_label,
                left_bottom=(0.525, 0.1),
                width_height=(0.2, 0.8),
            ),
            DorlingCartogram(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='d) Dorling Cartogram with Progressive Coloring',
                func_get_color_value=example5._func_get_color_value,
                func_value_to_color=example5._func_value_to_color,
                func_format_color_value=example5._func_format_color_value,
                func_render_label=example5._func_render_label,
                func_get_radius_value=example4._func_get_radius_value,
                func_format_radius_value=example4._func_format_radius_value,
                left_bottom=(0.757, 0.1),
                width_height=(0.2, 0.8),
            ),
        ],
    ).save('/tmp/infographics.example6.%d.png' % year)
