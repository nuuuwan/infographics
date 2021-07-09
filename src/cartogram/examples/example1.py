"""Example."""
import os

import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling


def _plot_population(region_id, sub_region_type):
    def _func_get_color(row):
        return 'gray'

    def _func_get_radius_value(row):
        return row['population']

    def _func_render_label(ax, x, y, span_y, row):
        r2 = span_y / 80
        ax.text(
            x,
            y + r2,
            row['name'],
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=15,
        )
        ax.text(
            x,
            y - r2,
            '{:.,}'.format(row.population),
            verticalalignment='center',
            horizontalalignment='center',
            fontsize=5,
        )

    gpd_df = geodata.get_region_geodata(region_id, sub_region_type)

    dorling.plot(
        gpd_df,
        func_get_radius_value=_func_get_radius_value,
        func_get_color=_func_get_color,
        func_render_label=_func_render_label,
    )
    plt.suptitle('Data Source: statistics.gov.lk/', fontsize=8)
    plt.title('Population in Sri Lanka')

    image_file = '/tmp/cartogram.example1.png'
    plt.savefig(image_file)
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_population('LK', 'province')
