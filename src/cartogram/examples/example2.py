"""Example."""
import os

import matplotlib.pyplot as plt
from geo import geodata

from cartogram import _utils, dorling


def _plot_winning_party(year, region_id):
    pd_to_result = _utils.get_election_data_index(year)

    winning_party_set = set()
    for result in pd_to_result.values():
        winning_party = _utils.get_winning_party_info(result)['party_id']
        winning_party_set.add(winning_party)

    def _func_get_color(row):
        result = pd_to_result[row.id]
        win_party = _utils.get_winning_party_info(result)
        p_votes = win_party['votes'] / result['summary']['valid']
        return _utils.party_to_rgba_color(win_party['party_id'], p_votes)

    def _func_get_radius_value(row):
        result = pd_to_result[row.id]
        return result['summary']['valid']

    def _func_render_label(ax, x, y, span_y, row):
        result = pd_to_result[row.id]
        win_party = _utils.get_winning_party_info(result)
        p_votes = win_party['votes'] / result['summary']['valid']

        r2 = span_y / 35
        ax.text(
            x,
            y + r2,
            win_party['party_id'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=10,
        )
        ax.text(
            x,
            y,
            '{:.0%}'.format(p_votes),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=15,
        )
        ax.text(
            x,
            y - r2 * 0.8,
            row['name'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=5,
        )

    gpd_df = geodata.get_region_geodata(region_id, 'pd')
    dorling.plot(
        gpd_df,
        func_get_radius_value=_func_get_radius_value,
        func_get_color=_func_get_color,
        func_render_label=_func_render_label,
    )

    plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
    plt.title(
        f'{year} Sri Lankan Presidential Election ' + '- By Winning Party',
    )
    image_file = f'/tmp/cartogram.presidential.{year}.png'

    labels_and_colors = []
    for winning_party in winning_party_set:
        for p_votes in [0.8, 0.65, 0.5]:
            labels_and_colors.append(
                (
                    '{winning_party} {p_votes:.0%}'.format(
                        winning_party=winning_party,
                        p_votes=p_votes,
                    ),
                    _utils.party_to_rgba_color(winning_party, p_votes),
                )
            )
    _utils.draw_color_legend(plt, labels_and_colors)

    plt.savefig(image_file)
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_winning_party(1999, 'EC-02')
