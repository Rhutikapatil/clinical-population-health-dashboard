# Power BI build guide

This dashboard was designed and validated as an HTML/data-model preview
(`dashboard/index.html`, and the live version published as a Claude
artifact) because the build environment for this project didn't have
Power BI Desktop installed. Everything below is a precise, mechanical
recipe to recreate it in Power BI — the data model, every measure, and
every visual are specified so there's no design decision left to make,
just building it.

## 1. Load the data

Get Data → Text/CSV → import all three files:
- `data/patients.csv` — one row per patient (6,000 rows)
- `data/utilization_monthly.csv` — one row per patient per month with a claim (≈84,500 rows)
- `data/care_gaps.csv` — one row per patient per eligible preventive-care measure (≈14,700 rows)

## 2. Model relationships

Model view → create:
- `Patients[patient_id]` (1) → `Utilization[patient_id]` (many)
- `Patients[patient_id]` (1) → `CareGaps[patient_id]` (many)

Both single-direction, from Patients.

## 3. Measures (DAX)

Create these in a new measure table called `_Measures`:

```DAX
Total Patients = DISTINCTCOUNT(Patients[patient_id])

Pct High Risk =
DIVIDE(
    CALCULATE(DISTINCTCOUNT(Patients[patient_id]), Patients[risk_tier] = "High"),
    [Total Patients]
)

Avg PMPM Cost = AVERAGE(Utilization[pmpm_cost])

30-Day Readmission Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Utilization), Utilization[readmission_30d] = TRUE, Utilization[admissions] > 0),
    CALCULATE(COUNTROWS(Utilization), Utilization[admissions] > 0)
)

ED Visits per 1000 per Month =
DIVIDE(
    SUM(Utilization[ed_visits]) * 1000,
    [Total Patients] * DISTINCTCOUNT(Utilization[month])
)

Care Gap Closure Rate =
DIVIDE(
    CALCULATE(COUNTROWS(CareGaps), CareGaps[gap_closed] = TRUE),
    COUNTROWS(CareGaps)
)

Total ED Visits = SUM(Utilization[ed_visits])
Total Admissions = SUM(Utilization[admissions])
```

## 4. Visuals — page 1 "Panel Overview"

| Visual | Type | Fields |
|---|---|---|
| KPI row | 6x Card visual | `[Total Patients]`, `[Pct High Risk]`, `[Avg PMPM Cost]`, `[30-Day Readmission Rate]`, `[ED Visits per 1000 per Month]`, `[Care Gap Closure Rate]` |
| Chronic condition prevalence | Clustered bar chart | Axis: unpivot the 8 `has_<condition>` columns first (Transform Data → Select the 8 columns → Unpivot Columns → rename to `condition`/`has_condition`); Axis = `condition`, Values = `% of Patients` measure (`DIVIDE(CALCULATE(DISTINCTCOUNT(patient_id), has_condition=TRUE), [Total Patients])`) |
| Risk tier distribution | Clustered column chart | Axis: `Patients[risk_tier]` (sort by a custom Low→Medium→High order column), Values: `[Total Patients]`. Conditional formatting: Low=green, Medium=amber, High=red |
| Avg cost by risk tier | Clustered column chart | Axis: `Patients[risk_tier]` (same sort), Values: `[Avg PMPM Cost]` |
| Monthly ED visits & admissions | Line chart | Axis: `Utilization[month]`, Values: `[Total ED Visits]` and `[Total Admissions]` as two lines |
| Avg PMPM cost trend | Line chart | Axis: `Utilization[month]`, Values: `[Avg PMPM Cost]` |
| Care gap closure by measure | Bar chart | Axis: `CareGaps[measure]`, Values: `[Care Gap Closure Rate]`, sorted ascending. Add a constant line analytics element at 80% ("target") |

## 5. Slicers

Add a slicer panel: `risk_tier`, `region`, `payer`, and a date slicer on `month` — every visual above should respond to all four.

## 6. Formatting

- Card visuals: use the risk-tier red/amber/green only where the KPI is a risk indicator (readmission rate, high-risk share, care gap shortfall vs. target); leave neutral KPIs in the report's default accent color.
- Apply a consistent number format: `#,0` for counts, `$#,0` for cost, `0.0%` for rates.
