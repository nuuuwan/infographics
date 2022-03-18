import os

from infographics._utils import log

DIR_NEW_EXAMPLES = 'new_examples'


def example_svg_file_name(file):
    return '/tmp/infographics.' + os.path.basename(file)[:-3] + '.svg'


def main():
    for file_only in sorted(os.listdir('new_examples')):
        if file_only[-3:] == '.py' and file_only != 'examples.py':
            py_file = os.path.join(DIR_NEW_EXAMPLES, file_only)
            cmd = f'python3 {py_file}'
            log.debug(f'Running "{cmd}"')
            os.system(cmd)


if __name__ == '__main__':
    main()
