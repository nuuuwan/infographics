from infographics.data import LKCensusData
from infographics.data_view.LKMap import LKMap


class LKCensusMap:
    def __init__(
        self,
        # LKCensusData
        table_id,

        # LKMap
        region_id,
        subregion_type,
        legend_title,
        color_palette,

        # LKCensusMap
        field,

    ):
        self.data = LKCensusData(table_id)
        self.view = LKMap(
            region_id,
            subregion_type,
            legend_title,
            color_palette,
        )
        self.field = field

    def __xml__(self):
        return self.view.__xml__()

    # Implement AbstractColoredView
    def get_color_value(self, id):
        d = self.data[id]
        return d[self.field] / d[self.total_field]

    # For AbstractLabelledView
    def get_label(self, id):
        return self.view.data[id]['name']

    def get_label_value(self, id):
        return self.get_color_value(id)
