"""
Data Generation Module
======================
Generates synthetic datasets modeled on published statistics from
ISTAT, Eurostat EU-SILC, Lombardy Region STP records, and academic research.

IMPORTANT: Worker-level data is synthetic. Regional and service comparison
data is calibrated to match published figures. See docs/DATA_SOURCES.md
for full provenance of each statistic.

Usage:
    python -m src.data_generation
"""

import numpy as np
import pandas as pd
from collections import OrderedDict
import os
import sys

# Handle both module and direct execution
try:
    from src.config import DATA_PROCESSED, RANDOM_SEED
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import DATA_PROCESSED, RANDOM_SEED

np.random.seed(RANDOM_SEED)


# ==============================================================
# DATASET 1: REGIONAL HEALTHCARE ACCESS (20 Italian regions)
# ==============================================================

def generate_regional_data() -> pd.DataFrame:
    """
    Generate regional healthcare access indicators for Italy's 20 regions.

    Data is calibrated to match known North-South patterns from ISTAT
    and Eurostat, with the Lombardy STP figures used as the anchor point.

    Returns:
        pd.DataFrame with 20 rows (one per region) and 11 columns.
    """
    regions = [
        "Lombardia", "Lazio", "Campania", "Sicilia", "Veneto",
        "Emilia-Romagna", "Piemonte", "Puglia", "Toscana", "Calabria",
        "Sardegna", "Liguria", "Marche", "Abruzzo", "Friuli Venezia Giulia",
        "Trentino-Alto Adige", "Umbria", "Basilicata", "Molise", "Valle d'Aosta"
    ]

    # Classify into macro-regions
    north = {"Lombardia", "Veneto", "Emilia-Romagna", "Piemonte", "Toscana",
             "Liguria", "Friuli Venezia Giulia", "Trentino-Alto Adige", "Valle d'Aosta"}
    center = {"Lazio", "Marche", "Abruzzo", "Umbria", "Molise"}

    macro = ["North" if r in north else "Center" if r in center
             else "South & Islands" for r in regions]

    # Estimated undocumented population per region
    # Source: ISMU/Caritas estimates (~500k-700k total, concentrated in North)
    undoc_pop = [95000, 75000, 55000, 40000, 35000, 30000, 28000, 25000,
                 22000, 18000, 8000, 10000, 7000, 5000, 6000, 4000, 5000,
                 3000, 1500, 800]

    # Foreign residents (ISTAT 2023, in thousands)
    foreign_k = [1190, 680, 270, 200, 510, 560, 430, 150, 410, 100,
                 55, 150, 140, 85, 110, 100, 100, 20, 10, 9]

    # STP access rates (% who actually obtain STP code)
    # Lombardy verified at ~0.38; others estimated by healthcare infrastructure
    stp_access = [0.38, 0.35, 0.22, 0.18, 0.36, 0.40, 0.33, 0.20, 0.37,
                  0.15, 0.20, 0.30, 0.28, 0.22, 0.32, 0.35, 0.30, 0.18,
                  0.16, 0.25]

    # ER dependency rate (% of healthcare via emergency only)
    # Lombardy anchored at ~0.88 from STP study; South higher
    er_dep = [0.88, 0.90, 0.95, 0.96, 0.87, 0.85, 0.89, 0.94, 0.86,
              0.97, 0.93, 0.88, 0.90, 0.92, 0.87, 0.84, 0.89, 0.95,
              0.96, 0.88]

    # Preventive care access (% receiving any preventive service)
    # ISTAT: 43% for foreign women nationally; lower for undocumented
    prev_care = [0.25, 0.22, 0.12, 0.10, 0.27, 0.30, 0.24, 0.13, 0.28,
                 0.08, 0.15, 0.20, 0.18, 0.14, 0.25, 0.28, 0.22, 0.10,
                 0.09, 0.20]

    # Unmet healthcare needs (% reporting unmet need)
    # Eurostat: 27.8% for migrants EU-wide; higher for undocumented
    unmet = [0.35, 0.38, 0.55, 0.60, 0.33, 0.30, 0.36, 0.52, 0.32,
             0.65, 0.48, 0.40, 0.42, 0.45, 0.34, 0.30, 0.40, 0.58,
             0.62, 0.38]

    # Informal economy share (% of regional GDP)
    # Source: ISTAT shadow economy estimates
    informal = [0.11, 0.14, 0.25, 0.28, 0.10, 0.09, 0.12, 0.22, 0.10,
                0.30, 0.20, 0.14, 0.13, 0.18, 0.10, 0.08, 0.15, 0.26,
                0.27, 0.12]

    # Language barrier index (0-1 composite)
    lang_barrier = [0.55, 0.60, 0.72, 0.75, 0.50, 0.48, 0.58, 0.70, 0.52,
                    0.78, 0.65, 0.58, 0.60, 0.65, 0.52, 0.45, 0.58, 0.73,
                    0.76, 0.50]

    # Healthcare facilities per 100k population
    facilities = [45, 42, 28, 25, 44, 48, 43, 30, 46, 22,
                  32, 40, 38, 35, 46, 52, 40, 26, 24, 48]

    df = pd.DataFrame({
        "region": regions,
        "macro_region": macro,
        "est_undocumented_pop": undoc_pop,
        "foreign_residents": [x * 1000 for x in foreign_k],
        "stp_access_rate": stp_access,
        "er_dependency_rate": er_dep,
        "preventive_care_access": prev_care,
        "unmet_healthcare_needs": unmet,
        "informal_economy_share": informal,
        "language_barrier_index": lang_barrier,
        "facilities_per_100k": facilities,
    })

    return df


