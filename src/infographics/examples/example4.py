from elections_lk import party_color, presidential

from infographics.DorlingCartogram import DorlingCartogram
from infographics.Infographic import Infographic

year = 2015
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
        DorlingCartogram(
            region_id='LK',
            sub_region_type='pd',
            func_get_color_value=_func_get_color_value,
            func_value_to_color=_func_value_to_color,
            func_format_color_value=_func_format_color_value,
            func_render_label=_func_render_label,
        ),
    ],
).save('/tmp/infographics.example4.%d.png' % year)
