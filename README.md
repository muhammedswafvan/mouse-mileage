
# 🖱️ Mouse Mileage

### Because apparently your cursor needed an odometer.

**Mouse Mileage** is a Windows desktop application that tracks how far your mouse cursor actually travels across your screen.

Cars have odometers. Bikes have odometers. Your mouse does all that travelling every day and gets absolutely no recognition.

Mouse Mileage fixes this completely unnecessary problem.

---

## 📸 Screenshot

<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/0abbf8b3-b068-4475-89e3-ca850c3a0d14" />

---

## ✨ What does it do?

Mouse Mileage runs in the background and globally tracks your mouse movement across Windows.

It measures:

- 🛣️ Total cursor distance travelled
- 📏 Physical distance in metres/kilometres
- ⚡ Current cursor speed
- 🚀 Maximum cursor speed
- 🖱️ Left clicks
- 🖱️ Right clicks
- 🛞 Scroll events
- ⏱️ Active tracking time
- 🔥 Cursor activity heatmap
- 💾 Session statistics

And, most importantly, it converts your cursor's journey into units that nobody asked for:

- ⚽ Football fields
- 🚌 City buses

---

## 🧠 How does it work?

Whenever the mouse moves, Mouse Mileage receives the cursor's new screen coordinates.

For two consecutive positions:

```text
(x₁, y₁) → (x₂, y₂)
```

the travelled distance is calculated using Euclidean distance:

```text
distance = √((x₂ - x₁)² + (y₂ - y₁)²)
```

These tiny movements are continuously accumulated to calculate the total cursor distance.

### But pixels aren't metres...

Correct.

Mouse Mileage lets the user enter the **physical width of their display in centimetres**.

For example, if:

```text
Screen resolution = 1920 pixels wide
Physical width    = 34.5 cm
```

then:

```text
cm per pixel = 34.5 / 1920
```

The accumulated pixel distance can then be converted into an approximate real-world physical distance.

So yes, when Mouse Mileage says your cursor travelled 1 kilometre, there is actual maths behind the stupidity.

---

## 🔥 Cursor Heatmap

Mouse Mileage also records where your cursor spends its time.

The screen is divided into regions and cursor activity is accumulated to generate a live heatmap.

This lets you scientifically answer important questions such as:

> "Which part of my monitor does my mouse visit the most?"

Humanity can finally move forward.

---

## 🌍 Global Tracking

Mouse Mileage uses global mouse listeners, which means tracking continues even when the application is:

- unfocused
- behind another window
- minimized

Your cursor cannot escape the odometer.

---

## 🛠️ Built With

- **Python**
- **Tkinter** — desktop GUI
- **pynput** — global mouse input tracking
- **PyInstaller** — Windows executable packaging

---

## 🚀 Running From Source

### 1. Clone the repository

```bash
git clone https://github.com/muhammedswafvan/mouse-mileage.git
cd mouse-mileage
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Mouse Mileage

```bash
python main.py
```

---

## 📦 Windows Executable

Mouse Mileage can also be packaged as a standalone Windows executable using PyInstaller.

```bash
pyinstaller "Mouse Mileage.spec"
```

The generated application will appear inside:

```text
dist/
└── Mouse Mileage.exe
```

The executable can run without manually starting the Python source code.

---

## 🎮 How to Use

1. Launch **Mouse Mileage**.
2. Enter the physical width of the visible part of your display in centimetres for more accurate physical-distance measurements.
3. Start tracking.
4. Use your computer normally.
5. Watch your cursor accumulate an alarming amount of mileage.
6. Pause or reset whenever you want.
7. Save the session if you want permanent evidence of your mouse's journey.

---

## 📊 Example

A session might look something like:

```text
Total Distance     508,680 px
Physical Distance  114.25 m
Current Speed      3,112 px/s
Maximum Speed      26,814 px/s
Active Time        00:07:00

Left Clicks        30
Right Clicks       0
Scroll Events      161
```

Which can then be translated into the far more useful:

```text
≈ 1.25 football fields
≈ 9.52 city buses
```

---

## 🧪 Tests

The project includes tests for the tracking and UI components.

Run them with:

```bash
python -m pytest
```

---

## 🤔 Why?

This project was built for a **Useless Project Hackathon**.

The goal was simple:

> Build something that genuinely works, measures something real, and solves a problem that absolutely nobody has.

Mouse Mileage doesn't pretend to increase your productivity.

It doesn't use AI to revolutionize your workflow.

It doesn't put your mouse movements on the blockchain.

It just tells you how far your cursor travelled.

And sometimes that's enough.

---

## 🔒 Privacy

Mouse Mileage tracks **mouse movement coordinates, clicks, scrolling, and session statistics** required for its functionality.

It does not need to record what you type or the contents of your screen.

Session information is stored locally by the application.

---

## 🏁 Project Status

**Hackathon build — v1.0**

The mouse is being monitored.

The mileage is accumulating.

There is no going back.

---

## 👨‍💻 Author

**Muhammed Swafvan**

**Faizan Luthyanvi**

B.Sc. Computer Science  
Farook College (Autonomous)

---



<p align="center">
  <b>Mouse Mileage</b><br>
  <i>Track. Measure. Compare. Repeat.</i>
</p>
