"""
Statistical Analysis Module
============================
Performs descriptive and inferential statistics on the
Invisible Patients datasets. Outputs a summary report to console.

Usage:
    python -m src.analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
import sys

try:
    from src.config import DATA_PROCESSED
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import DATA_PROCESSED


def descriptive_stats(df_workers: pd.DataFrame) -> dict:
    """Compute key descriptive statistics from worker-level data."""
    results = {
        "n": len(df_workers),
        "unmet_needs_pct": df_workers["unmet_healthcare_need"].mean() * 100,
        "er_only_pct": df_workers["er_only_healthcare"].mean() * 100,
        "stp_awareness_pct": df_workers["knows_stp_rights"].mean() * 100,
        "stp_usage_pct": df_workers["has_used_stp"].mean() * 100,
        "fear_pct": df_workers["fear_of_deportation"].mean() * 100,
        "injury_pct": df_workers["workplace_injury_12m"].mean() * 100,
        "mean_age": df_workers["age"].mean(),
        "mean_hours": df_workers["weekly_work_hours"].mean(),
        "mean_years_italy": df_workers["years_in_italy"].mean(),
    }
    return results


def chi_square_tests(df_workers: pd.DataFrame) -> list:
    """Run chi-square tests of independence for key relationships."""
    tests = []

    # Test 1: Fear of deportation vs. Unmet needs
    ct1 = pd.crosstab(df_workers["fear_of_deportation"], df_workers["unmet_healthcare_need"])
    chi2, p, dof, _ = stats.chi2_contingency(ct1)
    tests.append({"test": "Fear x Unmet Needs", "chi2": chi2, "p": p, "dof": dof})

    # Test 2: STP awareness vs. ER-only usage
    ct2 = pd.crosstab(df_workers["knows_stp_rights"], df_workers["er_only_healthcare"])
    chi2, p, dof, _ = stats.chi2_contingency(ct2)
    tests.append({"test": "STP Awareness x ER-Only", "chi2": chi2, "p": p, "dof": dof})

    # Test 3: Language level vs. Unmet needs
    ct3 = pd.crosstab(df_workers["italian_language_level"], df_workers["unmet_healthcare_need"])
    chi2, p, dof, _ = stats.chi2_contingency(ct3)
    tests.append({"test": "Language x Unmet Needs", "chi2": chi2, "p": p, "dof": dof})

    # Test 4: Fear vs. STP usage
    ct4 = pd.crosstab(df_workers["fear_of_deportation"], df_workers["has_used_stp"])
    chi2, p, dof, _ = stats.chi2_contingency(ct4)
    tests.append({"test": "Fear x STP Usage", "chi2": chi2, "p": p, "dof": dof})

    return tests


def sector_comparison(df_workers: pd.DataFrame) -> pd.DataFrame:
    """Compare key metrics across employment sectors."""
    return df_workers.groupby("sector").agg(
        n=("age", "count"),
        unmet_needs=("unmet_healthcare_need", "mean"),
        er_only=("er_only_healthcare", "mean"),
        stp_aware=("knows_stp_rights", "mean"),
        stp_used=("has_used_stp", "mean"),
        fear=("fear_of_deportation", "mean"),
        injury_rate=("workplace_injury_12m", "mean"),
        avg_hours=("weekly_work_hours", "mean"),
    ).round(3).sort_values("unmet_needs", ascending=False)


def regional_risk_ranking(df_regional: pd.DataFrame) -> pd.DataFrame:
    """Create composite risk score for each region."""
    df = df_regional.copy()

    # Normalize metrics (higher = worse access)
    df["risk_unmet"] = (df["unmet_healthcare_needs"] - df["unmet_healthcare_needs"].min()) / \
                       (df["unmet_healthcare_needs"].max() - df["unmet_healthcare_needs"].min())
    df["risk_er"] = (df["er_dependency_rate"] - df["er_dependency_rate"].min()) / \
                    (df["er_dependency_rate"].max() - df["er_dependency_rate"].min())
    df["risk_stp"] = 1 - (df["stp_access_rate"] - df["stp_access_rate"].min()) / \
                         (df["stp_access_rate"].max() - df["stp_access_rate"].min())
    df["risk_prev"] = 1 - (df["preventive_care_access"] - df["preventive_care_access"].min()) / \
                          (df["preventive_care_access"].max() - df["preventive_care_access"].min())

    # Composite score (equal weights)
    df["composite_risk_score"] = (df["risk_unmet"] + df["risk_er"] +
                                   df["risk_stp"] + df["risk_prev"]) / 4

    return df[["region", "macro_region", "composite_risk_score"]].sort_values(
        "composite_risk_score", ascending=False).round(3)


def main():
    """Run full statistical analysis."""
    print("=" * 60)
    print("STATISTICAL ANALYSIS")
    print("=" * 60)

    # Load data
    df_workers = pd.read_csv(os.path.join(DATA_PROCESSED, "worker_survey.csv"))
    df_regional = pd.read_csv(os.path.join(DATA_PROCESSED, "regional_healthcare.csv"))

    # 1. Descriptive statistics
    print("\n--- DESCRIPTIVE STATISTICS ---")
    desc = descriptive_stats(df_workers)
    for k, v in desc.items():
        print(f"  {k:30s}: {v:.1f}" if isinstance(v, float) else f"  {k:30s}: {v}")

    # 2. Chi-square tests
    print("\n--- CHI-SQUARE TESTS OF INDEPENDENCE ---")
    tests = chi_square_tests(df_workers)
    for t in tests:
        sig = "***" if t["p"] < 0.001 else "**" if t["p"] < 0.01 else "*" if t["p"] < 0.05 else "ns"
        print(f"  {t['test']:30s}: chi2={t['chi2']:8.2f}  p={t['p']:.4f}  {sig}")

    # 3. Correlation analysis
    print("\n--- KEY CORRELATIONS (Pearson r) ---")
    lang_map = {"None": 0, "Basic": 1, "Intermediate": 2, "Fluent": 3}
    lang_num = df_workers["italian_language_level"].map(lang_map)

    pairs = [
        ("fear_of_deportation", "unmet_healthcare_need", "Fear x Unmet Needs"),
        ("fear_of_deportation", "er_only_healthcare", "Fear x ER-Only"),
        ("knows_stp_rights", "er_only_healthcare", "STP Aware x ER-Only"),
        ("knows_stp_rights", "unmet_healthcare_need", "STP Aware x Unmet Needs"),
    ]
    for c1, c2, label in pairs:
        r, p = stats.pearsonr(df_workers[c1], df_workers[c2])
        print(f"  {label:30s}: r = {r:+.3f}  (p = {p:.4f})")

    r_lang, p_lang = stats.pearsonr(lang_num, df_workers["unmet_healthcare_need"])
    print(f"  {'Language x Unmet Needs':30s}: r = {r_lang:+.3f}  (p = {p_lang:.4f})")

    # 4. Sector comparison
    print("\n--- SECTOR COMPARISON ---")
    sector_df = sector_comparison(df_workers)
    print(sector_df.to_string())

    # 5. Regional risk ranking
    print("\n--- REGIONAL RISK RANKING (composite score) ---")
    risk = regional_risk_ranking(df_regional)
    for _, row in risk.iterrows():
        bar = "#" * int(row["composite_risk_score"] * 30)
        print(f"  {row['region']:25s} [{row['macro_region']:17s}]  {row['composite_risk_score']:.3f}  {bar}")

    # Save analysis outputs
    sector_df.to_csv(os.path.join(DATA_PROCESSED, "analysis_sector_comparison.csv"))
    risk.to_csv(os.path.join(DATA_PROCESSED, "analysis_regional_risk.csv"), index=False)

    print(f"\nAnalysis outputs saved to: {DATA_PROCESSED}")


if __name__ == "__main__":
    main()
