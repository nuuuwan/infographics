def number(f):
    for m, unit in [
        [1_000_000, 'M'],
        [1_000, 'K'],
    ]:
        if f > m:
            return number(f / m) + unit
    return f'{f:3.3g}'


def percent(p):
    for n_decimals in range(0, 3):
        p_limit = 0.1 ** (1 + n_decimals)
        if p > p_limit:
            format_str = '{p:.%d%%}' % (n_decimals)
            return format_str.format(p=p)
    return '<0.1%'
