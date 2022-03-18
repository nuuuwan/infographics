from functools import cached_property

from gig import ext_data

from infographics._utils import log

DATA_GROUP = 'census'


class LKCensusData:
    def __init__(self, table_id):
        self.table_id = table_id

    @cached_property
    def total_field(self):
        return 'total_population'

    @cached_property
    def data(self):
        log.debug('[expensive] calling ext_data._get_table_index')
        return ext_data._get_table_index(DATA_GROUP, self.table_id)
