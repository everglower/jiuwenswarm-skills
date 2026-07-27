---
name: fitness-data-parser
version: 1.0.0
author: bunburya (adapted)
description: Parse fitness tracker data files (FIT, GPX, TCX) into structured Pandas DataFrames. Extract GPS tracks, heart rate, cadence, speed, and lap data from Garmin, Strava, and other fitness devices.
tags: [health, fitness, garmin, strava, gpx, fit, tcx]
license: MIT
---

# Fitness Data Parser Skill

## Overview

Parse fitness tracker data files in FIT (Garmin), GPX (Universal GPS), and TCX (Training Center XML) formats into structured Pandas DataFrames. Extract track points (GPS, heart rate, cadence, speed) and lap summaries (distance, time, max/avg heart rate).

## When to Use

- User provides a `.fit`, `.gpx`, or `.tcx` file from a fitness device
- User wants to analyze workout data (running, cycling, swimming, etc.)
- User needs to extract heart rate zones, pace, elevation, or GPS coordinates
- User wants to compare data across multiple workout files

## Prerequisites

- Python ≥3.8
- Dependencies: `pandas`, `fitdecode` (for FIT files), `gpxpy` (for GPX files)
- Install: `pip install pandas fitdecode gpxpy`
- Scripts location: `scripts/parse_fit.py`, `scripts/parse_gpx.py`, `scripts/parse_tcx.py`

## Workflow

### Step 1: Identify File Format

Determine the file type by extension:
- `.fit` - Garmin FIT format (binary), use `parse_fit.py`
- `.gpx` - GPS Exchange Format (XML), use `parse_gpx.py`
- `.tcx` - Training Center XML, use `parse_tcx.py`

### Step 2: Parse the File

#### FIT Files (Garmin)

```python
import sys
sys.path.insert(0, 'scripts')
from parse_fit import fit_to_dataframes

points_df, laps_df = fit_to_dataframes('/path/to/activity.fit')
```

Extracts:
- **Points DataFrame**: latitude, longitude, lap, altitude, timestamp, heart_rate, cadence, speed
- **Laps DataFrame**: number, start_time, total_distance, total_elapsed_time, max_speed, max_heart_rate, avg_heart_rate

#### GPX Files (Universal GPS)

```python
from parse_gpx import gpx_to_dataframe

points_df = gpx_to_dataframe('/path/to/activity.gpx')
```

Extracts: latitude, longitude, elevation, timestamp, heart_rate (if available in extensions)

#### TCX Files (Training Center XML)

```python
from parse_tcx import tcx_to_dataframes

points_df, laps_df = tcx_to_dataframes('/path/to/activity.tcx')
```

Extracts: latitude, longitude, altitude, timestamp, heart_rate, cadence, speed, distance

### Step 3: Analyze Data

With the parsed DataFrames, perform analysis:

```python
# Heart rate zones
max_hr = 220 - 30  # example
points_df['hr_zone'] = pd.cut(points_df['heart_rate'],
    bins=[0, max_hr*0.5, max_hr*0.6, max_hr*0.7, max_hr*0.8, max_hr],
    labels=['Z1', 'Z2', 'Z3', 'Z4', 'Z5'])

# Pace calculation (for running)
points_df['time_diff'] = points_df['timestamp'].diff().dt.total_seconds()
points_df['dist_diff'] = points_df['distance'].diff()
points_df['pace'] = points_df['time_diff'] / (points_df['dist_diff'] / 1000)  # sec/km

# Elevation gain
elevation_gain = points_df[points_df['altitude'].diff() > 0]['altitude'].diff().sum()
```

### Step 4: Output

Present results as:
- Summary table: total distance, duration, avg/max heart rate, elevation gain
- Heart rate zone distribution (time in each zone)
- Pace analysis (avg, min, max, splits)
- Lap-by-lap breakdown

## Supported Devices

- **FIT**: Garmin vívoactive, Forerunner, Fenix, Edge series
- **GPX**: Strava exports, Garmin Connect exports, any GPS device
- **TCX**: Garmin Connect, Strava, Zwift exports

## Source

Adapted from [fitness_tracker_data_parsing](https://github.com/bunburya/fitness_tracker_data_parsing) (MIT License).
