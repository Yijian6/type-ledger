# Type Record

Minimal Windows desktop character counter:

- Runs in the background
- Listens to global keyboard input
- Stores only daily character counts
- Does not store typed content
- Minimizes to the system tray

## Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

## Behavior

- Visible characters count as `+1`
- `Space` counts by default
- `Enter` does not count by default
- `Backspace` subtracts `1` by default and never drops below `0`
- Closing the window hides it to the system tray
- Use the tray menu to show the window again or exit the app

## Data file

The app first tries:

```text
%APPDATA%\TypeRecord\data\daily_counts.json
```

If that path is not writable, it falls back to:

```text
<project>\data\daily_counts.json
```
