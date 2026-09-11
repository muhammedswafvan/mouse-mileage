import unittest

from app.ui import MouseMileageApp


class DistanceComparisonTests(unittest.TestCase):
    def test_comparison_text_formats_small_medium_and_large_values(self) -> None:
        self.assertEqual(MouseMileageApp._comparison_text(0, 12), "0.00x")
        self.assertEqual(MouseMileageApp._comparison_text(6, 12), "0.50x")
        self.assertEqual(MouseMileageApp._comparison_text(180, 12), "15.0x")
        self.assertEqual(MouseMileageApp._comparison_text(12000, 12), "1,000x")


if __name__ == "__main__":
    unittest.main()
