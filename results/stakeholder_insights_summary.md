# Population Health Panel — Insights Summary

*Panel: 6,000 patients · Period: Oct 2024 – Sep 2026 · Data: synthetic, calibrated to published population-health benchmarks (see project README)*

## Headline

The panel's highest-risk patients — 10.5% of the population — drive
average monthly cost roughly **5.5x higher** than low-risk patients
($925 vs. $167 PMPM) and close preventive-care gaps at the **lowest**
rate of any risk tier (50.5% vs. 74.1% for low-risk patients). That
combination is the case for care-management outreach: the group costing
the most is also the group least engaged with preventive care.

## What the data shows

**Chronic disease burden.** Hypertension (43.7%) and obesity (37.1%) are
the two most prevalent conditions in the panel, ahead of diabetes (25.5%)
and depression (25.0%) — a burden profile consistent with a typical mixed
commercial/Medicare population.

**Utilization is flat, not trending.** Monthly ED visits and admissions
hold steady across the full 24-month window with no sustained upward or
downward trend, and average PMPM cost stays within a narrow $350–$359
band throughout — there's no seasonal cost spike to plan around in this
panel.

**Readmissions.** 14.9% of hospital admissions result in a 30-day
readmission, in line with commonly cited benchmark ranges for mixed-payer
populations — worth tracking against a specific target once one is set,
since a synthetic panel has no external benchmark of its own to compare
against.

**Preventive care gaps are broad, not concentrated.** All seven tracked
measures sit 11–15 percentage points below an illustrative 80% closure
target — this isn't one broken program, it's a panel-wide gap. Colorectal
cancer screening and blood-pressure control are furthest behind (65.1%
each) and would be the first two measures a targeted campaign should
prioritize, both because of the gap size and because both have
well-established outreach playbooks (mailed FIT kits; home BP
cuff programs).

## Recommended next steps

1. Stand up a care-management outreach track for the high-risk tier,
   prioritized by the two furthest-behind measures (colorectal screening,
   BP control) — this tier has the most room to both improve outcomes and
   reduce avoidable cost.
2. Re-baseline the 30-day readmission rate against the organization's own
   target once this analysis runs on real claims data.
3. Because utilization and cost are flat rather than trending, treat this
   as a stable baseline period — a good window to launch an intervention
   and measure its effect against, since there's no confounding secular
   trend to control for.

*Methodology note: figures above come from the dashboard's underlying
data model (`data/patients.csv`, `data/utilization_monthly.csv`,
`data/care_gaps.csv`), aggregated per the definitions in the Power BI /
Tableau build guides in this project.*
