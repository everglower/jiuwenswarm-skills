---
name: insurance-claims-analyzer
version: 1.0.0
author: kelynst (adapted)
description: Clean, summarize, and visualize health insurance claims data. Handles CSV/Excel input with flexible column mapping, produces summary statistics, and generates charts for claims analysis.
tags: [health, insurance, claims, data-analysis]
license: MIT
---

# Insurance Claims Analyzer Skill

## Overview

Clean, summarize, and visualize health insurance claims data. Handles messy real-world claims exports with flexible column mapping, produces comprehensive summary statistics (overall and grouped), and generates charts for claims analysis.

## When to Use

- User provides a CSV or Excel file of insurance claims data
- User wants to analyze claims patterns, status distribution, or amount trends
- User needs to clean messy claims data before analysis
- User asks for claims summary statistics or visualizations

## Prerequisites

- Python ≥3.8
- Dependencies: `pandas`, `matplotlib`, `openpyxl` (for Excel)
- Install: `pip install pandas matplotlib openpyxl`
- Scripts location: `scripts/analyze_claims.py`
- Sample data: `scripts/sample_data.csv`

## Workflow

### Step 1: Load Data

```bash
python scripts/analyze_claims.py <input_file.csv>
```

The script auto-detects columns using flexible name candidates:

| Data Field | Recognized Column Names |
|------------|------------------------|
| Claim ID | claim_id, id, claim_number |
| Patient ID | patient_id, customer_id, client_id |
| Provider | provider, provider_name, hospital |
| Payer | payer, insurer, insurance, company |
| Amount | amount, billed_amount, claim_amount, total_claim_amount, charges |
| Status | status, claim_status, outcome, decision |
| Service Date | dos, date_of_service, service_date, claim_date |
| Submission Date | submission_date, received_date |

### Step 2: Data Cleaning

The script automatically:
- Removes blank-only rows and columns
- Strips leading/trailing whitespace
- Removes duplicated rows
- Normalizes date columns to ISO format (YYYY-MM-DD)
- Coerces amount columns to numeric
- Standardizes status values (case-insensitive matching)

### Step 3: Summary Statistics

Generates two types of summaries:

**Overall Summary** (`outputs/summary_overall.csv`):
- Total claims count
- Total claim amount
- Average claim amount
- Median claim amount
- Claims by status (count + amount)
- Date range

**Grouped Summaries** (`outputs/summary_by_*.csv`):
- By provider: claim count, total amount, avg amount, status distribution
- By payer: claim count, total amount, avg amount
- By status: count, total amount, avg amount
- By month: claim count, total amount, avg amount (time trend)

### Step 4: Visualizations

Generates charts in `outputs/`:

| Chart | Description |
|-------|-------------|
| `claims_by_status.png` | Bar chart: claim count and total amount by status |
| `claims_by_provider.png` | Horizontal bar: top 10 providers by claim count |
| `claims_timeline.png` | Line chart: monthly claim count and amount |
| `amount_distribution.png` | Histogram: distribution of claim amounts |
| `status_pie.png` | Pie chart: claim status distribution |

### Step 5: Analysis Output

Present findings as:
- **Data quality report**: rows dropped, columns normalized, missing values
- **Claims summary**: key metrics (total, average, median, by status)
- **Top providers**: highest claim volume and amounts
- **Time trends**: monthly patterns, seasonality
- **Anomalies**: unusually large claims, duplicate claim IDs

## Input Format

Accepts CSV or Excel (`.xlsx`) files. The script is designed to be flexible with column names commonly seen in Kaggle datasets and real insurance exports.

## Source

Adapted from [insclaim_analyzer](https://github.com/kelynst/insclaim_analyzer) (MIT License).
