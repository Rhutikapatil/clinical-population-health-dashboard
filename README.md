# Clinical Population Health Dashboard

A population-health analytics project: a clean patient/utilization/care-gap
data model, an interactive dashboard preview, and precise Power BI and
Tableau build guides — for a BI/data-analytics portfolio.

**Live dashboard preview:** built and published as an interactive HTML
artifact (see the link shared alongside this project) — six charts and a
KPI row over the full dataset, with hover tooltips throughout.

## Why it's structured this way

Power BI Desktop and Tableau Desktop are Windows/Mac GUI applications —
they weren't available in the Linux build environment this project was
put together in. Rather than fake a screenshot, this project ships what
actually transfers: a proper star-schema-style data model (`data/`), a
fully interactive dashboard preview built on that exact data
(`dashboard/index.html`), and **exact, mechanical build guides**
(`build_guides/`) with every DAX measure and Tableau calculated field
already written — importing the three CSVs into either tool and following
the guide is a 15–20 minute build, not a design decision.

## Data

Synthetic population-health data (`data/generate_population.py`) —
6,000 patients, 24 months of utilization, and preventive-care-gap
records — calibrated to published chronic-disease prevalence ranges and
typical PMPM cost/risk-tier relationships. Not real patient data; see the
generator's own docstring for the full provenance note. Swap in a real
de-identified extract (Synthea, a CMS public use file) by matching the
three-table schema in `data/*.csv`.

| File | Grain | Rows |
|---|---|---|
| `patients.csv` | 1 row / patient | 6,000 |
| `utilization_monthly.csv` | 1 row / patient / month with a claim | ~84,500 |
| `care_gaps.csv` | 1 row / patient / eligible preventive measure | ~14,700 |

## Contents

```
.
├── data/
│   ├── generate_population.py   # synthetic data generator
│   ├── build_summary.py          # aggregates the 3 CSVs -> dashboard/summary.json
│   ├── patients.csv
│   ├── utilization_monthly.csv
│   └── care_gaps.csv
├── dashboard/
│   ├── index.html                 # interactive dashboard (also published as a live artifact)
│   └── summary.json
├── build_guides/
│   ├── power_bi_guide.md          # DAX measures + visual-by-visual build steps
│   └── tableau_guide.md           # calculated fields + worksheet-by-worksheet build steps
└── results/
    └── stakeholder_insights_summary.md   # one-page, non-technical findings summary
```

## Key findings (see `results/stakeholder_insights_summary.md` for the full write-up)

- The highest-risk 10.5% of the panel costs ~5.5x more per member/month
  than the lowest-risk tier, and closes preventive care gaps at the
  lowest rate of any tier — the standard argument for targeted
  care-management outreach.
- All seven tracked preventive-care measures sit 11–15 points below an
  illustrative 80% target, with colorectal cancer screening and
  blood-pressure control furthest behind.
- Utilization and cost are flat across the 24-month window — a stable
  baseline to measure any new intervention against.

## Reproducing it

```bash
python3 -m venv venv && source venv/bin/activate
pip install pandas numpy
python3 data/generate_population.py
python3 data/build_summary.py
```

Then open `dashboard/index.html` directly in a browser, or follow either
guide in `build_guides/` to load the three CSVs into Power BI or Tableau.

## Stack

Python · pandas/NumPy (data generation) · HTML/SVG/vanilla JS (dashboard
preview) · Power BI (DAX) · Tableau (calculated fields)

## Author

Rhutika Patil — M.S. Bioinformatics, NC State University
[linkedin.com/in/rhutika-patil](https://linkedin.com/in/rhutika-patil) ·
[github.com/Rhutikapatil](https://github.com/Rhutikapatil)
