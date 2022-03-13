from functools import cached_property

from infographics.base import xy


class GeoMap:
    def __init__(
        self,
        # geodata
        region_id,
        subregion_type,

        # view
        get_color_value,
        legend_title,
        color_palette,
        get_label,
        get_label_value,

        # classes
        class_geodata,
        class_view,
    ):
        self.geodata = class_geodata(
            region_id,
            subregion_type,
        )

        self.view = class_view(
            self.keys,
            get_color_value,
            legend_title,
            color_palette,

            get_label,
            get_label_value,

            self.id_to_multipolygon,
        )

    def __xml__(self):
        return self.view.__xml__()

    # For View

    @cached_property
    def id_to_multipolygon(self):
        multi2polygon = xy.norm_multi2polygon(
            list(map(
                lambda geodata: geodata['multipolygon'],
                self.values(),
            )),
        )
        id_to_multipolygon = {}
        for i, id in enumerate(self.keys()):
            id_to_multipolygon[id] = multi2polygon[i]
        return id_to_multipolygon

    def keys(self):
        return self.geodata.data.keys()

    def values(self):
        return self.geodata.data.values()

    def __getitem__(self, id):
        return self.geodata.data[id]
