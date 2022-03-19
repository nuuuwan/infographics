"""Tests for infographics."""
import os
import unittest

from infographics.base import dorling_compress
DIR_EXAMPLES = 'new_examples'

class TestCase(unittest.TestCase):
    """Tests."""

    def test_examples(self):
        os.system('rm -rf /tmp/infographics.example*')
        for file_only in os.listdir(DIR_EXAMPLES):
            file = os.path.join(DIR_EXAMPLES, file_only)
            os.system(f'python3 {file}')

            i = file_only[7]
            svg_file = f'/tmp/infographics.example{i}.svg'
            self.assert_(os.path.exists())


if __name__ == '__main__':
    unittest.main()
