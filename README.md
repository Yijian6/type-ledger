# TypeLedger

**English** | [简体中文](./README.zh-CN.md)

A calm, privacy-first Windows typing tracker for understanding your daily output, writing rhythm, and weekly efficiency.

TypeLedger runs locally in the background, lives in the system tray, and records aggregate typing metrics only. It helps you see whether you are building a consistent writing or coding rhythm without saving what you typed.

```text
Local first. No account. No raw text storage.
```

## At A Glance

| What | Details |
| --- | --- |
| Platform | Windows desktop |
| Best for | Writers, developers, researchers, students, knowledge workers |
| Interface | English and Simplified Chinese |
| Data | Local aggregate metrics |
| Privacy | No raw typed text, no clipboard content, no screenshots |
| Package | Portable Windows build with PyInstaller |

## Quick Links

- [中文 README](./README.zh-CN.md)
- [Run from source](#run-from-source)
- [Build the Windows app](#build-the-windows-app)
- [Release checklist](./docs/release-checklist.md)

## What It Helps You Understand

TypeLedger is built around a few practical questions:

- Did I actually write or code today?
- Is this week more productive than last week?
- Did output improve because I worked longer, or because I worked more efficiently?
- Which hours of the day are usually my most active?
- Am I building a more consistent rhythm over time?

## Core Features

| Area | What You Get |
| --- | --- |
| Daily tracking | Net count, keyboard input, pasted characters, backspaces, accuracy estimate |
| Session rhythm | Current session, last session, session length, recent activity |
| Speed estimate | CPM and WPM estimates based on recent keyboard input |
| Weekly efficiency | Weekly output, active time, active efficiency, comparison with last week and target |
| History | Daily records, 30-day trend, hourly distribution, CSV export |
| Tray app | Background mode, tray menu, quick access to settings and history |
| Localization | English and Simplified Chinese UI |

## Privacy Model

TypeLedger stores aggregate numbers only.

It records counts such as typed characters, pasted characters, backspaces, session length, hourly totals, and weekly summaries. It does not save raw typed text, clipboard content, window titles, website URLs, file names, screenshots, or keystroke sequences.

The app runs on your own Windows machine. No cloud account is required.

## Download And Use

Download the latest portable build from [GitHub Releases](https://github.com/Yijian6/type-ledger/releases):

```text
TypeLedger-windows-portable.zip
```

Then:

1. Extract the zip to a folder you trust.
2. Run `TypeLedger.exe`.
3. If the main window starts hidden, open it from the system tray.

The current build is unsigned. Windows SmartScreen or antivirus tools may warn because the app uses a global keyboard hook to count keystrokes. This is expected for local input trackers. TypeLedger does not store typed content.

Developers can also use the source workflow below.

## Run From Source

Requirements:

- Windows
- Python 3.11+

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Build The Windows App

Install development dependencies:

```powershell
.venv\Scripts\pip install -r requirements-dev.txt
```

Build the portable app:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_windows.ps1
```

Outputs:

```text
dist\TypeLedger\TypeLedger.exe
dist\TypeLedger-windows-portable.zip
```

## Local Data

TypeLedger stores local data under:

```text
%APPDATA%\TypeRecord\
```

The folder name remains `TypeRecord` for compatibility with earlier versions.

Main files:

- `data\daily_counts.json`
- `config\settings.json`
- `data\logs\type_record.log`

## Development

Run tests:

```powershell
python -m pytest
```

Run linting:

```powershell
ruff check .
```

## Status

TypeLedger is an early-stage personal productivity tool. The current focus is reliability, local-first privacy, clean Windows packaging, and a polished bilingual user experience.

## License

No license has been declared yet. Add a license before distributing broadly or accepting external contributions.
