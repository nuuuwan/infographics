"""Tests for infographics."""

import unittest

from infographics.base import humanize


class TestCase(unittest.TestCase):
    """Tests."""

    def test_number(self):
        """Test."""
        for f, expected_s in [
            [1.234, '1.2'],
            [12.34, '12'],
            [123.4, '120'],
            [1234, '1.2K'],
            [12_340, '12K'],
            [123_400, '120K'],
            [1_234_000, '1.2M'],
            [12_340_000, '12M'],
            [123_400_000, '120M'],
            [1_234_000_000, '1.2B'],
        ]:
            actual_s = humanize.number(f)
            self.assertEqual(expected_s, actual_s)


if __name__ == '__main__':
    unittest.main()
