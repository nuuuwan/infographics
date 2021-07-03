"""Uploaded data to nuuuwan/cartogram:data branch."""

import os


def upload_data():
    """Upload data."""
    os.system('echo "test data" > /tmp/cartogram.test.txt')
    os.system('echo "# cartogram" > /tmp/README.md')


if __name__ == '__main__':
    upload_data()
