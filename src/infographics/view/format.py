

def as_number(num):
    if num > 1_000_000:
        num_x = num / 1_000_000
        return f'{num_x:1.1f}M'
    if num > 100_000:
        num_x = num / 10_000
        return f'{num_x:2.0f}0K'

    if num > 10_000:
        num_x = num / 1_000
        return f'{num_x:2.0f}K'

    if num > 1_000:
        num_x = num / 1_000
        return f'{num_x:1.1f}K'

    if num > 1_00:
        num_x = num / 10
        return f'{num_x:2.0f}0'

    if num > 1:
        return f'{num:2.0f}'

    return f'{num:.0%}'
