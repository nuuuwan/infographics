import os
import pkgutil

import new_examples
from infographics._utils import log


def example_svg_file_name(file):
    return '/tmp/infographics.' + os.path.basename(file)[:-3] + '.svg'


def main():
    for m in pkgutil.iter_modules(new_examples.__path__):
        if m.name == 'examples':
            continue
        log.info(f'Running: {m.name}.main()')
        mod = __import__(m.name)
        mod.main()


if __name__ == '__main__':
    main()
