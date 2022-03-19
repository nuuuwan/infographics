class Humanize:
    @staticmethod
    def int(f):
        for m, unit in [
            [1_000_000, 'M'],
            [1_000, 'K'],
        ]:
            if f > m:
                return Humanize.int(f / m) + unit
        return f'{f:3.3g}'

    @staticmethod
    def percent(p):
        if p > 0.1:
            return f'{p:.0%}'
        if p > 0.01:
            return f'{p:.1%}'
        if p > 0.001:
            return f'{p:.2%}'
        return '<0.1%'
