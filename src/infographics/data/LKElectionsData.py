
from infographics.data.GIGData import GIGData

DATA_GROUP = 'elections'


class LKElectionsData(GIGData):
    def __init__(self, table_id):
        GIGData.__init__(self, DATA_GROUP, table_id)
        self.source_text = 'Data Source: elections.gov.lk'

    def get_color_value_to_label(self, color_value):
        return color_value.upper()

    def get_color_value_to_color(self, color_value):
        return {
            'SLPP': 'maroon',

            'UNP': 'green',
            'SJB': 'lightgreen',
            'NDF': 'green',

            'SLFP': 'blue',
            'UPFA': 'blue',
            'PA': 'blue',

            'EPDP': 'red',
            'TMVP': 'red',
            'ITAK': 'yellow',
            'ACTC': 'yellow',

            'MNA': 'darkgreen',

            'SLMP': 'purple',

        }.get(color_value, 'gray')
