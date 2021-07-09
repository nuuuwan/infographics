from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

if __name__ == '__main__':
    Infographic(
        title='Sri Lanka',
        children=[LKMap(figure_text='Sri Lanka')],
    ).save('/tmp/infographics.example1.png')
