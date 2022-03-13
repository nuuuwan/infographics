from functools import cached_property

from gig import ext_data

from infographics._utils import log

DATA_GROUP = 'census'


class LKCensusData:
    DEFAULT_TABLE_ID = 'ethnicity_of_population'

    def __init__(self, table_id=DEFAULT_TABLE_ID):
        self.table_id = table_id

    @cached_property
    def total_field(self):
        return 'total_population'

    @cached_property
    def data(self):
        log.debug('[expensive] calling ext_data._get_table_index')
        if self.table_id == 'ethnicity_religion':
            ethnicity = ext_data._get_table_index(
                DATA_GROUP, 'ethnicity_of_population')
            religion = ext_data._get_table_index(
                DATA_GROUP, 'religious_affiliation_of_population')
            for id, d in religion.items():
                ethnicity[id] |= d
            return ethnicity
        return ext_data._get_table_index(DATA_GROUP, self.table_id)
