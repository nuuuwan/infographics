"""Implements dorling."""
import math
import matplotlib.pyplot as plt


def _destructure_point(point):
    return (point['x'], point['y'], point['r'], point['color'])


def _compress(points):
    dt = 0.1
    n_points = len(points)

    n_epochs = 100
    for _ in range(0, n_epochs):
        no_moves = True
        for i_a in range(0, n_points):
            (x_a, y_a, r_a, color_a) = _destructure_point(points[i_a])

            sx, sy = 0, 0
            for i_b in range(0, n_points):
                if i_a == i_b:
                    continue

                (x_b, y_b, r_b, color_b) = _destructure_point(points[i_b])
                dx, dy = x_b - x_a, y_b - y_a
                d2 = dx ** 2 + dy ** 2
                d = math.sqrt(d2)
                if d > r_a + r_b:
                    continue

                f_b_a = -r_b ** 3 / d2
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


def plot(
    gpd_df,
    ax=None,
    fig=None,
    func_get_radius_value=_default_func_get_radius_value,
    func_get_color=_default_func_get_color,
    max_radius=0.05,
    color_background=(0, 0, 0, 0.05)
):
    """Plot Dorling Cartogram."""
    points = []
    max_radius_value = None
    for i_row, row in gpd_df.iterrows():
        radius_value = func_get_radius_value(row)
        if max_radius_value is None or max_radius_value < radius_value:
            max_radius_value = radius_value

    r_max_radius_value = 0.08
    for i_row, row in gpd_df.iterrows():
        radius_value = func_get_radius_value(row)
        color = func_get_color(row)

        r = r_max_radius_value * math.sqrt(radius_value / max_radius_value)
        points.append({
            'x': row.geometry.centroid.x,
            'y': row.geometry.centroid.y,
            'r': r,
            'color': color,
        })
    points = _compress(points)

    if ax is None or fig is None:
        fig, ax = plt.subplots()

    gpd_df.plot(ax=ax, color=color_background)
    for point in points:
        (x, y, r, color) = _destructure_point(point)
        circle = plt.Circle((x, y), r, color=color, linewidth=1)
        ax.add_patch(circle)

    plt.axis('off')
    return plt
