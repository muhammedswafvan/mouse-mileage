import math
import threading
import time
from dataclasses import replace

from pynput import mouse

from .models import TrackingStats


class MouseTracker:
    """Collects global mouse events on pynput's listener thread."""

    SPEED_SAMPLE_SECONDS = 0.10
    HEATMAP_CELL_PX = 80

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._stats = TrackingStats()
        self._tracking = False
        self._last_position = None
        self._last_move_time = None
        self._speed_sample_started_at = None
        self._speed_sample_distance = 0.0
        self._started_at = None
        self._accumulated_seconds = 0.0
        self._listener = mouse.Listener(
            on_move=self._on_move, on_click=self._on_click, on_scroll=self._on_scroll
        )

    def start_listener(self) -> None:
        self._listener.start()

    def stop_listener(self) -> None:
        self._listener.stop()

    def start(self) -> None:
        with self._lock:
            if not self._tracking:
                self._tracking = True
                self._started_at = time.monotonic()
                self._last_position = None
                self._last_move_time = None
                self._reset_speed_sample()

    def pause(self) -> None:
        with self._lock:
            if self._tracking:
                now = time.monotonic()
                self._accumulated_seconds += now - self._started_at
                if self._last_position is not None and self._last_move_time is not None:
                    self._record_heatmap_dwell(
                        self._last_position, now - self._last_move_time, self._stats
                    )
                self._tracking = False
                self._stats.current_speed_px_s = 0.0
                self._last_position = None
                self._last_move_time = None
                self._reset_speed_sample()

    def reset(self) -> None:
        with self._lock:
            was_tracking = self._tracking
            self._stats = TrackingStats()
            self._accumulated_seconds = 0.0
            self._started_at = time.monotonic() if was_tracking else None
            self._last_position = None
            self._last_move_time = None
            self._reset_speed_sample()

    def is_tracking(self) -> bool:
        with self._lock:
            return self._tracking

    def snapshot(self) -> TrackingStats:
        with self._lock:
            result = replace(self._stats)
            result.heatmap_cells = dict(self._stats.heatmap_cells)
            result.active_seconds = self._accumulated_seconds
            if self._tracking:
                now = time.monotonic()
                result.active_seconds += now - self._started_at
                if self._last_position is not None and self._last_move_time is not None:
                    self._record_heatmap_dwell(
                        self._last_position, now - self._last_move_time, result
                    )
                if self._last_move_time is not None and now - self._last_move_time > 0.25:
                    result.current_speed_px_s = 0.0
            return result

    def _on_move(self, x: int, y: int) -> None:
        now = time.monotonic()
        with self._lock:
            if not self._tracking:
                return
            position = (x, y)
            if self._last_position is not None and self._last_move_time is not None:
                distance = math.dist(self._last_position, position)
                elapsed = now - self._last_move_time
                self._stats.distance_px += distance
                self._record_heatmap_dwell(self._last_position, elapsed, self._stats)
                self._record_speed_sample(distance, now)
            self._last_position = position
            self._last_move_time = now

    def _record_speed_sample(self, distance: float, now: float) -> None:
        if self._speed_sample_started_at is None:
            self._speed_sample_started_at = self._last_move_time

        self._speed_sample_distance += distance
        sample_elapsed = now - self._speed_sample_started_at
        if sample_elapsed >= self.SPEED_SAMPLE_SECONDS:
            speed = self._speed_sample_distance / sample_elapsed
            self._stats.current_speed_px_s = speed
            self._stats.max_speed_px_s = max(self._stats.max_speed_px_s, speed)
            self._reset_speed_sample(now)

    def _reset_speed_sample(self, started_at=None) -> None:
        self._speed_sample_started_at = started_at
        self._speed_sample_distance = 0.0

    def _record_heatmap_dwell(
        self, position: tuple[int, int], elapsed: float, stats: TrackingStats
    ) -> None:
        if elapsed <= 0:
            return
        col = position[0] // self.HEATMAP_CELL_PX
        row = position[1] // self.HEATMAP_CELL_PX
        key = f"{col},{row}"
        stats.heatmap_cells[key] = stats.heatmap_cells.get(key, 0.0) + elapsed

    def _on_click(self, _x, _y, button, pressed: bool) -> None:
        if not pressed:
            return
        with self._lock:
            if not self._tracking:
                return
            if button == mouse.Button.left:
                self._stats.left_clicks += 1
            elif button == mouse.Button.right:
                self._stats.right_clicks += 1

    def _on_scroll(self, _x, _y, _dx, _dy) -> None:
        with self._lock:
            if self._tracking:
                self._stats.scroll_events += 1
