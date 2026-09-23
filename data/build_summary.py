"""Aggregates patients/utilization/care_gaps into the JSON the dashboard consumes."""
import json
import pandas as pd

patients = pd.read_csv("data/patients.csv")
util = pd.read_csv("data/utilization_monthly.csv")
gaps = pd.read_csv("data/care_gaps.csv")

CONDITIONS = ["Diabetes", "Hypertension", "COPD", "CHF", "CKD", "Asthma", "Obesity", "Depression"]

kpis = {
    "total_patients": int(len(patients)),
    "pct_high_risk": round(100 * (patients.risk_tier == "High").mean(), 1),
    "avg_pmpm_cost": round(util.pmpm_cost.mean(), 2),
    "readmission_rate_30d": round(100 * util.loc[util.admissions > 0, "readmission_30d"].mean(), 1),
    "ed_visits_per_1000_per_month": round(1000 * util.ed_visits.sum() / (patients.shape[0] * util.month.nunique()), 1),
    "care_gap_closure_rate": round(100 * gaps.gap_closed.mean(), 1),
}

condition_prevalence = [
    {"condition": c, "pct": round(100 * patients[f"has_{c.lower().replace(' ', '_')}"].mean(), 1)}
    for c in CONDITIONS
]
condition_prevalence.sort(key=lambda r: -r["pct"])

risk_tier_counts = patients.risk_tier.value_counts().reindex(["Low", "Medium", "High"]).to_dict()

monthly = util.groupby("month").agg(
    ed_visits=("ed_visits", "sum"),
    admissions=("admissions", "sum"),
    avg_pmpm_cost=("pmpm_cost", "mean"),
).reset_index().sort_values("month")
monthly_trend = monthly.to_dict(orient="records")

cost_by_tier = util.groupby("risk_tier")["pmpm_cost"].mean().reindex(["Low", "Medium", "High"]).round(2).to_dict()

gap_by_measure = gaps.groupby("measure").gap_closed.mean().mul(100).round(1).sort_values().to_dict()

gap_by_tier = gaps.groupby("risk_tier").gap_closed.mean().mul(100).round(1).reindex(["Low", "Medium", "High"]).to_dict()

out = {
    "kpis": kpis,
    "condition_prevalence": condition_prevalence,
    "risk_tier_counts": risk_tier_counts,
    "monthly_trend": monthly_trend,
    "cost_by_tier": cost_by_tier,
    "gap_by_measure": gap_by_measure,
    "gap_by_tier": gap_by_tier,
}

with open("dashboard/summary.json", "w") as f:
    json.dump(out, f, indent=2)

print(json.dumps(kpis, indent=2))
