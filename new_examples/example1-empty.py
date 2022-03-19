from infographics.core import Infographic
from new_examples.run_all_examples import example_svg_file_name


def main():
    infographic = Infographic()
    infographic.save(example_svg_file_name(__file__))


if __name__ == '__main__':
    main()
