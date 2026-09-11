import threading
import unittest
from unittest.mock import patch

from app.models import TrackingStats
from app.tracker import MouseTracker


class MouseTrackerSpeedTests(unittest.TestCase):
    def make_tracker(self) -> MouseTracker:
        tracker = MouseTracker.__new__(MouseTracker)
        tracker._lock = threading.Lock()
        tracker._stats = TrackingStats()
        tracker._tracking = True
        tracker._last_position = None
        tracker._last_move_time = None
        tracker._speed_sample_started_at = None
        tracker._speed_sample_distance = 0.0
        tracker._started_at = 0.0
        tracker._accumulated_seconds = 0.0
        return tracker

    def test_speed_uses_sample_window_without_losing_distance(self) -> None:
        tracker = self.make_tracker()

        with patch("app.tracker.time.monotonic", side_effect=[0.0, 0.001, 0.002, 0.100]):
            tracker._on_move(0, 0)
            tracker._on_move(100, 0)
            tracker._on_move(200, 0)
            tracker._on_move(300, 0)

        self.assertEqual(tracker._stats.distance_px, 300)
        self.assertEqual(tracker._stats.current_speed_px_s, 3000)
        self.assertEqual(tracker._stats.max_speed_px_s, 3000)

    def test_tiny_interval_events_do_not_update_max_speed(self) -> None:
        tracker = self.make_tracker()

        with patch("app.tracker.time.monotonic", side_effect=[0.0, 0.001, 0.002]):
            tracker._on_move(0, 0)
            tracker._on_move(100, 0)
            tracker._on_move(200, 0)

        self.assertEqual(tracker._stats.distance_px, 200)
        self.assertEqual(tracker._stats.max_speed_px_s, 0)

    def test_heatmap_records_time_spent_in_previous_cell(self) -> None:
        tracker = self.make_tracker()

        with patch("app.tracker.time.monotonic", side_effect=[0.0, 2.0]):
            tracker._on_move(10, 10)
            tracker._on_move(90, 10)

        self.assertEqual(tracker._stats.heatmap_cells, {"0,0": 2.0})

    def test_snapshot_includes_current_stationary_heatmap_time(self) -> None:
        tracker = self.make_tracker()

        with patch("app.tracker.time.monotonic", side_effect=[0.0, 2.0]):
            tracker._on_move(10, 10)
            stats = tracker.snapshot()

        self.assertEqual(stats.heatmap_cells, {"0,0": 2.0})
        self.assertEqual(tracker._stats.heatmap_cells, {})


if __name__ == "__main__":
    unittest.main()
