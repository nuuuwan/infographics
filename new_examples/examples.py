import os

DIR_NEW_EXAMPLES = 'new_examples'


def example_svg_file_name(file):
    return '/tmp/infographics.' + os.path.basename(file)[:-3] + '.svg'


def main():
    for file_only in os.listdir('new_examples'):
        if file_only[-3:] == '.py':
            py_file = os.path.join(DIR_NEW_EXAMPLES, file_only)
            os.system(f'python3 {py_file}')


if __name__ == '__main__':
    main()
