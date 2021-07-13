from elections_lk import party_color, presidential

from infographics.examples import example3, example4
from infographics.Infographic import Infographic
from infographics.LKDorlingCartogram import LKDorlingCartogram

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
            LKDorlingCartogram(
                region_id=example3.region_id,
                sub_region_type='pd',
                figure_text='{:.0%} Compactness'.format(x[1]),
                func_get_color_value=example3._func_get_color_value,
                func_value_to_color=example3._func_value_to_color,
                func_format_color_value=example3._func_format_color_value,
                func_render_label=example3._func_render_label,
                func_get_radius_value=example4._func_get_radius_value,
                func_format_radius_value=example4._func_format_radius_value,
                left_bottom=(0.01 + (0.16 + 0.02) * x[0], 0.1),
                width_height=(0.16, 0.8),
                compactness=x[1],
            )
            for x in enumerate([0.1, 0.2, 0.3, 0.4, 0.5])
        ],
    ).save('/tmp/infographics.example7.%d.png' % year)
