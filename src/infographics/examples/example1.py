"""Example."""
import os

from geo import geodata
from utils import plotx

from infographics import dorling


def _plot_population(region_id, sub_region_type):
    gpd_df = geodata.get_region_geodata(region_id, sub_region_type)

    def _func_plot_inner():
        dorling.plot(gpd_df)

    image_file = '/tmp/infographics.example1.%s.%s.png' % (
        region_id,
        sub_region_type,
    )
    plotx.draw_infographic(
        title='Population in %s' % (region_id),
        subtitle='By %s' % sub_region_type.upper(),
        footer_text='Data Source: '
        + 'Department of Census and Statistics, Sri Lanka',
        image_file=image_file,
        func_plot_inner=_func_plot_inner,
    )
    os.system(f'open {image_file}')


if __name__ == '__main__':
    _plot_population('EC-01', 'pd')
