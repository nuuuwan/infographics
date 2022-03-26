"""Tests for infographics."""
import os
import unittest

DIR_EXAMPLES = 'examples'


class TestCase(unittest.TestCase):
    """Tests."""

    def test_examples(self):
        os.system('rm -rf /tmp/infographics.example*')
        for file_only in os.listdir(DIR_EXAMPLES):
            if file_only[:7] != 'example':
                continue
            file = os.path.join(DIR_EXAMPLES, file_only)
            os.system(f'python3 {file}')

            i = file_only[7]
            svg_file = f'/tmp/infographics.example{i}.svg'
            self.assertTrue(os.path.exists(svg_file))


if __name__ == '__main__':
    unittest.main()
