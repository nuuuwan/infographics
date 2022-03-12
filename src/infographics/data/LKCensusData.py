from functools import cached_property
from gig import ext_data
from infographics._utils import log

DATA_GROUP = 'census'


class LKCensusData:
    def __init__(self, table_id='ethnicity_of_population'):
        self.table_id = table_id

    @cached_property
    def idx(self):
        log.debug('[expensive] calling ext_data._get_table_index')
        return ext_data._get_table_index(DATA_GROUP, self.table_id)

    def __len__(self):
        return len(self.idx)

    def __getitem__(self, id):
        return self.idx[id]

    def keys(self):
        return self.idx.keys()

    def values(self):
        return self.idx.values()

    def __iter__(self):
        for id in self.keys():
            yield id
