"""Example."""
import os

from geo import geodata

from cartogram import _utils, dorling


def _plot_population(region_id, sub_region_type):
    gpd_df = geodata.get_region_geodata(region_id, sub_region_type)

    def _func_plot_inner(ax):
        dorling.plot(gpd_df, ax)

    image_file = '/tmp/cartogram.example1.%s.%s.png' % (
        region_id,
        sub_region_type,
    )
    _utils.draw_infographic(
        title='Population in %s' % (region_id),
        subtitle='By %s' % sub_region_type.upper(),
        footer_text='Data Source: statistics.gov.lk/',
        image_file=image_file,
        func_plot_inner=_func_plot_inner,
    )
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_population('LK', 'district')
