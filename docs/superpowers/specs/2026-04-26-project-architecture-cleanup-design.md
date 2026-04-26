# Project Cleanup And Architecture Refactor Design

**Date:** 2026-04-26

**Project:** Type Record

**Summary:** Reorganize the repository and split oversized modules so the codebase is easier to navigate and maintain, while preserving all current runtime behavior, data formats, and entry points.

## Goal

Clean up the project structure and clarify module responsibilities without changing product behavior.

This refactor should:

- keep `python app.py` working
- keep the current UI behavior and visual design intact
- keep configuration and persisted data formats unchanged
- keep existing tests passing
- make it obvious which file is responsible for which concern

## Current Problems

### Oversized UI Module

`type_record/ui.py` has grown into a mixed module that currently contains:

- theme tokens
- widget factories
- display formatting helpers
- main-window layout
- history dialog logic
- hourly dialog logic
- trend-chart drawing

This makes the UI layer hard to navigate and increases the chance of accidental coupling.

### Blurry Storage Boundary

`type_record/storage.py` is still the correct home for persistence, but it also contains a large amount of data sanitization and summary-building logic. That boundary is still acceptable for now, but it should be tightened rather than expanded further.

### Root Directory Noise

The repository root currently mixes:

- entry points
- source code
- runtime data
- generated caches
- design artifacts

The project is still understandable, but it no longer reads cleanly at a glance.

## Refactor Principles

### No Product Changes

This is a structural refactor, not a feature change.

Do not intentionally change:

- counting rules
- session rules
- tray behavior
- settings semantics
- file formats
- visual design direction

### Stable External Interfaces

The following must remain stable:

- root entry point `app.py`
- package import paths used by the app
- config file structure
- JSON storage layout
- test command behavior

### Prefer Extraction Over Reinvention

Move existing responsibilities into better files. Do not use this refactor to rename everything, redesign APIs unnecessarily, or introduce heavyweight architectural layers.

### Keep The Architecture Proportional

This project does not need an enterprise-style `domain/services/infrastructure` split. The refactor should produce a cleaner small-app architecture, not a more abstract one.

## Approved Target Structure

```text
type_record/
├─ app.py
├─ README.md
├─ requirements.txt
├─ requirements-dev.txt
├─ .gitignore
├─ assets/
├─ data/
├─ docs/
│  └─ superpowers/
│     ├─ specs/
│     └─ plans/
├─ tests/
└─ type_record/
   ├─ __init__.py
   ├─ app.py
   ├─ charting.py
   ├─ config.py
   ├─ counter.py
   ├─ i18n.py
   ├─ metrics.py
   ├─ storage.py
   ├─ tray.py
   └─ ui/
      ├─ __init__.py
      ├─ window.py
      ├─ dialogs.py
      ├─ theme.py
      ├─ widgets.py
      └─ formatting.py
```

## Module Responsibilities

### Root `app.py`

Keep a minimal root launcher so `python app.py` still works.

### `type_record/app.py`

Keep application composition and lifecycle wiring here:

- load config
- acquire single-instance guard
- create store
- configure logging
- create counter
- create window
- create tray
- wire callbacks

This remains the orchestration layer.

### `type_record/config.py`

Continue owning configuration loading, normalization, and atomic settings writes.

### `type_record/counter.py`

Continue owning keyboard-event handling, session snapshots, live counter state, and input heuristics.

### `type_record/storage.py`

Continue owning persistence and query access through `DailyCountStore`.

This file may still contain:

- JSON loading and fallback
- state sanitization
- atomic writes
- history queries
- summary queries

This refactor should not split storage into multiple files yet. The goal is to prevent further sprawl, not force a premature repository layer redesign.

### `type_record/metrics.py`

Continue owning pure text-statistics calculations.

No Tkinter, no file I/O, no stateful app logic.

### `type_record/charting.py`

Continue owning pure trend-geometry and smoothing helpers.

No Tkinter widget lifecycle logic.

### `type_record/tray.py`

Continue owning the tray controller and menu behavior.

### `type_record/ui/window.py`

New home for the main `CounterWindow` class and high-level screen-refresh coordination.

This file should keep:

- root window lifecycle
- main layout assembly
- refresh scheduling
- state-to-widget updates
- event hooks that belong directly to the main window

### `type_record/ui/dialogs.py`

New home for dialog-specific behavior currently embedded in the main UI module:

- settings dialog
- history dialog
- hourly dialog

