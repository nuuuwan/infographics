"""Example."""
import os
import matplotlib.pyplot as plt
from geo import geodata

from cartogram import dorling
from elections_lk import presidential

year = 2010
election_data = presidential.get_election_data(year)

pd_to_result = dict(zip(
    list(map(lambda result: result['pd_id'], election_data)),
    election_data,
))


def _func_get_color(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    p = result['summary']['rejected'] / result['summary']['polled']
    a = min(1, p * 20)
    return (0.9, 0, 0, a)


def _func_get_radius_value(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    return result['summary']['rejected']


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
    anchor_radius=0.05,
    anchor_radius_value=1_000,
)
plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
plt.title(f'{year} Sri Lankan Presidential Election - Rejected Votes')

image_file = f'/tmp/cartogram.presidential.{year}.rejected.png'
plt.savefig(image_file)
os.system(f'open {image_file}')
