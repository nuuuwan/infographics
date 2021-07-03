"""Tests for cartogram."""

import unittest

from cartogram import run_cartogram


class TestCase(unittest.TestCase):
    """Tests."""

    def test_run_cartogram(self):
        """Test."""
        self.assertTrue(run_cartogram.run_cartogram())


if __name__ == '__main__':
    unittest.main()
