from elections_lk import party_color, presidential

from infographics.examples import example3
from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = example3.year
pd_to_result = presidential.get_election_data_index(year)


def _func_get_color_value(row):
    result = pd_to_result[row.id]
    party_info = presidential.get_winning_party_info(result)
    party_info['p_votes'] = party_info['votes'] / result['summary']['valid']
    return party_info


def _func_value_to_color(party_info):
    return party_color.get_rgba_color(
        party_info['party_id'],
        party_info['p_votes'],
        p_to_a=lambda p: max(p - 0.3, 0) / 0.7,
    )


def _func_format_color_value(party_info):
    return '{party_id} {p_votes:.0%}'.format(
        party_id=party_info['party_id'],
        p_votes=party_info['p_votes'],
    )


def _func_render_label(*_):
    pass


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
                left_bottom=(0.05, 0.1),
                width_height=(0.4, 0.8),
            ),
            LKMap(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='b) True Area Map with Progressive Coloring',
                func_get_color_value=_func_get_color_value,
                func_value_to_color=_func_value_to_color,
                func_format_color_value=_func_format_color_value,
                func_render_label=_func_render_label,
                left_bottom=(0.55, 0.1),
                width_height=(0.4, 0.8),
            ),
        ],
    ).save('/tmp/infographics.example5.%d.png' % year)
