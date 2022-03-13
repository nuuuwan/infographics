
from infographics.data import LKGeoData
from infographics.data_view.GeoMap import GeoMap


class LKMap(GeoMap):
    def __init__(
        self,
        region_id,
        subregion_type,
        get_color_value,
        legend_title,
        color_palette,
        get_label,
        get_label_value,
        class_view,
    ):
        class_geodata = LKGeoData

        get_color_value = get_color_value \
            if get_color_value else self.get_color_value
        get_label = get_label \
            if get_label else self.get_label
        get_label_value = get_label_value \
            if get_label_value else self.get_label_value

        GeoMap.__init__(
            self,
            region_id,
            subregion_type,
            get_color_value,
            legend_title,
            color_palette,
            get_label,
            get_label_value,
            class_geodata,
            class_view,
        )

    def get_color_value(self, id):
        return self.geodata.data[id]['population'] / \
            self.geodata.data[id]['area']

    def get_label(self, id):
        return self.geodata.data[id]['name']

    def get_label_value(self, id):
        return self.geodata.data[id]['population']
