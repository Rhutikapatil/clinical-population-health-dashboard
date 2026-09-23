# Tableau build guide

Same rationale as the Power BI guide: Tableau Desktop wasn't available in
the build environment, so this is a precise recipe to recreate the
dashboard from the same three CSVs, including every calculated field.

## 1. Connect data

Connect → Text File → add `patients.csv`, `utilization_monthly.csv`,
`care_gaps.csv`. Relate (not join) all three on `patient_id` — Tableau's
relationship model handles the different grains (1 row/patient vs.
1 row/patient-month vs. 1 row/patient-measure) correctly without
duplicating rows.

## 2. Calculated fields

```
% High Risk
{ FIXED : COUNTD(IF [Risk Tier] = "High" THEN [Patient Id] END) } / COUNTD([Patient Id])

30-Day Readmission Rate
SUM(IF [Admissions] > 0 AND [Readmission 30d] THEN 1 ELSE 0 END)
/ SUM(IF [Admissions] > 0 THEN 1 ELSE 0 END)

ED Visits per 1000 per Month
(SUM([Ed Visits]) * 1000) / ({ COUNTD([Patient Id]) } * COUNTD([Month]))

Care Gap Closure Rate
SUM(IF [Gap Closed] THEN 1 ELSE 0 END) / COUNT([Gap Closed])

Risk Tier Sort Key
CASE [Risk Tier]
  WHEN "Low" THEN 1
  WHEN "Medium" THEN 2
  WHEN "High" THEN 3
END
```

For chronic condition prevalence, pivot the 8 `has_<condition>` columns
first: select them in the data pane → right-click → **Pivot** → rename the
resulting fields to `Condition` and `Has Condition`, then:

```
Condition Prevalence %
{ FIXED [Condition] : COUNTD(IF [Has Condition] = "True" THEN [Patient Id] END) }
/ { FIXED : COUNTD([Patient Id]) }
```

## 3. Worksheets

| Sheet | Chart | Build |
|---|---|---|
| Condition Prevalence | Horizontal bar | Rows: `Condition`, Columns: `Condition Prevalence %`, sort descending |
| Risk Tier Distribution | Vertical bar | Columns: `Risk Tier` (sorted by `Risk Tier Sort Key`), Rows: `CNTD(Patient Id)`, Color: `Risk Tier` (custom palette: Low=green, Medium=amber, High=red) |
| Cost by Risk Tier | Vertical bar | Columns: `Risk Tier` (same sort/color), Rows: `AVG(Pmpm Cost)` |
| Utilization Trend | Dual-line | Columns: `Month` (continuous), Rows: `SUM(Ed Visits)` and `SUM(Admissions)` as two measures on **Rows**, synchronized — not a dual-axis with two different scales, since both are counts |
| Cost Trend | Line | Columns: `Month`, Rows: `AVG(Pmpm Cost)` |
| Care Gap Closure | Horizontal bar | Rows: `Measure`, Columns: `Care Gap Closure Rate`, sort ascending; add a reference line at 0.80 ("Target") via Analytics pane → Reference Line |

## 4. Dashboard assembly

New Dashboard → 1180×900 fixed size → place the 6 sheets in the same
layout as the HTML preview (KPI text tiles across the top using **Text**
objects bound to the calculated fields above via a single-row worksheet,
then a 2-column grid of the six chart sheets). Add dashboard actions:
a filter action from the Risk Tier Distribution sheet to every other
sheet, so clicking a risk tier filters the whole dashboard.

## 5. Formatting

Match Power BI guide §6 — consistent number formats, and reserve
red/amber/green strictly for risk-tier and target-gap encodings, never as
a general accent color.
