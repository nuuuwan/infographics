from elections_lk import party_color, presidential

from infographics.examples import example3, example4
from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = example3.year
region_id = example3.region_id
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


true_map_prog = LKMap(
    region_id=region_id,
    sub_region_type='pd',
    figure_text='b) True Area Map with Progressive Coloring',
    func_get_color_value=_func_get_color_value,
    func_value_to_color=_func_value_to_color,
    func_format_color_value=_func_format_color_value,
    func_render_label=_func_render_label,
    left_bottom=(0.55, 0.1),
    width_height=(0.4, 0.8),
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
            example4.true_map,
            true_map_prog,
        ],
    ).save('/tmp/infographics.example5.%s.%d.png' % (region_id, year))
