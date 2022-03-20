from functools import cache

from gig import ext_data

from infographics._utils import log
from infographics.data.AbstractData import AbstractData

DATA_GROUP = 'census'


class LKCensusData(AbstractData):
    def __init__(self, table_id):
        self.table_id = table_id
        self.source_text = 'Data Source: 2012 Census (statistics.gov.lk)'

    @cache
    def get_data(self):
        log.debug('[expensive] calling ext_data._get_table_index')
        return ext_data._get_table_index(DATA_GROUP, self.table_id)

    @cache
    def get_id_to_total_population(self, id):
        return self[id]['total_population']

    def get_get_id_to_population(self, field_list):
        def get_id_to_population(id):
            return sum([self[id][field] for field in field_list])
        return get_id_to_population

    def get_get_id_to_p_population(self, field_list):
        get_id_to_population = self.get_get_id_to_population(field_list)

        def get_id_to_p_population(id):
            n_total = self.get_id_to_total_population(id)
            n_fields = get_id_to_population(id)
            return n_fields / n_total
        return get_id_to_p_population
