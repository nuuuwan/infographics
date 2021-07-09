from elections_lk import party_color, presidential

from infographics.DorlingCartogram import DorlingCartogram
from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

year = 2019
pd_to_result = presidential.get_election_data_index(year)


def _func_get_color_value(row):
    result = pd_to_result[row.id]
    return presidential.get_winning_party_info(result)


def _func_value_to_color(party_info):
    return party_color.get_rgb_color(party_info['party_id'])


def _func_format_color_value(party_info):
    return party_info['party_id']


def _func_render_label(row, x, y, spany):
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
                func_get_color_value=_func_get_color_value,
                func_value_to_color=_func_value_to_color,
                func_format_color_value=_func_format_color_value,
                func_render_label=_func_render_label,
                left_bottom=(0.05, 0.1),
                width_height=(0.4, 0.8),
            ),
            DorlingCartogram(
                region_id='LK',
                sub_region_type='pd',
                func_get_color_value=_func_get_color_value,
                func_value_to_color=_func_value_to_color,
                func_format_color_value=_func_format_color_value,
                func_render_label=_func_render_label,
                left_bottom=(0.55, 0.1),
                width_height=(0.4, 0.8),
            ),
        ],
    ).save('/tmp/infographics.example4.%d.png' % year)
