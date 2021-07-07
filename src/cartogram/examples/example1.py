"""Example."""
import os
import matplotlib.pyplot as plt
from geo import geodata

from elections_lk import presidential

from cartogram import dorling
from cartogram import _utils


def _plot(
    year,
    selected_party_id,
    region_id,
):
    election_data = presidential.get_election_data(year)
    pd_to_result = dict(zip(
        list(map(lambda result: result['pd_id'], election_data)),
        election_data,
    ))

    def _func_get_color(row):
        pd_id = row.id
        result = pd_to_result[pd_id]
        for_party = _utils._get_party_result(result, selected_party_id)
        p_votes = for_party['votes'] / result['summary']['valid']
        return _utils._party_to_rgba_color(for_party['party_id'], p_votes)


    def _func_get_radius_value(row):
        pd_id = row.id
        result = pd_to_result[pd_id]
        for_party = _utils._get_party_result(result, selected_party_id)
        return for_party['votes']

    def _func_render_label(ax, x, y, span_y, row):
        pd_id = row.id
        result = pd_to_result[pd_id]
        party_info = _utils._get_party_result(result, selected_party_id)
        party_p = party_info['votes'] / result['summary']['valid']

        r2 = span_y / 40
        ax.text(
            x,
            y + r2,
            party_info['party_id'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=8,
        )
        ax.text(
            x,
            y,
            '{:.0%}'.format(party_p),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=9,
        )
        ax.text(
            x,
            y - r2,
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
        # anchor_radius=0.08,
        # anchor_radius_value=100_000,
        # anchor_radius=0.1,
        # anchor_radius_value=2000,
        anchor_radius=0.04,
        anchor_radius_value=100_000,
    )
    plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
    plt.title(
        f'{year} Sri Lankan Presidential Election'
        + f'- {selected_party_id}',
    )
    image_file = '/tmp/cartogram.presidential' \
        + f'.{year}.{selected_party_id}.png'
    plt.savefig(image_file)
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot(2019, 'NDF', 'EC-03')
