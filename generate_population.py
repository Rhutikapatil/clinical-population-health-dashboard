"""
Synthetic clinical population health dataset generator.

IMPORTANT — data provenance: this is SIMULATED data, not real patient
records. It was generated because the build environment for this project
had no network route to CMS/data.gov or a Synthea data mirror (only package
registries and GitHub were reachable). The generator produces a realistic
population health schema — patients, monthly utilization, and preventive
care gaps — with prevalence and cost patterns calibrated to published,
publicly available population-health statistics (CDC chronic disease
prevalence ranges, CMS readmission benchmarks), so the resulting dashboard
demonstrates real population-health analytics patterns without exposing
any real patient information anywhere. Swap in a real de-identified
extract (Synthea, a CMS public use file) by matching this schema.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(7)

N_PATIENTS = 6000
CONDITIONS = ["Diabetes", "Hypertension", "COPD", "CHF", "CKD", "Asthma", "Obesity", "Depression"]
CONDITION_PREVALENCE = [0.14, 0.32, 0.07, 0.04, 0.06, 0.10, 0.24, 0.13]  # roughly CDC-range prevalence
RISK_TIERS = ["Low", "Medium", "High"]
PAYERS = ["Commercial", "Medicare", "Medicaid", "Uninsured/Self-pay"]
REGIONS = ["North", "South", "East", "West", "Central"]
CARE_GAP_MEASURES = [
    "HbA1c screening (diabetics)", "Annual eye exam (diabetics)", "Mammography (50-74F)",
    "Colorectal cancer screening (45-75)", "Blood pressure control (hypertensive)",
    "Statin therapy (high CV risk)", "Annual wellness visit",
]

# ---- Patients ----
age = np.clip(rng.normal(52, 18, N_PATIENTS), 1, 95).astype(int)
sex = rng.choice(["Female", "Male"], N_PATIENTS, p=[0.52, 0.48])
region = rng.choice(REGIONS, N_PATIENTS)
payer = rng.choice(PAYERS, N_PATIENTS, p=[0.46, 0.28, 0.20, 0.06])

conditions_matrix = np.zeros((N_PATIENTS, len(CONDITIONS)), dtype=bool)
for j, p in enumerate(CONDITION_PREVALENCE):
    age_boost = np.clip((age - 40) / 100, 0, 0.25)  # older -> somewhat higher prevalence
    conditions_matrix[:, j] = rng.random(N_PATIENTS) < np.clip(p + age_boost, 0, 0.85)

n_conditions = conditions_matrix.sum(axis=1)
risk_score = np.clip(
    10 + n_conditions * 12 + (age - 50) * 0.4 + rng.normal(0, 8, N_PATIENTS), 0, 100
)
risk_tier = pd.cut(risk_score, bins=[-1, 33, 66, 101], labels=RISK_TIERS)

patients = pd.DataFrame({
    "patient_id": [f"P{100000+i}" for i in range(N_PATIENTS)],
    "age": age,
    "sex": sex,
    "region": region,
    "payer": payer,
    "risk_score": risk_score.round(1),
    "risk_tier": risk_tier.astype(str),
    "n_chronic_conditions": n_conditions,
})
for j, c in enumerate(CONDITIONS):
    patients[f"has_{c.lower().replace(' ', '_')}"] = conditions_matrix[:, j]

# ---- Monthly utilization (24 months) ----
months = pd.period_range("2024-10", periods=24, freq="M").astype(str)
util_rows = []
base_risk_multiplier = {"Low": 0.4, "Medium": 1.0, "High": 2.6}
for pid, tier, ncond in zip(patients.patient_id, patients.risk_tier, patients.n_chronic_conditions):
    mult = base_risk_multiplier[tier]
    for m in months:
        ed_visits = rng.poisson(0.08 * mult)
        admissions = rng.poisson(0.02 * mult)
        readmit_30d = admissions > 0 and rng.random() < (0.12 + 0.05 * (tier == "High"))
        pmpm_cost = max(0, rng.normal(250 * mult + 60 * ncond, 120))
        if ed_visits or admissions or rng.random() < 0.55:  # not every patient has a claim every month
            util_rows.append({
                "patient_id": pid, "month": m, "risk_tier": tier,
                "ed_visits": ed_visits, "admissions": admissions,
                "readmission_30d": bool(readmit_30d and admissions > 0),
                "pmpm_cost": round(pmpm_cost, 2),
            })
utilization = pd.DataFrame(util_rows)

# ---- Care gaps ----
gap_rows = []
for pid, tier in zip(patients.patient_id, patients.risk_tier):
    for measure in CARE_GAP_MEASURES:
        eligible = rng.random() < 0.35  # not every patient is eligible for every measure
        if not eligible:
            continue
        closure_p = {"Low": 0.74, "Medium": 0.63, "High": 0.52}[tier]  # higher-risk patients have more gap
        closed = rng.random() < closure_p
        gap_rows.append({"patient_id": pid, "measure": measure, "risk_tier": tier, "gap_closed": closed})
care_gaps = pd.DataFrame(gap_rows)

patients.to_csv("data/patients.csv", index=False)
utilization.to_csv("data/utilization_monthly.csv", index=False)
care_gaps.to_csv("data/care_gaps.csv", index=False)

print(f"patients: {patients.shape}")
print(f"utilization_monthly: {utilization.shape}")
print(f"care_gaps: {care_gaps.shape}")
print(patients.risk_tier.value_counts())
