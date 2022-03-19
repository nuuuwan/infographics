from infographics.core import Infographic
from new_examples.common import save


def build_infographic():
    return Infographic()



if __name__ == '__main__':
    save(build_infographic(), __file__)
