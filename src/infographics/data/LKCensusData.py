from functools import cache, cached_property

from gig import ext_data

from infographics._utils import log

DATA_GROUP = 'census'


class LKCensusData:
    def __init__(self, table_id):
        self.table_id = table_id

    @property
    def total_field(self):
        return 'total_population'

    @cache
    def get_data(self):
        log.debug('[expensive] calling ext_data._get_table_index')
        return ext_data._get_table_index(DATA_GROUP, self.table_id)

    @cache
    def keys(self):
        return self.get_data().keys()

    def __getitem__(self, id):
        return self.get_data().get(id)

    def __len__(self):
        return len(self.keys())
