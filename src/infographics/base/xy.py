"""
Various xy rexed utils.

point hierarchy
0 - coordinates (x or y, x or y)
1 - point
2 - polygon (point_list)
3 - multipolygon (point_list_list)
"""
from utils import ds


def get_bounds(polygon):
    min_x, min_y = 180, 180
    max_x, max_y = -180, -180
    for x, y in polygon:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return ((min_x, min_y), (max_x, max_y))


def get_midxy(multipolygon):
    polygon = ds.flatten(multipolygon)
    ((min_x, min_y), (max_x, max_y)) = get_bounds(polygon)
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2
    return (mid_x, mid_y)


def get_spans(multipolygon):
    polygon = ds.flatten(multipolygon)
    ((min_x, min_y), (max_x, max_y)) = get_bounds(polygon)
    return (max_x - min_x), (max_y - min_y)


def shapely_multipolygon_to_polygon_list(multipolygon):
    return list(multipolygon)


def shapely_polygon_to_point_list(polygon):
    return list(polygon.exterior.coords)


def shapely_point_to_xy(point):
    return (point[1], point[0])


def norm_multi2polygon(
    multi2polygon,
    map_r=0.8,
    size=(
        1600,
        900)):
    polygon = ds.flatten(ds.flatten(multi2polygon))
    ((min_x, min_y), (max_x, max_y)) = get_bounds(polygon)
    x_span = max_x - min_x
    y_span = max_y - min_y

    r = x_span / y_span * (size[0] / size[1])
    padding_x = 0
    padding_y = 0
    if r > 1:
        padding_x = (1 - (1 / r)) / 2
    else:
        padding_y = (1 - r) / 2

    def t(xy):
        x, y = xy
        qy = (x - min_x) / x_span
        qx = (y - min_y) / y_span

        rx = padding_x + qx * (1 - padding_x * 2)
        ry = padding_y + qy * (1 - padding_y * 2)

        px = (rx * 2 - 1) * map_r
        py = (ry * 2 - 1) * map_r
        return (px, py)

    return list(map(
        lambda multipolygon: list(map(
            lambda polygon: list(map(
                t,
                polygon,
            )), multipolygon
        )),
        multi2polygon,
    ))