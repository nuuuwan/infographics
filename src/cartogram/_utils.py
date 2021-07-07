"""Utils."""

import logging

from matplotlib.patches import Patch

from elections_lk import presidential

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cartogram')


def party_to_rgb_color(party_id):
    """Get RGB color of party."""
    if party_id in ['NDF', 'UNP']:
        return (0, 0.5, 0)
    if party_id in ['UPFA', 'PA', 'SLFP']:
        return (0, 0, 0.8)
    if party_id in ['SLPP']:
        return (0.5, 0, 0)
    if party_id in ['NPP', 'JVP', 'NMPP']:
        return (0.8, 0, 0)
    if party_id in ['SLMP']:
        return (0.8, 0, 0.8)
    if party_id in ['ACTC']:
        return (0.8, 0.8, 0)

    return (0.8, 0.8, 0.8)


def _default_p_to_a(p):
    min_p = 0.45
    return max(0, p - min_p) / (1 - min_p)


def party_to_rgba_color(
    party_id,
    p_votes,
    p_to_a=_default_p_to_a,
):
    """Get RGBA color of party."""
    (r, g, b) = party_to_rgb_color(party_id)
    return (r, g, b, p_to_a(p_votes))


def get_party_result(result, party_id):
    """Get party result."""
    for_partys = list(filter(
        lambda d: d['party_id'] == party_id,
        result['by_party'],
    ))
    return for_partys[0] if len(for_partys) == 1 else None


def get_winning_party_info(result):
    """Get winning party result."""
    return result['by_party'][0]


def dict_get(_dict, keys):
    """Get dict values by keys."""
    return [_dict[key] for key in keys]


def dict_set(_dict, keys, values):
    """Set dict values by keys."""
    for key, value in zip(keys, values):
        _dict[key] = value
    return _dict


def draw_color_legend(plt, labels_and_colors):
    """Draw color legend."""
    patches = []
    for label, color in labels_and_colors:
        patches.append(Patch(
            color=color,
            label=label,
        ))
    plt.legend(handles=patches)


def get_election_data_index(year):
    """Get election data, indexed by PD."""
    election_data = presidential.get_election_data(year)
    return dict(zip(
        list(map(lambda result: result['pd_id'], election_data)),
        election_data,
    ))
