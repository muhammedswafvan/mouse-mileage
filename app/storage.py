import json
from pathlib import Path


class JsonStorage:
    def __init__(self) -> None:
        base = Path.home() / "AppData" / "Local" / "MouseMileage"
        base.mkdir(parents=True, exist_ok=True)
        self.settings_path = base / "settings.json"
        self.history_path = base / "sessions.json"

    @staticmethod
    def _read(path: Path, default):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return default

    @staticmethod
    def _write(path: Path, data) -> None:
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temp.replace(path)

    def load_screen_width_cm(self) -> float:
        return float(self._read(self.settings_path, {}).get("screen_width_cm", 34.5))

    def save_screen_width_cm(self, value: float) -> None:
        self._write(self.settings_path, {"screen_width_cm": value})

    def save_session(self, record: dict) -> None:
        history = self._read(self.history_path, [])
        history.append(record)
        self._write(self.history_path, history)
