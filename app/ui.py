import math
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from .storage import JsonStorage
from .tracker import MouseTracker


BG = "#0b1118"
PANEL = "#151c24"
PANEL_SOFT = "#101821"
BORDER = "#243140"
TEXT = "#f3f7fb"
MUTED = "#8fa0b3"
SUBTLE = "#5f7287"
GREEN = "#3fb950"
GREEN_DARK = "#173323"
BLUE = "#58a6ff"
BLUE_DARK = "#12263b"
PURPLE = "#9d7cff"
PURPLE_DARK = "#241c36"
RED = "#f85149"
ORANGE = "#f0883e"
ORANGE_DARK = "#331f14"
HEAT_LOW = "#263444"
HEAT_BORDER = "#303d4a"
FOOTBALL_FIELD_M = 91.44
BUS_M = 12.0
CRICKET_PITCH_LAP_M = 46.34
ICON_FONT = ("Segoe MDL2 Assets", 13)
ICON_FONT_LARGE = ("Segoe MDL2 Assets", 16)
ICONS = {
    "distance": "\uE707",
    "speed": "\uE945",
    "max_speed": "\uE9D9",
    "time": "\uE121",
    "left": "\uE962",
    "right": "\uE962",
    "scroll": "\uE7F4",
    "heatmap": "\uE80F",
    "compare": "\uE7C1",
    "field": "\uE7C1",
    "bus": "\uE806",
    "cricket": "\uE7FC",
    "play": "\u25B6",
    "pause": "\u2016",
    "reset": "\u21BB",
    "save": "\u25A3",
}


class MouseMileageApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Mouse Mileage")
        self.root.geometry("1180x720")
        self.root.minsize(980, 640)
        self.root.configure(bg=BG)
        self.storage = JsonStorage()
        self.tracker = MouseTracker()
        self.screen_width_px = self.root.winfo_screenwidth()
        self.screen_height_px = self.root.winfo_screenheight()
        self.session_started_at = None

        self.width_var = tk.StringVar(value=f"{self.storage.load_screen_width_cm():g}")
        self.status_var = tk.StringVar(value="\u25cf Paused")
        self.session_var = tk.StringVar(value="Ready")
        self.values = {name: tk.StringVar(value="-") for name in (
            "pixels", "physical", "speed", "speed_physical", "max_speed",
            "max_speed_physical", "left", "right", "scroll", "duration", "duration_plain"
        )}
        self.comparisons = {name: tk.StringVar(value="-") for name in (
            "fields", "buses", "cricket"
        )}

        self._configure_style()
        self._build()
        self.tracker.start_listener()
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self._refresh()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Soft.TFrame", background=PANEL_SOFT)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Soft.TLabel", background=PANEL_SOFT, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI Semibold", 28))
        style.configure("Subtitle.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 11))
        style.configure("Badge.TLabel", background=BLUE_DARK, foreground=BLUE, font=("Segoe UI Semibold", 9))
        style.configure("Status.TLabel", background=GREEN_DARK, foreground=GREEN, font=("Segoe UI Semibold", 10))
        style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("PanelMuted.TLabel", background=PANEL, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background=PANEL, foreground=MUTED, font=("Segoe UI Semibold", 9))
        style.configure("Metric.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 23))
        style.configure("MetricDetail.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 18))
        style.configure("MetricSmall.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 19))
        style.configure("SectionTitle.TLabel", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 19))
        style.configure("Hint.TLabel", background=PANEL, foreground=SUBTLE, font=("Segoe UI", 9))
        style.configure("Compare.TLabel", background=PANEL, foreground=BLUE, font=("Segoe UI Semibold", 22))
        style.configure("IconBadge.TLabel", background=BLUE_DARK, foreground=BLUE, font=ICON_FONT, anchor="center")
        style.configure("IconBadgeGreen.TLabel", background=GREEN_DARK, foreground=GREEN, font=ICON_FONT, anchor="center")
        style.configure("IconBadgeRed.TLabel", background=ORANGE_DARK, foreground=ORANGE, font=ICON_FONT, anchor="center")
        style.configure("IconBadgePurple.TLabel", background=PURPLE_DARK, foreground=PURPLE, font=ICON_FONT, anchor="center")
        style.configure("PanelIcon.TLabel", background=PANEL, foreground=BLUE, font=ICON_FONT_LARGE)
        style.configure("CompareIcon.TLabel", background=PANEL, foreground=BLUE, font=ICON_FONT)
        style.configure("TEntry", fieldbackground=PANEL_SOFT, foreground=TEXT, insertcolor=TEXT, bordercolor=BORDER)
        style.configure("Primary.TButton", background=GREEN, foreground="#06150b", font=("Segoe UI Semibold", 10), padding=(20, 10))
        style.configure("Secondary.TButton", background=PANEL, foreground=TEXT, font=("Segoe UI Semibold", 10), padding=(18, 10))
        style.configure("Save.TButton", background=BLUE, foreground="#07111d", font=("Segoe UI Semibold", 10), padding=(20, 10))
        style.map("Primary.TButton", background=[("active", "#56d364")], foreground=[("active", "#06150b")])
        style.map("Secondary.TButton", background=[("active", "#1b2530")], foreground=[("active", TEXT)])
        style.map("Save.TButton", background=[("active", "#79c0ff")], foreground=[("active", "#07111d")])

    def _build(self) -> None:
        outer = ttk.Frame(self.root, style="App.TFrame", padding=24)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(3, weight=1)

        self._build_header(outer)
        self._build_metrics(outer)
        self._build_dashboard_body(outer)
        self._build_controls(outer)

    def _build_header(self, parent) -> None:
        header = ttk.Frame(parent, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)

        title_row = ttk.Frame(header, style="App.TFrame")
        title_row.grid(row=0, column=0, sticky="w")
        ttk.Label(title_row, text="Mouse Mileage", style="Title.TLabel").pack(side="left")
        ttk.Label(title_row, text="v1.0", style="Badge.TLabel", padding=(10, 4)).pack(side="left", padx=(12, 0), pady=(9, 0))
        ttk.Label(header, text="Track. Measure. Compare. Repeat.", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 0))

        status_box = ttk.Frame(header, style="App.TFrame")
        status_box.grid(row=0, column=1, rowspan=2, sticky="e")
        ttk.Label(status_box, textvariable=self.status_var, style="Status.TLabel", padding=(14, 7)).pack(anchor="e")
        ttk.Label(status_box, textvariable=self.session_var, style="Muted.TLabel").pack(anchor="e", pady=(6, 0))

    def _build_metrics(self, parent) -> None:
        metrics = ttk.Frame(parent, style="App.TFrame")
        metrics.grid(row=1, column=0, sticky="ew")
        for col in range(4):
            metrics.columnconfigure(col, weight=1, uniform="metrics")

        self._metric_card(
            metrics, 0, 0, "TOTAL DISTANCE", self.values["pixels"], self.values["physical"],
            BLUE, icon=ICONS["distance"], detail_style="MetricDetail.TLabel"
        )
        self._metric_card(
            metrics, 0, 1, "CURRENT SPEED", self.values["speed"], self.values["speed_physical"],
            GREEN, icon=ICONS["speed"], icon_style="IconBadgeGreen.TLabel", detail_style="MetricDetail.TLabel"
        )
        self._metric_card(
            metrics, 0, 2, "MAX SPEED", self.values["max_speed"], self.values["max_speed_physical"],
            ORANGE, icon=ICONS["max_speed"], icon_style="IconBadgeRed.TLabel", detail_style="MetricDetail.TLabel"
        )
        self._metric_card(
            metrics, 0, 3, "ACTIVE TIME", self.values["duration"], self.values["duration_plain"],
            PURPLE, icon=ICONS["time"], icon_style="IconBadgePurple.TLabel"
        )

        click_row = ttk.Frame(parent, style="App.TFrame")
        click_row.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        for col in range(3):
            click_row.columnconfigure(col, weight=1, uniform="clicks")
        self._metric_card(click_row, 0, 0, "LEFT CLICKS", self.values["left"], tk.StringVar(value="Primary button"), BLUE, small=True, icon=ICONS["left"])
        self._metric_card(click_row, 0, 1, "RIGHT CLICKS", self.values["right"], tk.StringVar(value="Secondary button"), BLUE, small=True, icon=ICONS["right"])
        self._metric_card(click_row, 0, 2, "SCROLL EVENTS", self.values["scroll"], tk.StringVar(value="Wheel activity"), BLUE, small=True, icon=ICONS["scroll"])

    def _metric_card(
        self, parent, row, column, title, value_var, detail_var, accent,
        small=False, icon=None, icon_style="IconBadge.TLabel", detail_style="Hint.TLabel"
    ) -> None:
        card = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, bd=0)
        card.grid(row=row, column=column, sticky="nsew", padx=6)
        card.columnconfigure(0, weight=1)

        tk.Frame(card, bg=accent, height=3).grid(row=0, column=0, sticky="ew")
        body = ttk.Frame(card, style="Panel.TFrame", padding=(14, 11, 14, 12))
        body.grid(row=1, column=0, sticky="nsew")
        heading = ttk.Frame(body, style="Panel.TFrame")
        heading.pack(fill="x")
        if icon:
            ttk.Label(heading, text=icon, style=icon_style, padding=(8, 6)).pack(side="left", padx=(0, 9))
        ttk.Label(heading, text=title, style="CardTitle.TLabel").pack(side="left", anchor="center")
        ttk.Label(body, textvariable=value_var, style="MetricSmall.TLabel" if small else "Metric.TLabel").pack(anchor="w", pady=(6, 0))
        ttk.Label(body, textvariable=detail_var, style=detail_style).pack(anchor="w")

    def _build_dashboard_body(self, parent) -> None:
        body = ttk.Frame(parent, style="App.TFrame")
        body.grid(row=3, column=0, sticky="nsew", pady=(14, 0))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        heat_panel = tk.Frame(body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, bd=0)
        heat_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        heat_panel.columnconfigure(0, weight=1)
        heat_panel.rowconfigure(1, weight=1)

        heat_header = ttk.Frame(heat_panel, style="Panel.TFrame", padding=(16, 13, 16, 7))
        heat_header.grid(row=0, column=0, sticky="ew")
        heat_header.columnconfigure(0, weight=1)
        heat_title = ttk.Frame(heat_header, style="Panel.TFrame")
        heat_title.grid(row=0, column=0, sticky="w")
        ttk.Label(heat_title, text=ICONS["heatmap"], style="PanelIcon.TLabel").pack(side="left", padx=(0, 8))
        ttk.Label(heat_title, text="Cursor Heatmap", style="SectionTitle.TLabel").pack(side="left")
        ttk.Label(heat_header, text="Where your mouse has been", style="PanelMuted.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 0))
        legend = ttk.Frame(heat_header, style="Panel.TFrame")
        legend.grid(row=0, column=1, rowspan=2, sticky="e")
        ttk.Label(legend, text="Less", style="PanelMuted.TLabel").pack(side="left", padx=(0, 7))
        for index, color in enumerate((HEAT_LOW, "#34516f", BLUE, "#d36b52", RED)):
            tk.Frame(legend, bg=color, width=12, height=8).pack(side="left", padx=(0 if index == 0 else 3, 0))
        ttk.Label(legend, text="More", style="PanelMuted.TLabel").pack(side="left", padx=(7, 0))

        canvas_shell = ttk.Frame(heat_panel, style="Panel.TFrame", padding=(16, 7, 16, 10))
        canvas_shell.grid(row=1, column=0, sticky="nsew")
        canvas_shell.columnconfigure(0, weight=1)
        canvas_shell.rowconfigure(0, weight=1)
        self.heatmap_canvas = tk.Canvas(
            canvas_shell,
            height=260,
            bg=PANEL_SOFT,
            highlightthickness=1,
            highlightbackground=HEAT_BORDER,
            bd=0,
        )
        self.heatmap_canvas.grid(row=0, column=0, sticky="nsew")

        calibration = ttk.Frame(heat_panel, style="Panel.TFrame", padding=(16, 3, 16, 14))
        calibration.grid(row=2, column=0, sticky="ew")
        ttk.Label(calibration, text="Physical screen width:", style="PanelMuted.TLabel").pack(side="left")
        ttk.Entry(calibration, textvariable=self.width_var, width=8).pack(side="left", padx=(9, 6))
        ttk.Label(calibration, text=f"cm    Detected width: {self.screen_width_px} px", style="PanelMuted.TLabel").pack(side="left")

        compare_panel = tk.Frame(body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, bd=0)
        compare_panel.grid(row=0, column=1, sticky="nsew")
        compare_panel.columnconfigure(0, weight=1)
        compare_panel.rowconfigure(1, weight=1)
        compare_header = ttk.Frame(compare_panel, style="Panel.TFrame", padding=(16, 13, 16, 8))
        compare_header.grid(row=0, column=0, sticky="ew")
        compare_title = ttk.Frame(compare_header, style="Panel.TFrame")
        compare_title.pack(anchor="w")
        ttk.Label(compare_title, text=ICONS["compare"], style="PanelIcon.TLabel").pack(side="left", padx=(0, 8))
        ttk.Label(compare_title, text="Distance Comparisons", style="SectionTitle.TLabel").pack(side="left")
        ttk.Label(compare_header, text="Tiny cursor miles, made tangible", style="PanelMuted.TLabel").pack(anchor="w", pady=(2, 0))

        compare_body = ttk.Frame(compare_panel, style="Panel.TFrame", padding=(16, 3, 16, 14))
        compare_body.grid(row=1, column=0, sticky="nsew")
        for index, (label, key, detail, icon) in enumerate((
            ("Football fields", "fields", "100-yard field", ICONS["field"]),
            ("City buses", "buses", "approximately 12 m each", ICONS["bus"]),
            ("Cricket pitch laps", "cricket", "approximately 22 yards / 20.12 m", ICONS["cricket"]),
        )):
            item = ttk.Frame(compare_body, style="Panel.TFrame")
            item.pack(fill="x", expand=True)
            item.columnconfigure(1, weight=1)
            ttk.Label(item, text=icon, style="CompareIcon.TLabel", padding=(0, 4)).grid(row=0, column=0, rowspan=3, sticky="n", padx=(0, 10))
            ttk.Label(item, textvariable=self.comparisons[key], style="Compare.TLabel").grid(row=0, column=1, sticky="w")
            ttk.Label(item, text=label, style="CardTitle.TLabel").grid(row=1, column=1, sticky="w", pady=(1, 0))
            ttk.Label(item, text=detail, style="Hint.TLabel").grid(row=2, column=1, sticky="w")
            if index < 2:
                tk.Frame(compare_body, bg=BORDER, height=1).pack(fill="x", pady=8)

    def _build_controls(self, parent) -> None:
        controls = ttk.Frame(parent, style="App.TFrame")
        controls.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        controls.columnconfigure(2, weight=1)
        self.start_button = ttk.Button(controls, text=f"{ICONS['play']}  Start Tracking", style="Primary.TButton", command=self._toggle)
        self.start_button.grid(row=0, column=0, padx=(0, 10), sticky="w")
        ttk.Button(controls, text=f"{ICONS['reset']}  Reset", style="Secondary.TButton", command=self._reset).grid(row=0, column=1, sticky="w")
        ttk.Button(controls, text=f"{ICONS['save']}  Save Session", style="Save.TButton", command=self._save).grid(row=0, column=3, sticky="e")

    def _calibration(self, show_error=False):
        try:
            value = float(self.width_var.get())
            if not 5 <= value <= 500:
                raise ValueError
            return value
        except ValueError:
            if show_error:
                messagebox.showerror("Invalid calibration", "Enter a screen width between 5 and 500 cm.")
            return None

    def _toggle(self) -> None:
        if self.tracker.is_tracking():
            self.tracker.pause()
            self.start_button.configure(text=f"{ICONS['play']}  Resume Tracking")
            self.status_var.set("\u25cf Paused")
            self.session_var.set("Session paused")
        else:
            if self._calibration(show_error=True) is None:
                return
            self.tracker.start()
            if self.session_started_at is None:
                self.session_started_at = datetime.now()
            self.start_button.configure(text=f"{ICONS['pause']}  Pause Tracking")
            self.status_var.set("\u25cf Tracking globally")
            self.session_var.set(f"Started {self.session_started_at.strftime('%I:%M %p').lstrip('0')}")

    def _reset(self) -> None:
        self.tracker.reset()
        self.session_started_at = datetime.now() if self.tracker.is_tracking() else None
        if self.tracker.is_tracking():
            self.session_var.set(f"Started {self.session_started_at.strftime('%I:%M %p').lstrip('0')}")
        else:
            self.session_var.set("Ready")

    def _save(self) -> None:
        width = self._calibration(show_error=True)
        if width is None:
            return
        self.storage.save_screen_width_cm(width)
        self.storage.save_session(self.tracker.snapshot().to_record(self.screen_width_px, width))
        messagebox.showinfo("Session saved", "Your current session was saved locally.")

    @staticmethod
    def _time_text(seconds: float) -> str:
        total = int(seconds)
        hours, remainder = divmod(total, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    @staticmethod
    def _plain_time_text(seconds: float) -> str:
        if seconds < 60:
            return f"{int(seconds)} seconds active"
        minutes = seconds / 60
        if minutes < 60:
            return f"{minutes:.1f} minutes active"
        return f"{minutes / 60:.1f} hours active"

    def _refresh(self) -> None:
        stats = self.tracker.snapshot()
        width = self._calibration() or 0
        cm = stats.distance_px * width / self.screen_width_px
        distance_m = cm / 100
        self.values["pixels"].set(f"{stats.distance_px:,.0f} px")
        self.values["physical"].set(self._physical_distance_text(cm))
        self.values["speed"].set(f"{stats.current_speed_px_s:,.0f} px/s")
        self.values["speed_physical"].set(self._physical_speed_text(stats.current_speed_px_s, width))
        self.values["max_speed"].set(f"{stats.max_speed_px_s:,.0f} px/s")
        self.values["max_speed_physical"].set(self._physical_speed_text(stats.max_speed_px_s, width))
        self.values["left"].set(f"{stats.left_clicks:,}")
        self.values["right"].set(f"{stats.right_clicks:,}")
        self.values["scroll"].set(f"{stats.scroll_events:,}")
        self.values["duration"].set(self._time_text(stats.active_seconds))
        self.values["duration_plain"].set(self._plain_time_text(stats.active_seconds))
        self._update_comparisons(distance_m)
        self._draw_heatmap(stats)
        self.root.after(100, self._refresh)

    @staticmethod
    def _physical_distance_text(cm: float) -> str:
        if cm < 100:
            return f"{cm:,.2f} cm"
        if cm < 100_000:
            return f"{cm / 100:,.2f} m"
        return f"{cm / 100_000:,.3f} km"

    def _physical_speed_text(self, speed_px_s: float, screen_width_cm: float) -> str:
        if not self.screen_width_px or not screen_width_cm:
            return "0.00 m/s"
        meters_per_second = speed_px_s * screen_width_cm / self.screen_width_px / 100
        if meters_per_second < 1:
            return f"{meters_per_second:.2f} m/s"
        return f"{meters_per_second:,.1f} m/s"

    def _update_comparisons(self, distance_m: float) -> None:
        self.comparisons["fields"].set(self._comparison_text(distance_m, FOOTBALL_FIELD_M))
        self.comparisons["buses"].set(self._comparison_text(distance_m, BUS_M))
        self.comparisons["cricket"].set(self._comparison_text(distance_m, CRICKET_PITCH_LAP_M))

    @staticmethod
    def _comparison_text(distance_m: float, unit_m: float) -> str:
        if distance_m <= 0 or unit_m <= 0:
            return "0.00x"
        value = distance_m / unit_m
        if value < 10:
            return f"{value:.2f}x"
        if value < 100:
            return f"{value:.1f}x"
        return f"{value:,.0f}x"

    def _draw_heatmap(self, stats) -> None:
        canvas = self.heatmap_canvas
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1 or height <= 1:
            return

        if not stats.heatmap_cells:
            canvas.create_text(
                width / 2,
                height / 2,
                text="Move the cursor to build the heatmap",
                fill=MUTED,
                font=("Segoe UI", 10),
            )
            canvas.create_rectangle(0, 0, width - 1, height - 1, outline=HEAT_BORDER)
            return

        max_seconds = max(stats.heatmap_cells.values())
        if max_seconds <= 0:
            return

        cell_px = self.tracker.HEATMAP_CELL_PX
        for key, seconds in stats.heatmap_cells.items():
            try:
                col_text, row_text = key.split(",", 1)
                col = int(col_text)
                row = int(row_text)
            except ValueError:
                continue

            screen_x1 = col * cell_px
            screen_y1 = row * cell_px
            screen_x2 = screen_x1 + cell_px
            screen_y2 = screen_y1 + cell_px
            if screen_x2 < 0 or screen_y2 < 0:
                continue
            if screen_x1 > self.screen_width_px or screen_y1 > self.screen_height_px:
                continue

            x1 = max(0, screen_x1 / self.screen_width_px * width)
            y1 = max(0, screen_y1 / self.screen_height_px * height)
            x2 = min(width, screen_x2 / self.screen_width_px * width)
            y2 = min(height, screen_y2 / self.screen_height_px * height)
            intensity = math.log1p(seconds) / math.log1p(max_seconds)
            canvas.create_rectangle(x1, y1, x2, y2, fill=self._heat_color(intensity), outline="")

        canvas.create_rectangle(0, 0, width - 1, height - 1, outline=HEAT_BORDER)

    @staticmethod
    def _heat_color(intensity: float) -> str:
        intensity = max(0.0, min(1.0, intensity))
        if intensity < 0.55:
            return MouseMileageApp._blend_color(HEAT_LOW, BLUE, intensity / 0.55)
        return MouseMileageApp._blend_color(BLUE, RED, (intensity - 0.55) / 0.45)

    @staticmethod
    def _blend_color(start: str, end: str, amount: float) -> str:
        amount = max(0.0, min(1.0, amount))
        start_rgb = tuple(int(start[index:index + 2], 16) for index in (1, 3, 5))
        end_rgb = tuple(int(end[index:index + 2], 16) for index in (1, 3, 5))
        blended = tuple(
            round(start_value + (end_value - start_value) * amount)
            for start_value, end_value in zip(start_rgb, end_rgb)
        )
        return f"#{blended[0]:02x}{blended[1]:02x}{blended[2]:02x}"

    def _close(self) -> None:
        self.tracker.pause()
        self.tracker.stop_listener()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()
