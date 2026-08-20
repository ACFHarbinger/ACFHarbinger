import unittest
from src.svg_renderer import render_stats_svg, render_languages_svg
from src.constants import FALLBACK_STATS

class TestSvgRenderer(unittest.TestCase):
    def test_render_stats_svg(self):
        svg = render_stats_svg(FALLBACK_STATS)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("Total Stars:", svg)
        self.assertIn("Total Commits:", svg)
        self.assertIn(str(FALLBACK_STATS['rank']), svg)

    def test_render_languages_svg(self):
        svg = render_languages_svg(FALLBACK_STATS)
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("Most Used Languages", svg)
        self.assertIn("Python", svg)

if __name__ == "__main__":
    unittest.main()
