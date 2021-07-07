"""Implements dorling."""
import math
import matplotlib.pyplot as plt

from cartogram.dorling_compress import _compress


def _default_func_get_radius_value(row):
    return row.population


def _default_func_get_color(row):
    return (0, 0.5, 0, 0.5)


def _default_func_render_label(ax, x, y, r, row):
    ax.text(
        x,
        y + r/3,
        row.id,
        verticalalignment='center',
        horizontalalignment='center',
        fontsize=6,
    )
    ax.text(
        x,
        y - r/3,
        '{:,}'.format(_default_func_get_radius_value(row)),
        verticalalignment='center',
        horizontalalignment='center',
        fontsize=8,
    )


def _default_func_render_legend(ax, x, y, span_y, anchor_radius):
    pass


def plot(
    gpd_df,
    ax=None,
    fig=None,
    func_get_radius_value=_default_func_get_radius_value,
    func_get_color=_default_func_get_color,
    func_render_label=_default_func_render_label,
    color_background=(0.8, 0.8, 0.8, 0.25),
    color_border=(0.8, 0.8, 0.8, 0.5),
    compactness=0.333,
):
    """Plot Dorling Cartogram."""
    max_radius_value = 0
    (minx, miny, maxx, maxy) = (180, 180, -180, -180)
    sum_radius_value = 0
    n_regions = 0
    for _, row in gpd_df.iterrows():
        radius_value = func_get_radius_value(row)
        max_radius_value = max(
            max_radius_value,
            radius_value,
        )
        sum_radius_value += radius_value

        (minx1, miny1, maxx1, maxy1) = row.geometry.bounds
        minx = min(minx, minx1)
        miny = min(miny, miny1)
        maxx = max(maxx, maxx1)
        maxy = max(maxy, maxy1)

        n_regions += 1
    area = (maxx - minx) * (maxy - miny)

    alpha = compactness * math.pi / 4
    beta = alpha * area / math.pi / sum_radius_value

    points = []
    for i_row, row in gpd_df.iterrows():
        radius_value = func_get_radius_value(row)
        r = math.sqrt(radius_value * beta)
        points.append({
            'x': row.geometry.centroid.x,
            'y': row.geometry.centroid.y,
            'r': r,
            'row': row,
        })

    points = _compress(
        points,
        (minx, miny, maxx, maxy),
    )

    if ax is None or fig is None:
        fig, ax = plt.subplots()

    gpd_df.plot(
        ax=ax,
        color=color_background,
        edgecolor=color_border,
    )
    span_y = (maxy - miny)
    for point in points:
        x, y, r, row = point['x'], point['y'], point['r'], point['row']
        color = func_get_color(row)
        ax.add_patch(plt.Circle(
            (x, y),
            r,
            facecolor=color,
            edgecolor='gray',
            linewidth=0.3,
        ))
        if n_regions < 20:
            func_render_label(ax, x, y, span_y, row)

    x = maxx - (maxx - minx) * 0.1
    y = maxy - (maxy - miny) * 0.25
    anchor_radius_value = math.pow(
        10,
        round(math.log10(max_radius_value)),
    )
    anchor_radius = math.sqrt(anchor_radius_value * beta)
    for pr in [1]:
        r = anchor_radius * pr
        ax.text(
            x, y,
            '{:,}'.format((int)(pr ** 2 * anchor_radius_value)),
            verticalalignment='center',
            horizontalalignment='center',
        )
        ax.add_patch(plt.Circle(
            (x, y),
            r,
            color='gray',
            fill=False,
            linewidth=1,
        ))

    y -= r

    fig.set_size_inches(16, 9)
    plt.axis('off')
    return plt
