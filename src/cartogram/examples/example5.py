"""Example."""
import os
import matplotlib.pyplot as plt
from geo import geodata
from gig import ext_data
from cartogram import dorling
from elections_lk import presidential

religion_data = ext_data.get_table_data(
    'census',
    'religious_affiliation_of_population',
    entity_type='pd',
)
ethnic_data = ext_data.get_table_data(
    'census',
    'ethnicity_of_population',
    entity_type='pd',
)

year = 2019
election_data = presidential.get_election_data(year)
pd_to_result = dict(zip(
    list(map(lambda result: result['pd_id'], election_data)),
    election_data,
))


def _func_get_color(row):
    pd_id = row.id
    religion = religion_data[pd_id]
    ethnic = ethnic_data[pd_id]
    total = religion['total_population']


    p_sinhala = ethnic['sinhalese'] / total
    p_tamil = (ethnic['indian_tamil'] + ethnic['sri_lankan_tamil']) / total
    p_muslim = (ethnic['moor'] + ethnic['malay']) / total
    p_sinhala_buddhist = religion['buddhist'] / total
    p_sinhala_non_buddhist = p_sinhala - p_sinhala_buddhist

    if p_sinhala_buddhist > 0.9:
        return (0.5, 0, 0, 0.8)
    if p_sinhala_buddhist > 0.7:
        return (0.5, 0, 0, 0.4)

    if p_tamil > 0.9:
        return (1, 0.5, 0, 0.8)
    if p_tamil > 0.7:
        return (1, 0.5, 0, 0.4)

    if p_muslim > 0.9:
        return (0, 0.5, 0, 0.8)
    if p_muslim > 0.7:
        return (0, 0.5, 0, 0.4)

    return (0.5, 0.5, 0.5, 0.5)


def _func_get_radius_value(row):
    pd_id = row.id
    result = pd_to_result[pd_id]
    return result['summary']['electors']


def _func_render_label(ax, x, y, span_y, row):
    return

def _func_render_legend(ax, x0, y0, span_y, anchor_radius):
    x, y = x0, y0
    for label, color in [
        ['Sinhala-Buddhist > 90%', (0.5, 0, 0, 0.8)],
        ['Sinhala-Buddhist > 70%', (0.5, 0, 0, 0.4)],

        ['Tamil > 90%', (1, 0.5, 0, 0.8)],
        ['Tamil > 70%', (1, 0.5, 0, 0.4)],

        ['Muslim > 90%', (0, 0.5, 0, 0.8)],
        ['Muslim > 70%', (0, 0.5, 0, 0.4)],

        ['Others', (0.5, 0.5, 0.5, 0.5)],
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


gpd_df = geodata.get_region_geodata('EC-01', 'pd')
dorling.plot(
    gpd_df,
    func_get_radius_value=_func_get_radius_value,
    func_get_color=_func_get_color,
    func_render_label=_func_render_label,
    func_render_legend=_func_render_legend,
    anchor_radius=0.01,
    anchor_radius_value=100_000,
)
plt.suptitle('Data Source: https://elections.gov.lk', fontsize=8)
plt.title(f'{year} Sri Lankan Presidential Election - Sinhala+Buddhist')

image_file = f'/tmp/cartogram.presidential.sinhala_buddhist.png'
plt.savefig(image_file)
os.system(f'open {image_file}')