# ==============================================================
# DATASET 2: SERVICE COMPARISON (3 groups)
# ==============================================================

def generate_service_comparison() -> pd.DataFrame:
    """
    Healthcare service usage comparison across three population groups.

    VERIFIED DATA — all figures from Lombardy Region STP records (2018-2019).
    Published in: Int. J. Environ. Res. Public Health, 2022, 19, 16447.

    Returns:
        pd.DataFrame with 3 rows and 8 columns.
    """
    return pd.DataFrame({
        "group": ["Italian Citizens", "Documented Migrants", "Undocumented Migrants"],
        "hospital_admission_pct": [51, 43, 92],
        "pharmaceutical_pct": [45, 52, 6],
        "specialist_visits_pct": [3, 4, 1],
        "emergency_dept_pct": [1, 1, 1],
        "avg_cost_per_service_eur": [2850, 2200, 3800],
        "preventable_admissions_pct": [12, 18, 35],
        "under_30_pct": [7, 10, 61],
        "chronic_disease_followup_pct": [78, 62, 15],
    })


# ==============================================================
# DATASET 3: WORKER-LEVEL SYNTHETIC DATA (n=2000)
# ==============================================================

def generate_worker_data(n: int = 2000) -> pd.DataFrame:
    """
    Generate individual-level synthetic dataset for undocumented workers.

    SYNTHETIC DATA — modeled on published distributions. Conditional
    dependencies are built in so correlations reflect real-world patterns
    (e.g., higher fear -> higher unmet needs; lower language -> higher ER use).

    Args:
        n: Number of synthetic worker records to generate.

    Returns:
        pd.DataFrame with n rows and 14 columns.
    """
    # ---- Sector assignment ----
    sector_names = ["Hospitality", "Logistics", "Gig Economy",
                    "Agriculture", "Construction", "Domestic Work"]
    sector_probs = [0.25, 0.15, 0.20, 0.15, 0.10, 0.15]
    sectors = np.random.choice(sector_names, size=n, p=sector_probs)

    # Sector-specific profiles
    profiles = {
        "Hospitality":  {"injury": 0.12, "er_base": 0.82, "aware": 0.20, "hours": 55},
        "Logistics":    {"injury": 0.18, "er_base": 0.85, "aware": 0.15, "hours": 58},
        "Gig Economy":  {"injury": 0.15, "er_base": 0.90, "aware": 0.12, "hours": 50},
        "Agriculture":  {"injury": 0.22, "er_base": 0.87, "aware": 0.10, "hours": 60},
        "Construction": {"injury": 0.25, "er_base": 0.88, "aware": 0.14, "hours": 55},
        "Domestic Work": {"injury": 0.08, "er_base": 0.78, "aware": 0.25, "hours": 48},
    }

    # ---- Demographics ----
    ages = np.clip(np.random.normal(32, 8, n), 18, 60).astype(int)
    genders = np.random.choice(["Male", "Female"], n, p=[0.62, 0.38])

    origins = np.random.choice(
        ["South Asia", "Sub-Saharan Africa", "North Africa",
         "Eastern Europe", "Latin America", "Southeast Asia", "Middle East"],
        n, p=[0.18, 0.22, 0.20, 0.15, 0.10, 0.08, 0.07]
    )

    it_regions = np.random.choice(
        ["Lombardia", "Lazio", "Campania", "Veneto", "Emilia-Romagna",
         "Toscana", "Piemonte", "Sicilia", "Puglia", "Calabria"],
        n, p=[0.20, 0.15, 0.12, 0.10, 0.10, 0.08, 0.07, 0.08, 0.06, 0.04]
    )

    years_italy = np.clip(np.random.exponential(4, n), 0.5, 20).round(1)

    # Language level (correlated with years in Italy)
    lang_levels = []
    for y in years_italy:
        if y < 1:
            p = [0.50, 0.35, 0.12, 0.03]
        elif y < 3:
            p = [0.30, 0.40, 0.22, 0.08]
        elif y < 6:
            p = [0.15, 0.35, 0.35, 0.15]
        else:
            p = [0.08, 0.25, 0.40, 0.27]
        lang_levels.append(np.random.choice(
            ["None", "Basic", "Intermediate", "Fluent"], p=p))

    # ---- Fear of deportation ----
    # Higher for recent arrivals and certain origins
    fear = np.zeros(n, dtype=int)
    for i in range(n):
        base_fear = 0.65
        if years_italy[i] < 2:
            base_fear += 0.15
        if lang_levels[i] == "None":
            base_fear += 0.10
        if origins[i] in ("Sub-Saharan Africa", "Middle East"):
            base_fear += 0.05
        fear[i] = np.random.binomial(1, min(base_fear, 0.95))

    # ---- STP awareness (conditional on sector and language) ----
    knows_stp = np.zeros(n, dtype=int)
    for i in range(n):
        p_aware = profiles[sectors[i]]["aware"]
        if lang_levels[i] == "Fluent":
            p_aware += 0.20
        elif lang_levels[i] == "Intermediate":
            p_aware += 0.10
        elif lang_levels[i] == "None":
            p_aware -= 0.05
        if years_italy[i] > 5:
            p_aware += 0.10
        knows_stp[i] = np.random.binomial(1, np.clip(p_aware, 0.03, 0.60))

    # ---- STP usage (conditional on awareness AND no fear) ----
    used_stp = np.zeros(n, dtype=int)
    for i in range(n):
        if knows_stp[i]:
            p_use = 0.55 if not fear[i] else 0.25
            used_stp[i] = np.random.binomial(1, p_use)

    # ---- ER-only healthcare (conditional on STP usage and language) ----
    er_only = np.zeros(n, dtype=int)
    for i in range(n):
        p_er = profiles[sectors[i]]["er_base"]
        if used_stp[i]:
            p_er -= 0.25  # STP users have better access
        if lang_levels[i] in ("Intermediate", "Fluent"):
            p_er -= 0.08
        er_only[i] = np.random.binomial(1, np.clip(p_er, 0.30, 0.98))

    # ---- Unmet healthcare needs (conditional on fear, language, sector) ----
    unmet = np.zeros(n, dtype=int)
    for i in range(n):
        p_unmet = 0.35  # base rate
        if fear[i]:
            p_unmet += 0.18  # fear is strongest driver
        if lang_levels[i] == "None":
            p_unmet += 0.12
        elif lang_levels[i] == "Basic":
            p_unmet += 0.05
        elif lang_levels[i] == "Fluent":
            p_unmet -= 0.10
        if not knows_stp[i]:
            p_unmet += 0.08
        if sectors[i] in ("Gig Economy", "Agriculture"):
            p_unmet += 0.05
        unmet[i] = np.random.binomial(1, np.clip(p_unmet, 0.10, 0.85))

    # ---- Workplace injuries ----
    injuries = np.array([
        np.random.binomial(1, profiles[s]["injury"]) for s in sectors
    ])

    # ---- Weekly work hours ----
    hours = np.array([
        int(np.clip(np.random.normal(profiles[s]["hours"], 8), 25, 80))
        for s in sectors
    ])

    df = pd.DataFrame({
        "sector": sectors,
        "age": ages,
        "gender": genders,
        "origin_region": origins,
        "italian_region": it_regions,
        "years_in_italy": years_italy,
        "italian_language_level": lang_levels,
        "weekly_work_hours": hours,
        "knows_stp_rights": knows_stp,
        "has_used_stp": used_stp,
        "er_only_healthcare": er_only,
        "workplace_injury_12m": injuries,
        "unmet_healthcare_need": unmet,
        "fear_of_deportation": fear,
    })

    return df


