def shapely_multipolygon_to_polygon_list(multipolygon):
    return list(multipolygon)


def shapely_polygon_to_point_list(polygon):
    return list(polygon.exterior.coords)


def shapely_point_to_xy(point):
    return (point[1], point[0])
