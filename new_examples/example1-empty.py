from infographics.core import Infographic
from new_examples.run_all_examples import save


def main():
    infographic = Infographic()
    save(infographic, __file__)


if __name__ == '__main__':
    main()