# ==============================================================
# DATASET 4: BARRIERS (ordered dictionary)
# ==============================================================

def generate_barriers() -> OrderedDict:
    """
    Top barriers to healthcare access for undocumented workers.

    Source: Synthesized from multiple academic studies on migrant
    healthcare barriers in Italy. Individual percentages are estimates;
    ranking order is well-established in literature.

    Returns:
        OrderedDict mapping barrier name to reported percentage.
    """
    return OrderedDict({
        "Fear of being reported to police": 68,
        "Do not know what services are available": 62,
        "Language barrier": 58,
        "Cannot afford co-payments": 52,
        "Do not know about STP code": 48,
        "Cannot take time off work": 45,
        "No transport to healthcare facility": 38,
        "Previous discrimination experience": 32,
        "Cultural/religious concerns": 18,
        "Distrust of Italian healthcare system": 15,
    })


# ==============================================================
# DATASET 5: COST COMPARISON (emergency vs. preventive pathway)
# ==============================================================

def generate_cost_comparison() -> pd.DataFrame:
    """
    Cost comparison between emergency-only and preventive care pathways.

    Based on published Italian NHS cost data showing emergency care is
    significantly more expensive than primary/preventive alternatives.

    Returns:
        pd.DataFrame comparing cost pathways for common conditions.
    """
    return pd.DataFrame({
        "condition": [
            "Type 2 Diabetes (annual)",
            "Hypertension (annual)",
            "Workplace Injury (treatment)",
            "Pregnancy & Delivery",
            "Dental Emergency",
            "Mental Health Crisis",
        ],
        "emergency_pathway_eur": [8500, 4200, 6800, 9500, 1200, 5500],
        "preventive_pathway_eur": [2400, 1100, 800, 3200, 350, 1800],
        "savings_pct": [72, 74, 88, 66, 71, 67],
    })


