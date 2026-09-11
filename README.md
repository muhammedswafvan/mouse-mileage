# Mouse Mileage

## Hackathon demo quick start

Mouse Mileage is a dark Windows telemetry dashboard that tracks global cursor
distance, speed, clicks, scrolls, active time, heatmap dwell, and playful
distance comparisons.

Run from source:

```bat
pip install -r requirements.txt
python main.py
```

Run the packaged executable:

```bat
dist\Mouse Mileage.exe
```

Core technologies: Python, Tkinter, pynput, JSON local storage, and PyInstaller.

Main features: global mouse tracking, calibrated physical distance, current and
max speed, click and scroll counters, active session timer, cursor heatmap,
football-field/bus/cricket-pitch comparisons, reset, pause/resume, and local
session saving.

A dark Windows desktop app that tracks global cursor movement, speed, clicks,
scroll events, and active session time. It converts pixels to physical distance
using your monitor's measured width.

## Run from source

1. Install Python 3.10 or newer from https://python.org and enable **Add Python to PATH**.
2. Open Command Prompt in this folder.
3. Create and activate an environment:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Install dependencies and run:

   ```bat
   pip install -r requirements.txt
   python main.py
   ```

Enter the physical width of the screen's visible display area—not its diagonal
size or bezel-to-bezel width—then click **Start tracking**. Tracking continues
when the window is unfocused or minimized.

## Build a Windows executable

With the virtual environment active, double-click `build.bat` or run it from
Command Prompt. The standalone executable will be created at:

```text
dist\Mouse Mileage.exe
```

## Local data

Settings and saved sessions are stored as JSON under:

```text
%LOCALAPPDATA%\MouseMileage\
```

Saving creates a timestamped record in `sessions.json`. Reset clears only the
live counters; it does not delete saved history.

## Notes

- Distance conversion assumes square pixels and one consistent display scale.
- On multi-monitor setups with different pixel densities, physical distance is
  an estimate based on the primary screen calibration.
- Exceptionally large instantaneous speeds can occur when Windows or a program
  warps the cursor to a new position.
