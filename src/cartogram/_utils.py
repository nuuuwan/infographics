"""Utils."""

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cartogram')


def _party_to_rgb_color(party_id):
    if party_id == 'NDF':
        return (0, 0.5, 0)
    if party_id == 'SLPP':
        return (0.5, 0, 0)
    if party_id in ['NPP', 'JVP', 'NMPP']:
        return (0.8, 0, 0)

    return (0.8, 0.8, 0.8)


def _default_p_to_a(p):
    return p

def _party_to_rgba_color(
    party_id,
    p_votes,
    p_to_a=_default_p_to_a,
):
    (r, g, b) = _party_to_rgb_color(party_id)
    return (r, g, b, p_to_a(p_votes))


def _get_party_result(result, party_id):
    for_partys = list(filter(
        lambda d: d['party_id'] == party_id,
        result['by_party'],
    ))
    return for_partys[0] if len(for_partys) == 1 else None


def _get_winning_party_info(result):
    return result['by_party'][0]