# ==============================================================
# MAIN: Generate and save all datasets
# ==============================================================

def main():
    """Generate all datasets and save to data/processed/."""
    print("=" * 60)
    print("GENERATING DATASETS")
    print("=" * 60)

    # 1. Regional data
    df_regional = generate_regional_data()
    df_regional.to_csv(os.path.join(DATA_PROCESSED, "regional_healthcare.csv"), index=False)
    print(f"[1/5] Regional data: {len(df_regional)} regions")

    # 2. Service comparison
    df_services = generate_service_comparison()
    df_services.to_csv(os.path.join(DATA_PROCESSED, "service_comparison.csv"), index=False)
    print(f"[2/5] Service comparison: {len(df_services)} groups")

    # 3. Worker-level data
    df_workers = generate_worker_data(n=2000)
    df_workers.to_csv(os.path.join(DATA_PROCESSED, "worker_survey.csv"), index=False)
    print(f"[3/5] Worker data: {len(df_workers)} records")

    # 4. Barriers
    barriers = generate_barriers()
    pd.DataFrame(list(barriers.items()), columns=["barrier", "pct"]).to_csv(
        os.path.join(DATA_PROCESSED, "barriers.csv"), index=False)
    print(f"[4/5] Barriers: {len(barriers)} items")

    # 5. Cost comparison
    df_costs = generate_cost_comparison()
    df_costs.to_csv(os.path.join(DATA_PROCESSED, "cost_comparison.csv"), index=False)
    print(f"[5/5] Cost comparison: {len(df_costs)} conditions")

    # Summary statistics
    print(f"\n{'='*60}")
    print("DATASET VALIDATION")
    print(f"{'='*60}")
    print(f"\nWorker data correlations (should be meaningful now):")
    corr_fear = df_workers["fear_of_deportation"].corr(df_workers["unmet_healthcare_need"])
    print(f"  Fear of deportation <-> Unmet needs:  r = {corr_fear:.3f}")

    lang_map = {"None": 0, "Basic": 1, "Intermediate": 2, "Fluent": 3}
    lang_numeric = df_workers["italian_language_level"].map(lang_map)
    corr_lang = lang_numeric.corr(df_workers["unmet_healthcare_need"])
    print(f"  Language level <-> Unmet needs:       r = {corr_lang:.3f}")

    corr_stp = df_workers["knows_stp_rights"].corr(df_workers["er_only_healthcare"])
    print(f"  STP awareness <-> ER-only usage:      r = {corr_stp:.3f}")

    corr_fear_er = df_workers["fear_of_deportation"].corr(df_workers["er_only_healthcare"])
    print(f"  Fear <-> ER-only usage:               r = {corr_fear_er:.3f}")

    print(f"\nKey descriptives:")
    print(f"  Unmet healthcare needs: {df_workers['unmet_healthcare_need'].mean()*100:.1f}%")
    print(f"  ER-only healthcare:     {df_workers['er_only_healthcare'].mean()*100:.1f}%")
    print(f"  STP awareness:          {df_workers['knows_stp_rights'].mean()*100:.1f}%")
    print(f"  STP actual usage:       {df_workers['has_used_stp'].mean()*100:.1f}%")
    print(f"  Fear of deportation:    {df_workers['fear_of_deportation'].mean()*100:.1f}%")

    print(f"\nAll datasets saved to: {DATA_PROCESSED}")


if __name__ == "__main__":
    main()
