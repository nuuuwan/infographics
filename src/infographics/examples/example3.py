from elections_lk import party_color, presidential

from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = 2019
region_id = 'LK'
pd_to_result = presidential.get_election_data_index(year)


def _func_get_color_value(row):
    result = pd_to_result[row.id]
    return presidential.get_winning_party_info(result)['party_id']


def _func_value_to_color(party_id):
    return party_color.get_rgb_color(party_id)


def _func_format_color_value(party_id):
    return party_id


def _func_render_label(row, x, y, spany):
    pass


true_map = LKMap(
    region_id=region_id,
    sub_region_type='pd',
    figure_text='a) True-Area Map',
    func_get_color_value=_func_get_color_value,
    func_value_to_color=_func_value_to_color,
    func_format_color_value=_func_format_color_value,
    func_render_label=_func_render_label,
    left_bottom=(0.1, 0.1),
    width_height=(0.8, 0.8),
)


if __name__ == '__main__':
    Infographic(
        title='%d Sri Lankan Presidential Election' % year,
        subtitle='By Winning Party',
        footer_text='\n'.join(
            [
                'data from https://elections.gov.lk',
                'visualization by @nuuuwan',
            ]
        ),
        children=[
            true_map,
        ],
    ).save('/tmp/infographics.example3.%s.%d.png' % (region_id, year))
