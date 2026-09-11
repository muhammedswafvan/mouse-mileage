from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


@dataclass
class TrackingStats:
    distance_px: float = 0.0
    current_speed_px_s: float = 0.0
    max_speed_px_s: float = 0.0
    left_clicks: int = 0
    right_clicks: int = 0
    scroll_events: int = 0
    active_seconds: float = 0.0
    heatmap_cells: dict[str, float] = field(default_factory=dict)

    def to_record(self, screen_width_px: int, screen_width_cm: float) -> dict:
        cm = self.distance_px * screen_width_cm / screen_width_px if screen_width_px else 0.0
        return {
            "saved_at": datetime.now(timezone.utc).isoformat(),
            **asdict(self),
            "screen_width_px": screen_width_px,
            "screen_width_cm": screen_width_cm,
            "distance_cm": cm,
            "distance_m": cm / 100,
            "distance_km": cm / 100_000,
        }
