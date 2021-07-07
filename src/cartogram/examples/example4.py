"""Example."""
import os
import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling
from elections_lk import presidential

year1 = 2005
year2 = 2019
year1_party_id = 'UNP'
year2_party_id = 'NDF'

election_data1 = presidential.get_election_data(year1)
election_data2 = presidential.get_election_data(year2)

pd_to_result1 = dict(zip(
    list(map(lambda result: result['pd_id'], election_data1)),
    election_data1,
))
pd_to_result2 = dict(zip(
    list(map(lambda result: result['pd_id'], election_data2)),
    election_data2,
))


def _func_get_color(row):
    pd_id = row.id
    result1 = pd_to_result1[pd_id]
    result2 = pd_to_result2[pd_id]
    by_party1 = result1['by_party']
    by_party2 = result2['by_party']

    for for_party in by_party1:
        if for_party['party_id'] == year1_party_id:
            p1 = for_party['votes'] / result1['summary']['valid']
    for for_party in by_party2:
        if for_party['party_id'] == year2_party_id:
            p2 = for_party['votes'] / result2['summary']['valid']

    dp = abs(p1 - p2)
    a = min(1, dp * 10)
    if p1 > p2:
        return (0.5, 0, 0, a)
    return (0, 0.5, 0, a)


def _func_get_radius_value(row):
    pd_id = row.id
    result1 = pd_to_result1[pd_id]
    result2 = pd_to_result2[pd_id]
    by_party1 = result1['by_party']
    by_party2 = result2['by_party']

    for for_party in by_party1:
        if for_party['party_id'] == year1_party_id:
            n1 = for_party['votes']
    for for_party in by_party2:
        if for_party['party_id'] == year2_party_id:
            n2 = for_party['votes']

    return abs(n1 - n2)


def _func_render_label(ax, x, y, span_y, row):
    return
    pd_id = row.id
    result = pd_to_result[pd_id]
    by_party = result['by_party']
    winning_party_id = by_party[0]['party_id']
    valid = result['summary']['valid']
    winning_party_p = by_party[0]['votes'] / valid

    r2 = span_y / 40
    ax.text(
        x,
        y + r2,
        winning_party_id,
        verticalalignment='center',
        horizontalalignment='center',
        fontsize=8,
    )
    ax.text(
        x,
        y,
        '{:.0%}'.format(winning_party_p),
        verticalalignment='center',
        horizontalalignment='center',
        fontsize=9,
    )
    ax.text(
        x,
        y - r2,
        row['name'],
        verticalalignment='center',
        horizontalalignment='center',
        fontsize=5,
    )


gpd_df = geodata.get_region_geodata('LK', 'pd')
dorling.plot(
    gpd_df,
    func_get_radius_value=_func_get_radius_value,
    func_get_color=_func_get_color,
    func_render_label=_func_render_label,
    anchor_radius=0.08,
    anchor_radius_value=20_000,
    # anchor_radius=0.1,
    # anchor_radius_value=2000,
    # anchor_radius=0.1,
    # anchor_radius_value=5_000,
)
plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
plt.title(
    'Sri Lankan Presidential Election - '
    + f'{year1_party_id} in {year1} vs {year2_party_id} in {year2}'
)

image_file = '/tmp/cartogram.presidential.' \
    + f'{year1}.{year1_party_id}.vs.{year2}.{year2_party_id}.png'


plt.savefig(image_file)
os.system(f'open {image_file}')
