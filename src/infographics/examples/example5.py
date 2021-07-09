from elections_lk import party_color, presidential

from infographics.DorlingCartogram import DorlingCartogram
from infographics.examples import example4
from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = 2019
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
                region_id='LK',
                sub_region_type='pd',
                func_get_color_value=example4._func_get_color_value,
                func_value_to_color=example4._func_value_to_color,
                func_format_color_value=example4._func_format_color_value,
                func_render_label=example4._func_render_label,
                left_bottom=(0.0167, 0.1),
                width_height=(0.3, 0.8),
            ),
            LKMap(
                region_id='LK',
                sub_region_type='pd',
                func_get_color_value=_func_get_color_value,
                func_value_to_color=_func_value_to_color,
                func_format_color_value=_func_format_color_value,
                func_render_label=_func_render_label,
                left_bottom=(0.35, 0.1),
                width_height=(0.3, 0.8),
            ),
            DorlingCartogram(
                region_id='LK',
                sub_region_type='pd',
                func_get_color_value=_func_get_color_value,
                func_value_to_color=_func_value_to_color,
                func_format_color_value=_func_format_color_value,
                func_render_label=_func_render_label,
                left_bottom=(0.6833, 0.1),
                width_height=(0.3, 0.8),
            ),
        ],
    ).save('/tmp/infographics.example4.%d.png' % year)
