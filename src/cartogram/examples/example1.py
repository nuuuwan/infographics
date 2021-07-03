"""Example."""
import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling
from elections_lk import presidential

year = 2019
election_data = presidential.get_election_data()

pd_to_result = dict(zip(
    list(map(lambda result: result['pd_id'], election_data)),
    election_data,
))


def _func_get_color(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    by_party = result['by_party']

    for for_party in by_party:
        if for_party['party_id'] == 'NDF':
            a = for_party['votes'] / result['summary']['valid']
            return (0, 0.5, 0, a)


def _func_get_radius_value(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    by_party = result['by_party']

    for for_party in by_party:
        if for_party['party_id'] == 'NDF':
            return for_party['votes']


gpd_df = geodata.get_region_geodata('LK', 'pd')
dorling.plot(
    gpd_df,
    func_get_radius_value=_func_get_radius_value,
    func_get_color=_func_get_color,
)
plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
plt.title(f'{year} Sri Lankan Presidential Election')
plt.show()
