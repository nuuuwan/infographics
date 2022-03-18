"""Tests for infographics."""

import unittest

from src.infographics.base import dorling_compress


class TestCase(unittest.TestCase):
    """Tests."""

    def test_compress(self):
        """Test."""
        points = [
            {'x': 0.25, 'y': 0.25, 'r': 0.01, 'color': 'r'},
            {'x': 0.25, 'y': 0.75, 'r': 0.02, 'color': 'g'},
            {'x': 0.75, 'y': 0.25, 'r': 0.04, 'color': 'b'},
            {'x': 0.75, 'y': 0.75, 'r': 0.03, 'color': 'orange'},
        ]
        compressed_points = dorling_compress._compress(points, [0, 0, 1, 1])
        self.assertEqual(points, compressed_points)


if __name__ == '__main__':
    unittest.main()
