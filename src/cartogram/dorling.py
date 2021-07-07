"""Implements dorling."""
import math
import matplotlib.pyplot as plt


def _compress(points):
    dt = 0.0015
    n_points = len(points)

    n_epochs = 1000
    for _ in range(0, n_epochs):
        no_moves = True
        for i_a in range(0, n_points):
            x_a, y_a, r_a = \
                points[i_a]['x'], points[i_a]['y'], points[i_a]['r']

            sx, sy = 0, 0
            for i_b in range(0, n_points):
                if i_a == i_b:
                    continue

                x_b, y_b, r_b = \
                    points[i_b]['x'], points[i_b]['y'], points[i_b]['r']
                dx, dy = x_b - x_a, y_b - y_a
                d2 = dx ** 2 + dy ** 2
                d = math.sqrt(d2)
                if d > r_a + r_b:
                    continue

                f_b_a = -r_b ** 2 / d2
                s = dt * f_b_a
                theta = math.atan2(dy, dx)
                sx += s * math.cos(theta)
                sy += s * math.sin(theta)

            points[i_a]['x'] += sx
            points[i_a]['y'] += sy
            no_moves = False
        if no_moves:
            break
    return points


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
    func_render_legend=_default_func_render_legend,
    anchor_radius=0.02,
    anchor_radius_value=100_000,
    color_background=(0.8, 0.8, 0.8, 0.1),
    color_border=(0.8, 0.8, 0.8, 0.2),
):
    """Plot Dorling Cartogram."""
    max_radius_value = 0
    (minx, miny, maxx, maxy) = (180, 180, -180, -180)
    min_squre_span = None
    for _, row in gpd_df.iterrows():
        radius_value = func_get_radius_value(row)
        max_radius_value = max(
            max_radius_value,
            radius_value,
        )

        (minx1, miny1, maxx1, maxy1) = row.geometry.bounds
        minx = min(minx, minx1)
        miny = min(miny, miny1)
        maxx = max(maxx, maxx1)
        maxy = max(maxy, maxy1)

    points = []
    for i_row, row in gpd_df.iterrows():
        radius_value = func_get_radius_value(row)
        r = anchor_radius * \
            math.sqrt(radius_value / anchor_radius_value)
        points.append({
            'x': row.geometry.centroid.x,
            'y': row.geometry.centroid.y,
            'r': r,
            'row': row,
        })


    points = _compress(points)

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
        func_render_label(ax, x, y, span_y, row)

    x = maxx - (maxx - minx) * 0.1
    y = maxy - (maxy - miny) * 0.025

    for p in [1, 0.5, 0.25]:
        r = anchor_radius * math.sqrt(p)
        y -= r
        ax.add_patch(plt.Circle(
            (x, y),
            r,
            color='black',
            fill=False,
            linewidth=1,
        ))
        ax.text(
            x + anchor_radius * 2, y,
            '{:,}'.format((int)(p * anchor_radius_value)),
            verticalalignment='center',
        )
        y -= r
    y -= r
    func_render_legend(ax, x, y, span_y, anchor_radius)

    fig.set_size_inches(16, 9)
    plt.axis('off')
    return plt
