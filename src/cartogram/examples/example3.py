"""Example."""
import os
import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling
from cartogram import _utils


def _plot_rejected_votes(year, region_id):
    pd_to_result = _utils.get_election_data_index(year)

    def _func_get_color(row):
        summary = pd_to_result[row.id]['summary']
        p_reject = summary['rejected'] / summary['polled']
        return (1, 1 - p_reject / 0.05, 1 - p_reject / 0.05, 0.8)

    def _func_get_radius_value(row):
        return pd_to_result[row.id]['summary']['rejected']

    def _func_render_label(ax, x, y, span_y, row):
        summary = pd_to_result[row.id]['summary']
        p_reject = summary['rejected'] / summary['polled']

        r2 = span_y / 50
        ax.text(
            x,
            y + r2,
            '{:.1%}'.format(p_reject),
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

    gpd_df = geodata.get_region_geodata(region_id, 'pd')
    dorling.plot(
        gpd_df,
        func_get_radius_value=_func_get_radius_value,
        func_get_color=_func_get_color,
        func_render_label=_func_render_label,
    )

    labels_and_colors = []
    for i in range(0, 6):
        p_reject = i * 0.01
        labels_and_colors.append((
            '{p_reject:.0%}'.format(
                p_reject=p_reject,
            ),
            (1, 1 - p_reject / 0.05, 1 - p_reject / 0.05, 0.8),
        ))
    _utils.draw_color_legend(plt, labels_and_colors)

    plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
    plt.title(
        f'{year} Sri Lankan Presidential Election'
        + ' - Rejected Votes',
    )

    image_file = f'/tmp/cartogram.presidential.{year}.rejected.png'
    plt.savefig(image_file)
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_rejected_votes(2015, 'EC-01')
