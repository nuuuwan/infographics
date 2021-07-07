"""Example."""
import os
import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling
from cartogram import _utils


def _plot_single_party(
    year,
    selected_party_id,
    region_id,
):
    pd_to_result = _utils.get_election_data_index(year)

    def _func_get_color(row):
        result = pd_to_result[row.id]
        for_party = _utils.get_party_result(result, selected_party_id)
        p_votes = for_party['votes'] / result['summary']['valid']
        return _utils.party_to_rgba_color(
            selected_party_id,
            p_votes,
            p_to_a=lambda a: a,
        )

    def _func_get_radius_value(row):
        result = pd_to_result[row.id]
        for_party = _utils.get_party_result(result, selected_party_id)
        return for_party['votes']

    def _func_render_label(ax, x, y, span_y, row):
        result = pd_to_result[row.id]
        party_info = _utils.get_party_result(result, selected_party_id)
        party_p = party_info['votes'] / result['summary']['valid']

        r2 = span_y / 80
        ax.text(
            x,
            y + 3 * r2,
            party_info['party_id'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=10,
        )
        ax.text(
            x,
            y + r2 * 0.5,
            '{:.0%}'.format(party_p),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=15,
        )
        ax.text(
            x,
            y - r2,
            row['name'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=5,
        )
        ax.text(
            x,
            y - 3 * r2,
            '{:,}'.format(party_info['votes']),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=10,
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
        f'{year} Sri Lankan Presidential Election'
        + f'- {selected_party_id}',
    )

    labels_and_colors = []
    for p_votes in [0.8, 0.5, 0.2]:
        labels_and_colors.append((
            '{selected_party_id} {p_votes:.0%}'.format(
                selected_party_id=selected_party_id,
                p_votes=p_votes,
            ),
            _utils.party_to_rgba_color(
                selected_party_id,
                p_votes,
                p_to_a=lambda a: a,
            ),
        ))
    _utils.draw_color_legend(plt, labels_and_colors)

    image_file = '/tmp/cartogram.presidential' \
        + f'.{year}.{selected_party_id}.png'
    plt.savefig(image_file)
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_single_party(2019, 'NDF', 'LK')