The goal is not to build a separate dialog framework. The goal is simply to stop treating every popup as an inline method cluster inside one giant file.

### `type_record/ui/theme.py`

New home for UI tokens and presentation constants:

- colors
- fonts
- reusable spacing or border constants if needed

This must remain static and dependency-light.

### `type_record/ui/widgets.py`

New home for reusable widget-construction helpers currently embedded in the window class, such as:

- command buttons
- cards
- tiles
- trend stats
- status lines
- metric blocks

These helpers should stay small and presentation-focused.

### `type_record/ui/formatting.py`

New home for display-formatting helpers currently mixed into the window class, such as:

- duration formatting
- last-input formatting
- axis label formatting
- date-display helpers that are presentation-only

This file should not know about Tk widgets.

## Cleanup Scope

### In Scope

- reorganize the UI package
- move existing UI constants and helpers into focused files
- adjust imports
- update tests if import paths require it
- improve `.gitignore` coverage for obvious generated directories
- keep docs under `docs/superpowers/`
- keep runtime artifacts and caches out of the conceptual source layout

### Out Of Scope

- feature work
- UI redesign
- storage format changes
- new analytics model
- background-process behavior changes
- packaging or installer changes
- large storage subsystem split

## Execution Order

### 1. Root Cleanup

Clean up ignore rules and ensure generated directories are treated as generated, not as source structure.

### 2. Create `type_record/ui/`

Introduce the package and move non-behavioral UI pieces first:

- theme tokens
- formatting helpers
- widget helpers

This reduces the risk of circular imports before moving larger dialog and window logic.

### 3. Split Dialog Logic

Move dialog-specific code out of the giant UI file and into `dialogs.py`, keeping the behavior and call sites stable.

### 4. Move Main Window Module

Relocate the main `CounterWindow` implementation into `ui/window.py` and provide a stable import surface from `type_record.ui`.

### 5. Update Imports And Entry Points

Ensure the package still imports cleanly from:

- root `app.py`
- `type_record/app.py`
- tests

### 6. Verify Behavior

Run compilation and tests after the refactor.

## Import Compatibility Strategy

To avoid breaking the rest of the codebase during the split, `type_record/ui/__init__.py` should re-export `CounterWindow`.

That means existing import sites can continue using:

`from type_record.ui import CounterWindow`

even after the implementation moves to `type_record/ui/window.py`.

This keeps the refactor low-risk and limits call-site churn.

## Verification

Minimum validation required:

- `python -m compileall type_record`
- `python -m pytest`
- smoke check that `python app.py` still starts

If any import cycle appears during the split, resolve it by moving pure constants or pure helpers to lower-level modules rather than by adding ad-hoc runtime imports.

## Risks And Handling

### Circular Imports In UI Split

Risk:

`window.py`, `dialogs.py`, and `widgets.py` can easily begin depending on each other in both directions.

Handling:

Extract only pure helpers first. Keep ownership clear:

- `theme.py` and `formatting.py` should be leaf modules
- `widgets.py` may depend on `theme.py`
- `dialogs.py` may depend on `theme.py`, `widgets.py`, and `formatting.py`
- `window.py` may depend on all of them
- lower-level modules should not depend back on `window.py`

### Over-Splitting

Risk:

Turning a 1000-line file into too many tiny files can make navigation worse.

Handling:

Split only along clear responsibility boundaries already present in the code. Do not create files with vague ownership.

### Accidental UI Behavior Drift

Risk:

Moving code can accidentally alter initialization order, Tk variable setup, or widget wiring.

Handling:

Preserve construction order, keep callback signatures unchanged, and validate through tests plus startup smoke checks.

### Storage Scope Creep

Risk:

Once the refactor starts, it will be tempting to redesign `storage.py` more aggressively.

Handling:

Do not split storage in this round. Limit changes there to import or helper adjustments that are strictly necessary for the project cleanup.

## Success Criteria

This refactor is successful if:

- the repository root reads cleanly
- `type_record/ui.py` no longer exists as a single giant mixed-responsibility module
- the new UI package has clear file ownership
- the app still starts the same way
- tests still pass
- a future contributor can quickly tell where to edit visuals, dialogs, formatting, storage, or orchestration

## Recommendation

Implement this as a medium-sized structural refactor:

- split the UI layer now
- tighten boundaries without over-abstracting
- leave deeper storage redesign for a future change only if a real feature demands it
