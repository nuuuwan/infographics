from elections_lk.presidential.presidential import get_election_data_index

from infographics.examples import example3, example4, example5
from infographics.Infographic import Infographic
from infographics.LKDorlingCartogram import LKDorlingCartogram

year = example3.year
region_id = example3.region_id
pd_to_result = get_election_data_index(year)


true_map = example3.true_map
true_map.set_position(
    left_bottom=(0.025, 0.1),
    width_height=(0.2, 0.8),
)

dorling = example4.dorling
dorling.set_position(
    left_bottom=(0.275, 0.1),
    width_height=(0.2, 0.8),
)

true_map_prog = example5.true_map_prog
true_map_prog.set_position(
    left_bottom=(0.525, 0.1),
    width_height=(0.2, 0.8),
)

dorling_prog = LKDorlingCartogram(
    region_id=region_id,
    sub_region_type='pd',
    figure_text='d) Dorling Cartogram with Progressive Coloring',
    func_get_color_value=example5._func_get_color_value,
    func_value_to_color=example5._func_value_to_color,
    func_format_color_value=example5._func_format_color_value,
    func_render_label=example5._func_render_label,
    func_get_area_value=example4._func_get_area_value,
    func_format_area_value=example4._func_format_area_value,
    left_bottom=(0.775, 0.1),
    width_height=(0.2, 0.8),
)

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
            true_map,
            dorling,
            true_map_prog,
            dorling_prog,
        ],
    ).save('/tmp/infographics.example6.%s.%d.png' % (region_id, year))
