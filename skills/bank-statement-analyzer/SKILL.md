---
name: bank-statement-analyzer
version: 1.0.0
author: sahusaksham726 (adapted)
description: Analyze bank statement data to extract spending patterns, income vs expense trends, category breakdowns, anomaly detection, and credit score estimation. Generates visualizations and summary reports.
tags: [health, finance, banking, statement, spending-analysis]
license: MIT
---

# Bank Statement Analyzer Skill

## Overview

Analyze bank statement data to extract spending patterns, income vs expense trends, category breakdowns, anomaly detection, and credit score estimation. Generates comprehensive visualizations and summary reports for personal financial health assessment.

## When to Use

- User provides a bank statement CSV file
- User wants to analyze their spending patterns
- User asks about income vs expense trends
- User wants to detect unusual transactions
- User asks for a financial health overview

## Prerequisites

- Python ≥3.8
- Dependencies: `pandas`, `matplotlib`, `seaborn`, `numpy`
- Install: `pip install pandas matplotlib seaborn numpy`
- Scripts location: `references/Bank_Statement_Analyzer.ipynb` (reference notebook)
- Sample data: `scripts/sample_data.csv`

## Workflow

### Step 1: Load Bank Statement

```python
import pandas as pd

# Load the bank statement CSV
df = pd.read_csv('path/to/bank_statement.csv')

# Expected columns (flexible):
# - date / transaction_date / posting_date
# - description / details / narration
# - amount / debit / credit
# - balance / running_balance
# - category / type (optional)
```

If columns differ from expected, map them:
```python
column_map = {
    'Transaction Date': 'date',
    'Description': 'description',
    'Debit Amount': 'debit',
    'Credit Amount': 'credit',
}
df = df.rename(columns=column_map)
```

### Step 2: Data Cleaning

- Parse dates to datetime
- Separate debits (expenses) and credits (income)
- Calculate net cash flow per transaction
- Handle missing values
- Remove duplicates

### Step 3: Analysis

The reference notebook performs the following analyses:

**Monthly Income vs Expense** (`fig1`):
- Group by month, sum credits and debits
- Calculate net savings rate
- Identify months with deficit

**Net Cash Flow per Month** (`fig2`):
- Monthly net = income - expenses
- 3-month rolling average trend
- Identify improving/declining financial health

**Expense Category Breakdown** (`fig3`):
- Categorize transactions (if not pre-categorized, use keyword matching)
- Top 10 expense categories
- Category share as percentage of total spending

**Month-end Balance Trend** (`fig4`):
- Balance at end of each month
- Identify balance depletion patterns
- Calculate average monthly balance

**Correlation Heatmaps** (`fig5`):
- Correlation between income, expenses, balance, transaction count
- Identify which metrics move together

**Anomaly Detection** (`fig6`):
- Z-score based outlier detection on transaction amounts
- Flag transactions >3 standard deviations from mean
- Highlight potentially fraudulent or unusual transactions

**Credit Score Estimation** (`fig7`):
- Estimate financial health score (0-850 scale, similar to FICO)
- Based on: payment consistency, debt-to-income ratio, balance stability, savings rate
- Track score over time

### Step 4: Output

Generate visualizations saved as PNG files:
- `fig1_monthly_income_vs_expense.png`
- `fig2_Net_Cash_Flow_per_Month.png`
- `fig3_Expense_Category_BreakDown.png`
- `fig4_Month-end_Balance_Trend.png`
- `fig5_heatmaps.png`
- `fig6_anomaly.png`
- `fig7_credit_score.png`

### Step 5: Present Results

Provide a comprehensive financial health report:
- **Income/Expense Summary**: monthly averages, trends
- **Spending Analysis**: top categories, unusual patterns
- **Financial Health Score**: estimated score with breakdown
- **Anomalies**: flagged transactions for review
- **Recommendations**: actionable advice based on patterns

## Customization

The analysis can be adapted for different bank statement formats by adjusting the column mapping. The reference notebook uses a sample dataset that can be replaced with the user's actual bank statement.

## Source

Adapted from [Bank-Statement-Analyzer](https://github.com/sahusaksham726-crypto/Bank-Statement-Analyzer) (MIT License).
