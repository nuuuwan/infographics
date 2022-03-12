from infographics.core import ColorPaletteVaryLightness
from infographics.data import LKCensusData
from infographics.data_view.LKMap import LKMap


class LKCensusMap(LKCensusData, LKMap):
    DEFAULT_FIELD = 'sinhalese'
    DEFAULT_COLOR_PALETTE = ColorPaletteVaryLightness(hue=0)

    def __init__(
        self,
        table_id=LKCensusData.DEFAULT_TABLE_ID,
        field=DEFAULT_FIELD,
        region_id=LKMap.DEFAULT_REGION_ID,
        subregion_type=LKMap.DEFAULT_SUBREGION_TYPE,
        color_palette=DEFAULT_COLOR_PALETTE,
    ):
        LKCensusData.__init__(self, table_id)
        LKMap.__init__(
            self,
            region_id,
            subregion_type,
            legend_title='% of Population',
            color_palette=color_palette,
        )
        self.field = field

    # Implement AbstractColoredView
    def get_color_value(self, id):
        d = self.lk_census_data[id]
        return d[self.field] / d[self.total_field]

    # Implement AbstractLabelledView
    def get_label(self, id):
        return self.region_id

    def get_label_value(self, id):
        return self.lk_census_data[id][self.field]
