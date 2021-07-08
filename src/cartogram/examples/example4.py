"""Example."""
import os

import matplotlib.pyplot as plt
from elections_lk import presidential
from geo import geodata

from cartogram import _utils, dorling


def _plot_vote_diff(
    year1,
    year1_party_id,
    year2,
    year2_party_id,
    region_id,
    p_max,
):
    pd_to_result1 = presidential.get_election_data_index(year1)
    pd_to_result2 = presidential.get_election_data_index(year2)

    def _func_get_color(row):
        result1 = pd_to_result1[row.id]
        party_year1 = presidential.get_party_result(
            result1,
            year1_party_id,
        )
        result2 = pd_to_result2[row.id]
        party_year2 = presidential.get_party_result(
            result2,
            year2_party_id,
        )

        p1 = party_year1['votes'] / result1['summary']['valid']
        p2 = party_year2['votes'] / result2['summary']['valid']

        p_diff = p1 - p2
        a = min(1, abs(p_diff) / p_max)
        color = (1, 0, 0, a) if (p_diff < 0) else (0, 0, 1, a)
        return color

    def _func_get_radius_value(row):
        result1 = pd_to_result1[row.id]
        party_year1 = presidential.get_party_result(
            result1,
            year1_party_id,
        )
        result2 = pd_to_result2[row.id]
        party_year2 = presidential.get_party_result(
            result2,
            year2_party_id,
        )

        p1 = party_year1['votes'] / result1['summary']['valid']
        p2 = party_year2['votes'] / result2['summary']['valid']

        return abs(p1 - p2) * result2['summary']['valid']

    def _func_render_label(ax, x, y, span_y, row):
        result1 = pd_to_result1[row.id]
        party_year1 = presidential.get_party_result(
            result1,
            year1_party_id,
        )
        result2 = pd_to_result2[row.id]
        party_year2 = presidential.get_party_result(
            result2,
            year2_party_id,
        )

        p1 = party_year1['votes'] / result1['summary']['valid']
        p2 = party_year2['votes'] / result2['summary']['valid']

        d_n = (p2 - p1) * result2['summary']['valid']

        r2 = span_y / 35
        ax.text(
            x,
            y + r2,
            '{:+.1%}'.format(p2 - p1),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=10,
        )
        ax.text(
            x,
            y,
            row['name'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=5,
        )
        ax.text(
            x,
            y - r2,
            '{:+,.0f}'.format(d_n),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=7.5,
        )

    gpd_df = geodata.get_region_geodata(region_id, 'pd')
    dorling.plot(
        gpd_df,
        func_get_radius_value=_func_get_radius_value,
        func_get_color=_func_get_color,
        func_render_label=_func_render_label,
    )

    labels_and_colors = []
    for i in range(0, 5):
        p_diff = (2 - i) * (p_max / 2)
        if p_diff == 0:
            continue

        a = min(1, abs(p_diff) / p_max)
        color = (1, 0, 0, a) if (p_diff < 0) else (0, 0, 1, a)

        labels_and_colors.append(
            (
                '{p_diff:+.0%}'.format(
                    p_diff=p_diff,
                ),
                color,
            )
        )
    _utils.draw_color_legend(plt, labels_and_colors)

    plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
    plt.title(
        'Sri Lankan Presidential Election - '
        + f'{year1_party_id} in {year1} vs {year2_party_id} in {year2}'
    )
    image_file = (
        '/tmp/cartogram.presidential.'
        + f'{year1}.{year1_party_id}.vs.{year2}.{year2_party_id}.png'
    )
    plt.savefig(image_file)
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_vote_diff(
        1999,
        'UNP',
        2019,
        'NDF',
        'EC-02',
        p_max=0.6,
    )
