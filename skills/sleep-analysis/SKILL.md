---
name: sleep-analysis
version: 1.0.0
author: tuchandra (adapted)
description: Pull and analyze Fitbit sleep data. Fetches intraday sleep stages via Fitbit API, performs statistical analysis on sleep patterns, and generates visualizations. Use when user wants to analyze their Fitbit sleep data.
tags: [health, sleep, fitbit, data-analysis]
license: MIT
---

# Sleep Analysis Skill

## Overview

Pull intraday sleep data from Fitbit API and perform statistical analysis on sleep patterns. Analyzes sleep stages (deep, light, REM, wake), sleep efficiency, consistency, and trends over time.

## When to Use

- User wants to analyze their Fitbit sleep data
- User has a Fitbit device and wants sleep pattern insights
- User asks about sleep quality, sleep stages, or sleep trends
- User wants to identify factors affecting their sleep

## Prerequisites

- Python ≥3.8
- Dependencies: `requests`, `pandas`, `matplotlib`, `scikit-learn`, `statsmodels`
- Fitbit Developer account with a "personal app" registered
- `client_secret.json` file with Fitbit API credentials
- Scripts location: `scripts/fitbit.py`
- Reference notebooks: `references/spring-sleep-analysis.ipynb`, `references/stats-and-sleep.ipynb`

## Workflow

### Step 1: Setup Fitbit API Credentials

1. Register a personal app at <https://dev.fitbit.com/apps/new>
2. Create `client_secret.json`:
```json
{
  "client_id": "<your_client_id>",
  "client_secret": "<your_client_secret>",
  "redirect_uri": "http://localhost:8080"
}
```
3. Complete OAuth flow to get access token

### Step 2: Pull Sleep Data

```python
import sys
sys.path.insert(0, 'scripts')
from fitbit import get_sleep_data

# Pull last 150 days of sleep data
sleep_data = get_sleep_data(start_date='2026-01-01')
```

The API returns intraday sleep stages:
- **deep**: Deep sleep (most restorative)
- **light**: Light sleep
- **rem**: REM sleep (dreaming, memory consolidation)
- **wake**: Awake periods during sleep

### Step 3: Statistical Analysis

Use the Jupyter notebooks as reference templates:

**Spring Sleep Analysis** (`references/spring-sleep-analysis.ipynb`):
- Sleep stage distribution over time
- Bedtime and wake time consistency
- Sleep efficiency trends (time asleep / time in bed)
- Day-of-week patterns

**Stats and Sleep** (`references/stats-and-sleep.ipynb`):
- Correlation between sleep metrics and daily activities
- Regression analysis: does bedtime affect sleep quality?
- Anomaly detection: nights with unusual sleep patterns
- Time series decomposition: trend vs seasonal patterns

### Step 4: Key Metrics

Calculate and present:

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Sleep Efficiency | (total_sleep - wake) / total_time_in_bed * 100 | >85% = good |
| Deep Sleep % | deep_sleep_minutes / total_sleep_minutes * 100 | 13-23% = normal |
| REM % | rem_minutes / total_sleep_minutes * 100 | 20-25% = normal |
| Sleep Consistency | std_dev of bedtime | Lower = better |
| Sleep Onset Latency | time from bed to first sleep | <30min = good |

### Step 5: Output

Generate:
- **Sleep summary table**: nightly metrics (duration, efficiency, stage distribution)
- **Trend charts**: sleep duration and quality over time
- **Pattern analysis**: weekday vs weekend, seasonal trends
- **Recommendations**: based on identified patterns

## Limitations

- Requires Fitbit device and API access
- API rate limit: 150 requests/hour
- Data accuracy depends on Fitbit's sleep detection algorithm
- Not a medical device; analysis is for informational purposes only

## Source

Adapted from [sleep-analysis](https://github.com/tuchandra/sleep-analysis) (MIT License).
