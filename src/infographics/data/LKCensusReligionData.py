

from infographics.data.LKCensusData import LKCensusData


class LKCensusReligionData(LKCensusData):
    TABLE_ID = 'religions_affiliation_of_population'

    def __init__(self):
        LKCensusData.__init__(self, LKCensusReligionData.TABLE_ID)
