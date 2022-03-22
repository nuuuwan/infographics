"""Implements dorling."""

from infographics._utils import log

R_PADDING = 0.01
D_T = 0.01
MAX_EPOCHS = 1000


def move_into_bounds(points, i_a, bounds):
    [cx_a, cy_a], [rx_a, ry_a] = points[i_a]
    (minx, miny, maxx, maxy) = bounds

    d_minx = (cx_a - rx_a) - minx
    d_miny = (cy_a - ry_a) - miny
    d_maxx = maxx - (cx_a + rx_a)
    d_maxy = maxy - (cy_a + ry_a)

    if any([d_minx < 0, d_miny < 0, d_maxx < 0, d_maxy < 0]):
        if d_minx < 0:
            cx_a = minx + rx_a
        if d_miny < 0:
            cy_a = miny + ry_a

        if d_maxx < 0:
            cx_a = maxx - rx_a
        if d_maxy < 0:
            cy_a = maxy - ry_a

        points[i_a][0] = [cx_a, cy_a]
        return points, True
    return points, False


def get_move_delta(points, i_a, i_b):
    if i_a == i_b:
        return 0, 0

    [cx_a, cy_a], [rx_a, ry_a] = points[i_a]
    [cx_b, cy_b], [rx_b, ry_b] = points[i_b]

    dx, dy = cx_b - cx_a, cy_b - cy_a
    if (abs(dx) > (rx_a + rx_b) * (1 + R_PADDING)) \
            or (abs(dy) > (ry_a + ry_b) * (1 + R_PADDING)):
        return 0, 0

    rb2 = ry_a ** 2 + ry_b ** 2
    d2 = dx ** 2 + dy ** 2
    f_b_a = -D_T * (rb2) / d2

    return dx * f_b_a, dy * f_b_a


def _compress(points, bounds):
    n_points = len(points)
    for i_epochs in range(0, MAX_EPOCHS):
        if i_epochs % (MAX_EPOCHS / 10) == 0:
            log.debug('i_epochs = {:,}'.format(i_epochs))

        no_moves = True
        for i_a in range(0, n_points):
            points, did_move = move_into_bounds(points, i_a, bounds)
            if did_move:
                no_moves = False
                continue

            sx, sy = 0, 0
            for i_b in range(0, n_points):
                dsx, dsy = get_move_delta(points, i_a, i_b)
                sx += dsx
                sy += dsy

            if sx or sy:
                points[i_a][0][0] += sx
                points[i_a][0][1] += sy
                no_moves = False

        if no_moves:
            break
    return points
