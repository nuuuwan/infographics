"""Example."""
import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling
from elections_lk import presidential

year = 2019
election_data = presidential.get_election_data(year)

pd_to_result = dict(zip(
    list(map(lambda result: result['pd_id'], election_data)),
    election_data,
))


def _func_get_color(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    by_party = result['by_party']
    winning_party_id = by_party[0]['party_id']
    winning_party_p = by_party[0]['votes'] / result['summary']['valid']

    a = max(0, winning_party_p - 0.45) / 0.55
    if winning_party_id == 'SLPP':
        return (0.5, 0, 0, a)
    if winning_party_id in ['UPFA', 'PA', 'SLFP']:
        return (0, 0, 0.8, a)
    if winning_party_id in ['NDF', 'UNP']:
        return (0, 0.5, 0, a)
    if winning_party_id in ['JVP']:
        return (0.8, 0, 0, a)
    if winning_party_id in ['ACTC']:
        return (0.8, 0.8, 0, a)
    return (0, 0, 0, a)


def _func_get_radius_value(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    return result['summary']['valid']


gpd_df = geodata.get_region_geodata('LK', 'pd')
dorling.plot(
    gpd_df,
    func_get_radius_value=_func_get_radius_value,
    func_get_color=_func_get_color,
)

plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
plt.title(f'{year} Sri Lankan Presidential Election')
plt.show()
