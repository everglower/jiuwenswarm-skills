---
name: apple-health-analyst
version: 1.0.0
author: RuochenLyu (adapted)
description: Analyze Apple Health export data locally. Generates health reports and training reports with cross-metric reasoning, long-term trends, and offline HTML output. Use when user provides an Apple Health export ZIP file.
tags: [health, apple, fitness, sleep, recovery, training]
license: MIT
---

# Apple Health Analyst Skill

## Overview

Analyze Apple Health export data locally, generating either a health report or a training report with cross-metric reasoning, long-term trends, and offline HTML output.

Not a data dashboard — this skill interprets data like a health advisor: How are sleep and recovery linked? How does schedule regularity affect HRV? Does training load match recovery capacity?

## When to Use

- User provides an Apple Health export (`Export.zip`)
- User asks to analyze sleep, recovery, activity, or training patterns
- User wants cross-metric correlation analysis (sleep-HRV coupling, training-recovery balance)
- User asks for a training readiness assessment

## Prerequisites

- Node.js ≥18.x installed
- The skill scripts are in TypeScript; run via `npx tsx` or compile first
- Scripts location: `scripts/src/` (analyzers, render, pipeline)
- Config: `scripts/package.json` and `scripts/tsconfig.json`

## Workflow

### Step 1: Obtain Apple Health Export

User exports from iPhone:
1. Open **Health** app → profile picture → **Export All Health Data**
2. Save the resulting `Export.zip` to their computer
3. Provide the path to the ZIP file

### Step 2: Run Analysis

```bash
cd scripts
npx tsx src/cli.ts <path-to-export.zip> --output ../output/
```

The CLI auto-detects:
- Main XML file (root element `HealthData`)
- Language (Chinese/English based on user language)
- Report type (health report, training report, or both)

### Step 3: Review Output

Output is an offline HTML file with inline CSS + SVG charts:
- `output/report.html` — Health report (sleep, recovery, activity scores)
- `output/training.report.html` — Training report (ATL/CTL/TSB, sport-specific trends)

### Step 4: Interpret Results

The report includes:
- **Cross-metric correlation analysis** — Sleep-HRV coupling, training-recovery balance, schedule regularity
- **Composite scoring** — Sleep/Recovery/Activity on a 0-100 scale
- **Behavioral pattern detection** — Weekend warrior, night owl drift, sleep compensation
- **Workout-type trend analysis** — Break out trends for specific workouts
- **Dedicated training report** — ATL/CTL/TSB over 12 months

## Analyzers

Located in `scripts/src/analyzers/`:

| Analyzer | Function |
|----------|----------|
| `activity.ts` | Step counts, distance, flights climbed |
| `sleep.ts` / `sleepShared.ts` | Sleep stages, duration, efficiency, consistency |
| `recovery.ts` | HRV, resting heart rate, respiratory rate |
| `bodyComposition.ts` | Weight, body fat percentage, BMI |
| `crossMetric.ts` | Sleep-HRV coupling, schedule regularity, training-recovery balance |
| `training.ts` / `trainingLoad.ts` | ATL/CTL/TSB, training readiness, sport-specific analysis |
| `menstrualCycle.ts` | Cycle tracking, phase correlations |
| `overview.ts` | Composite 0-100 scores across all dimensions |

## Privacy

- Runs entirely locally, no external APIs, no data uploads
- Output HTML contains only aggregated metrics, no raw data export

## Source

Adapted from [apple-health-analyst](https://github.com/RuochenLyu/apple-health-analyst) (MIT License).
