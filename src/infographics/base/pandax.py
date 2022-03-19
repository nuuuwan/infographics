from shapely.geometry import MultiPolygon, Polygon

from infographics.base import xy, shapely


def df_to_geodata_index(df):
    geodata_index = {}
    for row in df.itertuples():
        d = dict(row._asdict())

        shape = d['geometry']
        if isinstance(shape, MultiPolygon):
            polygon_list = shapely.shapely_multipolygon_to_polygon_list(shape)
        elif isinstance(shape, Polygon):
            polygon_list = [shape]
        else:
            polygon_list = []

        point_list_list = list(map(
            shapely.shapely_polygon_to_point_list,
            polygon_list,
        ))

        multipolygon = list(map(
            lambda point_list: list(map(
                shapely.shapely_point_to_xy,
                point_list,
            )),
            point_list_list,
        ))

        del d['geometry']
        geodata_index[d['id']] = d | {
            'multipolygon': multipolygon,
        }

    geodata_index = dict(sorted(
        geodata_index.items(),
        key=lambda item: item[0],
    ))
    return geodata_index
