import colorsys
import math

import matplotlib.pyplot as plt
from geo import geodata

from infographics import plotx

N_LEGEND_VALUES = 5


def _default_func_get_color_value(row):
    return row.population / row.area


def _default_func_value_to_color(density):
    log_density = math.log10(density)
    h = (1 - (log_density - 1) / 4) / 3
    (r, g, b) = colorsys.hsv_to_rgb(h, 0.8, 0.8)
    return (r, g, b)


def _default_func_format_color_value(color_value):
    return '{:,.0f} per km²'.format(color_value)


def _default_func_render_label(row, x, y, spany):
    r2 = spany / 40
    plotx.draw_text((x, y + r2), row['name'], fontsize=6)

    color_value = _default_func_get_color_value(row)
    rendered_color_value = _default_func_format_color_value(color_value)
    plotx.draw_text((x, y + r2 * 0.1), rendered_color_value, fontsize=8)


class LKMap:
    def __init__(
        self,
        region_id='LK',
        sub_region_type='province',
        func_get_color_value=_default_func_get_color_value,
        func_value_to_color=_default_func_value_to_color,
        func_format_color_value=_default_func_format_color_value,
        func_render_label=_default_func_render_label,
        func_render_overlay=None,
    ):
        self.region_id = region_id
        self.sub_region_type = sub_region_type

        self.func_get_color_value = func_get_color_value
        self.func_value_to_color = func_value_to_color
        self.func_format_color_value = func_format_color_value
        self.func_render_label = func_render_label

        self.func_render_overlay = func_render_overlay

    def draw(self):
        gpd_df = geodata.get_region_geodata(
            self.region_id,
            self.sub_region_type,
        )

        (
            n_regions,
            minx,
            miny,
            maxx,
            maxy,
            spanx,
            spany,
            area,
        ) = plotx.get_bounds(gpd_df)

        color_values = []
        gpd_df['color'] = gpd_df['id'].astype(object)
        for i_row, row in gpd_df.iterrows():
            color_value = self.func_get_color_value(row)
            color_values.append(color_value)
            color = self.func_value_to_color(color_value)
            gpd_df.at[i_row, 'color'] = color

        ax = plt.axes([0.1, 0.1, 0.8, 0.8])
        gpd_df.plot(
            ax=ax,
            color=gpd_df['color'],
            edgecolor=plotx.DEFAULTS.COLOR_STROKE,
            linewidth=plotx.DEFAULTS.STROKE_WIDTH,
        )

        for i_row, row in gpd_df.iterrows():
            self.func_render_label(
                row,
                row.geometry.centroid.x,
                row.geometry.centroid.y,
                spany,
            )

        # color legend
        labels = []
        handles = []

        n_color_values = len(color_values)
        sorted_color_values = sorted(color_values, reverse=True)
        for i in range(0, N_LEGEND_VALUES):
            i_color_value = (int)(
                i * (n_color_values - 1) / (N_LEGEND_VALUES - 1)
            )
            color_value = sorted_color_values[i_color_value]
            color = _default_func_value_to_color(color_value)
            labels.append(self.func_format_color_value(color_value))
            handles.append(plotx.get_color_patch(color))

        plt.legend(handles=handles, labels=labels)

        if self.func_render_overlay:
            self.func_render_overlay(
                gpd_df,
                n_regions,
                minx,
                miny,
                maxx,
                maxy,
                spanx,
                spany,
                area,
            )

        plt.axis('off')


if __name__ == '__main__':
    from Infographic import Infographic

    Infographic(
        title='Sri Lanka',
        children=[
            LKMap(region_id='LK', sub_region_type='district'),
        ],
    ).save('/tmp/infographics.lkmap.png').close()
