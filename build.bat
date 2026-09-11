@echo off
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "Mouse Mileage" main.py
echo.
echo Build complete: dist\Mouse Mileage.exe
pause
