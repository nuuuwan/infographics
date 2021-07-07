"""Example."""
import os
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

    a = winning_party_p
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

def _func_render_legend(ax, x0, y0, span_y, anchor_radius):
    x, y = x0, y0
    for label, color in [
        ['SLPP 75%', (0.5, 0, 0, 0.75)],
        ['SLPP 50%', (0.5, 0, 0, 0.5)],

        ['NDF 75%', (0, 0.5, 0, 0.75)],
        ['NDF 50%', (0, 0.5, 0, 0.5)],
    ]:
        r = span_y * 0.01
        y -= r
        ax.add_patch(plt.Circle(
            (x, y),
            r,
            color=color,
        ))
        ax.text(
            x + span_y * 0.01 * 2, y,
            label,
            verticalalignment='center',
        )
        y -= span_y * 0.01 * 3



gpd_df = geodata.get_region_geodata('LK', 'pd')
dorling.plot(
    gpd_df,
    func_get_radius_value=_func_get_radius_value,
    func_get_color=_func_get_color,
    func_render_label=_func_render_label,
    func_render_legend=_func_render_legend,
    anchor_radius=0.1,
    anchor_radius_value=200_000,
)

plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
plt.title(f'{year} Sri Lankan Presidential Election')

image_file = f'/tmp/cartogram.presidential.{year}.png'
plt.savefig(image_file)
os.system(f'open {image_file}')
