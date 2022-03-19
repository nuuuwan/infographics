import os

def get_svg_file_name(file):
    return '/tmp/infographics.' + os.path.basename(file)[:-3] + '.svg'


def save(infographic, file):
    infographic.save(get_svg_file_name(file))
