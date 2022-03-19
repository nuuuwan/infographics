"""Tests for infographics."""

import unittest

from infographics.base import dorling_compress


class TestCase(unittest.TestCase):
    """Tests."""

    def test_compress(self):
        """Test."""
        points = [
            [[0.25, 0.25], [0.01, 0.04]],
            [[0.25, 0.75], [0.02, 0.03]],
            [[0.75, 0.25], [0.04, 0.02]],
            [[0.75, 0.75], [0.03, 0.01]],
        ]
        compressed_points = dorling_compress._compress(points, [0, 0, 1, 1])
        self.assertEqual(points, compressed_points)


if __name__ == '__main__':
    unittest.main()
