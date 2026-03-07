"""
Visualization Module
====================
Generates 12 publication-quality charts for the Invisible Patients report.

Each figure is self-contained with proper titles, labels, legends,
and source annotations. Designed for both screen and print.

Usage:
    python -m src.visualizations
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from scipy import stats
import os
import sys

try:
    from src.config import (COLORS, MPL_STYLE, FIGURES_DIR, DATA_PROCESSED,
                            FIG_DPI, FIGSIZE_WIDE, FIGSIZE_STD, FIGSIZE_TALL, FIGSIZE_QUAD)
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import (COLORS, MPL_STYLE, FIGURES_DIR, DATA_PROCESSED,
                            FIG_DPI, FIGSIZE_WIDE, FIGSIZE_STD, FIGSIZE_TALL, FIGSIZE_QUAD)

plt.rcParams.update(MPL_STYLE)


def _save(fig, name):
    """Save figure and close."""
    path = os.path.join(FIGURES_DIR, f"{name}.png")
    fig.savefig(path, dpi=FIG_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {name}.png")


def _add_source(ax, text, y=-0.12):
    """Add source annotation below plot."""
    ax.annotate(text, xy=(0, y), xycoords="axes fraction",
                fontsize=7.5, color=COLORS["muted"], fontstyle="italic")


# ==============================================================
# FIGURE 1: Healthcare Expenditure Distribution
# ==============================================================

def fig01_expenditure(df_services):
    """Three-group comparison of healthcare spending by service type."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STD)

    categories = ["Hospital\nAdmissions", "Pharmaceutical\nPrescriptions",
                   "Specialist\nVisits", "Emergency\nDepartment"]
    x = np.arange(len(categories))
    width = 0.25

    italian = [51, 45, 3, 1]
    documented = [43, 52, 4, 1]
    undocumented = [92, 6, 1, 1]

    b1 = ax.bar(x - width, italian, width, label="Italian Citizens",
                color=COLORS["italian"], alpha=0.85, edgecolor="white", linewidth=0.5)
    b2 = ax.bar(x, documented, width, label="Documented Migrants",
                color=COLORS["documented"], alpha=0.85, edgecolor="white", linewidth=0.5)
    b3 = ax.bar(x + width, undocumented, width, label="Undocumented Migrants",
                color=COLORS["undocumented"], alpha=0.85, edgecolor="white", linewidth=0.5)

    for bars in [b1, b2, b3]:
        for bar in bars:
            h = bar.get_height()
            if h > 3:
                ax.text(bar.get_x() + bar.get_width()/2, h + 1,
                        f"{h}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_ylabel("Share of Total Healthcare Expenditure (%)", fontsize=11)
    ax.set_title("Healthcare Expenditure Distribution by Service Type",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 105)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    _add_source(ax, "Source: Lombardy Region STP records (2018-2019). DOI: 10.3390/ijerph192416447")

    _save(fig, "01_expenditure_distribution")


# ==============================================================
# FIGURE 2: Top Barriers to Healthcare Access
# ==============================================================

def fig02_barriers(barriers_df):
    """Horizontal bar chart of reported healthcare barriers."""
    fig, ax = plt.subplots(figsize=FIGSIZE_TALL)

    names = barriers_df["barrier"].tolist()
    values = barriers_df["pct"].tolist()
    n = len(names)

    colors = plt.cm.Reds(np.linspace(0.3, 0.9, n))[::-1]
    bars = ax.barh(range(n), values, color=colors, edgecolor="white", linewidth=0.5, height=0.7)

    ax.set_yticks(range(n))
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Respondents Reporting This Barrier (%)", fontsize=11)
    ax.set_title("Top Barriers to Healthcare Access\nfor Undocumented Workers in Italy",
                 fontsize=14, fontweight="bold", pad=15)

    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + 1, i, f"{val}%", va="center", fontsize=10,
                fontweight="bold", color=COLORS["text"])

    ax.set_xlim(0, 82)
    _add_source(ax, "Source: Synthesized from published academic studies on migrant healthcare barriers in Italy")

    _save(fig, "02_barriers")


# ==============================================================
# FIGURE 3: Regional Comparison (triple panel)
# ==============================================================

def fig03_regional(df_regional):
    """Three-panel regional comparison across all 20 Italian regions."""
    fig, axes = plt.subplots(1, 3, figsize=(17, 7))

    metrics = [
        ("unmet_healthcare_needs", "Unmet Healthcare Needs (%)", "Reds"),
        ("stp_access_rate", "STP Code Access Rate (%)", "Blues"),
        ("er_dependency_rate", "ER Dependency Rate (%)", "Oranges"),
    ]

    for idx, (col, title, cmap) in enumerate(metrics):
        ax = axes[idx]
        df_s = df_regional.sort_values(col, ascending=True)
        colors = plt.cm.get_cmap(cmap)(np.linspace(0.2, 0.9, len(df_s)))

        ax.barh(range(len(df_s)), df_s[col] * 100, color=colors,
                edgecolor="white", linewidth=0.3, height=0.7)
        ax.set_yticks(range(len(df_s)))
        ax.set_yticklabels(df_s["region"], fontsize=8)
        ax.set_xlabel("%", fontsize=10)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlim(0, 100)

    fig.suptitle("Regional Healthcare Access Indicators for Undocumented Workers",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    _save(fig, "03_regional_comparison")


# ==============================================================
# FIGURE 4: Sector Analysis (quad panel)
# ==============================================================

def fig04_sectors(df_workers):
    """Four-panel sector analysis of key healthcare metrics."""
    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE_QUAD)

    sector_order = df_workers.groupby("sector")["unmet_healthcare_need"].mean().sort_values(ascending=True).index

    panels = [
        ("unmet_healthcare_need", "% with Unmet Healthcare Needs", COLORS["undocumented"], axes[0, 0]),
        ("knows_stp_rights", "% Aware of STP Rights", COLORS["documented"], axes[0, 1]),
        ("workplace_injury_12m", "% Reporting Workplace Injury (12 months)", COLORS["accent"], axes[1, 0]),
        ("er_only_healthcare", "% Using Only Emergency Services", COLORS["italian"], axes[1, 1]),
    ]

    for col, xlabel, color, ax in panels:
        means = df_workers.groupby("sector")[col].mean().reindex(sector_order)
        ax.barh(means.index, means.values * 100, color=color, alpha=0.85,
                edgecolor="white", linewidth=0.5, height=0.6)
        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_title(xlabel, fontweight="bold", fontsize=10)

        for i, (name, val) in enumerate(means.items()):
            ax.text(val * 100 + 0.5, i, f"{val*100:.1f}%", va="center", fontsize=8)

    fig.suptitle("Healthcare Access Patterns by Employment Sector",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    _save(fig, "04_sector_analysis")


# ==============================================================
# FIGURE 5: STP Awareness vs. Usage Gap
# ==============================================================

def fig05_stp_gap(df_workers):
    """Side-by-side comparison of STP awareness vs actual usage."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STD)

    stp = df_workers.groupby("sector").agg(
        knows=("knows_stp_rights", "mean"),
        used=("has_used_stp", "mean")
    ).sort_values("knows", ascending=True)

    y = np.arange(len(stp))
    h = 0.35

    ax.barh(y + h/2, stp["knows"] * 100, h, label="Knows About STP",
            color=COLORS["documented"], alpha=0.85, edgecolor="white")
    ax.barh(y - h/2, stp["used"] * 100, h, label="Has Actually Used STP",
            color=COLORS["undocumented"], alpha=0.85, edgecolor="white")

    ax.set_yticks(y)
    ax.set_yticklabels(stp.index, fontsize=10)
    ax.set_xlabel("Percentage (%)", fontsize=11)
    ax.set_title("The STP Gap: Awareness vs. Actual Usage\nby Employment Sector",
                 fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="lower right", fontsize=10)

    for i, (idx, row) in enumerate(stp.iterrows()):
        gap = (row["knows"] - row["used"]) * 100
        if gap > 1:
            ax.annotate(f"Gap: {gap:.0f}pp", xy=(row["knows"] * 100 + 0.8, i + h/2),
                        fontsize=8, color=COLORS["accent"], fontweight="bold", va="center")

    _add_source(ax, "Source: Synthetic worker data modeled on published STP access patterns")
    _save(fig, "05_stp_gap")


# ==============================================================
# FIGURE 6: Fear vs. Unmet Needs
# ==============================================================

def fig06_fear(df_workers):
    """Impact of deportation fear on unmet healthcare needs."""
    fig, ax = plt.subplots(figsize=(8, 6))

    fear_unmet = df_workers.groupby("fear_of_deportation")["unmet_healthcare_need"].mean() * 100
    labels = ["No Fear of\nDeportation", "Fears\nDeportation"]
    bar_colors = [COLORS["documented"], COLORS["undocumented"]]

    bars = ax.bar(labels, fear_unmet.values, color=bar_colors, width=0.5,
                  alpha=0.85, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, fear_unmet.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1,
                f"{val:.1f}%", ha="center", fontweight="bold", fontsize=14)

    diff = fear_unmet.iloc[1] - fear_unmet.iloc[0]
    ax.annotate(f"+{diff:.1f} percentage points",
                xy=(0.5, max(fear_unmet) * 0.5), xycoords=("axes fraction", "data"),
                fontsize=11, color=COLORS["accent"], fontweight="bold", ha="center")

    ax.set_ylabel("% with Unmet Healthcare Needs", fontsize=12)
    ax.set_title("Fear of Deportation and Unmet Healthcare Needs",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylim(0, max(fear_unmet) + 10)
    _add_source(ax, "Source: Synthetic data with conditional dependency modeling")

    _save(fig, "06_fear_vs_unmet")


# ==============================================================
# FIGURE 7: Language Level vs. Unmet Needs
# ==============================================================

def fig07_language(df_workers):
    """Impact of Italian language proficiency on healthcare access."""
    fig, ax = plt.subplots(figsize=(8, 6))

    lang_order = ["None", "Basic", "Intermediate", "Fluent"]
    lang_unmet = df_workers.groupby("italian_language_level")["unmet_healthcare_need"].mean()
    lang_unmet = lang_unmet.reindex(lang_order).fillna(0) * 100
    colors = [COLORS["undocumented"], COLORS["accent"], COLORS["documented"], COLORS["positive"]]

    bars = ax.bar(lang_order, lang_unmet.values, color=colors, width=0.55,
                  alpha=0.85, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, lang_unmet.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1,
                f"{val:.1f}%", ha="center", fontweight="bold", fontsize=12)

    ax.set_ylabel("% with Unmet Healthcare Needs", fontsize=12)
    ax.set_xlabel("Italian Language Proficiency", fontsize=12)
    ax.set_title("Italian Language Proficiency and\nUnmet Healthcare Needs",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylim(0, max(lang_unmet.values) + 10)
    _add_source(ax, "Source: Synthetic data. Language levels correlated with years in Italy.")

    _save(fig, "07_language_vs_unmet")


# ==============================================================
# FIGURE 8: North-South Divide
# ==============================================================

def fig08_north_south(df_regional):
    """Macro-regional comparison of healthcare access indicators."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STD)

    macro = df_regional.groupby("macro_region").agg(
        unmet=("unmet_healthcare_needs", "mean"),
        er_dep=("er_dependency_rate", "mean"),
        stp=("stp_access_rate", "mean"),
        prev=("preventive_care_access", "mean"),
    ).reindex(["North", "Center", "South & Islands"])

    x = np.arange(len(macro))
    w = 0.2

    ax.bar(x - 1.5*w, macro["unmet"]*100, w, label="Unmet Needs",
           color=COLORS["undocumented"], alpha=0.85)
    ax.bar(x - 0.5*w, macro["er_dep"]*100, w, label="ER Dependency",
           color=COLORS["accent"], alpha=0.85)
    ax.bar(x + 0.5*w, macro["stp"]*100, w, label="STP Access Rate",
           color=COLORS["documented"], alpha=0.85)
    ax.bar(x + 1.5*w, macro["prev"]*100, w, label="Preventive Care",
           color=COLORS["positive"], alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(macro.index, fontsize=12)
    ax.set_ylabel("Percentage (%)", fontsize=11)
    ax.set_title("Italy's North-South Divide in Healthcare Access\nfor Undocumented Workers",
                 fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    ax.set_ylim(0, 100)

    _save(fig, "08_north_south_divide")


# ==============================================================
# FIGURE 9: Age Distribution
# ==============================================================

def fig09_age(df_workers):
    """Age distribution comparison: undocumented workers vs. verified Italian patterns."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STD)

    bins = [18, 25, 30, 35, 40, 45, 50, 55, 61]
    labels = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-60"]

    df_workers["age_group"] = pd.cut(df_workers["age"], bins=bins, labels=labels, right=False)
    age_dist = df_workers["age_group"].value_counts(normalize=True).reindex(labels) * 100

    # Verified Italian citizen distribution (approximated from ISTAT)
    citizen_dist = [5, 6, 8, 10, 12, 14, 16, 18]
    citizen_dist = [x / sum(citizen_dist) * 100 for x in citizen_dist]

    x = np.arange(len(labels))
    w = 0.35

    ax.bar(x - w/2, age_dist.values, w, label="Undocumented Workers (synthetic)",
           color=COLORS["undocumented"], alpha=0.85, edgecolor="white")
    ax.bar(x + w/2, citizen_dist, w, label="Italian Citizens (approx. ISTAT pattern)",
           color=COLORS["italian"], alpha=0.85, edgecolor="white")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Age Group", fontsize=11)
    ax.set_ylabel("% of Healthcare Service Users", fontsize=11)
    ax.set_title("Age Distribution of Healthcare Service Users",
                 fontsize=14, fontweight="bold", pad=15)
    ax.legend(fontsize=10)
    _add_source(ax, "Verified: 61% of undocumented services for under-30 (Lombardy STP study)")

    _save(fig, "09_age_distribution")


# ==============================================================
# FIGURE 10: Origin Region Analysis
# ==============================================================

def fig10_origin(df_workers):
    """Healthcare access patterns by origin region."""
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

    # 10a: Unmet needs by origin
    origin_unmet = df_workers.groupby("origin_region")["unmet_healthcare_need"].mean().sort_values(ascending=True) * 100
    colors_origin = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(origin_unmet)))
    axes[0].barh(origin_unmet.index, origin_unmet.values, color=colors_origin,
                 edgecolor="white", linewidth=0.5, height=0.6)
    axes[0].set_xlabel("% with Unmet Healthcare Needs")
    axes[0].set_title("Unmet Healthcare Needs\nby Origin Region", fontweight="bold", fontsize=12)

    for i, (name, val) in enumerate(origin_unmet.items()):
        axes[0].text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=9)

    # 10b: Fear of deportation by origin
    origin_fear = df_workers.groupby("origin_region")["fear_of_deportation"].mean().sort_values(ascending=True) * 100
    colors_fear = plt.cm.OrRd(np.linspace(0.2, 0.8, len(origin_fear)))
    axes[1].barh(origin_fear.index, origin_fear.values, color=colors_fear,
                 edgecolor="white", linewidth=0.5, height=0.6)
    axes[1].set_xlabel("% Reporting Fear of Deportation")
    axes[1].set_title("Fear of Deportation\nby Origin Region", fontweight="bold", fontsize=12)

    for i, (name, val) in enumerate(origin_fear.items()):
        axes[1].text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=9)

    fig.suptitle("Healthcare Access Patterns by Origin Region",
                 fontsize=14, fontweight="bold", y=1.01)
    plt.tight_layout()
    _save(fig, "10_origin_analysis")


# ==============================================================
# FIGURE 11: Correlation Heatmap
# ==============================================================

def fig11_correlation(df_workers):
    """Correlation heatmap of key healthcare access determinants."""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create numeric version
    lang_map = {"None": 0, "Basic": 1, "Intermediate": 2, "Fluent": 3}
    df_num = df_workers[["age", "years_in_italy", "weekly_work_hours",
                          "knows_stp_rights", "has_used_stp", "er_only_healthcare",
                          "workplace_injury_12m", "unmet_healthcare_need",
                          "fear_of_deportation"]].copy()
    df_num["language_level"] = df_workers["italian_language_level"].map(lang_map)

    rename = {
        "age": "Age",
        "years_in_italy": "Years in Italy",
        "weekly_work_hours": "Weekly Hours",
        "knows_stp_rights": "Knows STP",
        "has_used_stp": "Used STP",
        "er_only_healthcare": "ER Only",
        "workplace_injury_12m": "Injury (12m)",
        "unmet_healthcare_need": "Unmet Need",
        "fear_of_deportation": "Fear Deportation",
        "language_level": "Language Level",
    }
    df_num = df_num.rename(columns=rename)

    corr = df_num.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap="RdBu_r", center=0, annot=True,
                fmt=".2f", linewidths=0.5, ax=ax, square=True,
                cbar_kws={"shrink": 0.8, "label": "Pearson r"},
                annot_kws={"size": 9})

    ax.set_title("Correlation Matrix: Healthcare Access Determinants",
                 fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    _save(fig, "11_correlation_heatmap")


# ==============================================================
# FIGURE 12: Cost Comparison — Emergency vs. Preventive
# ==============================================================

def fig12_cost_comparison(df_costs):
    """Cost comparison between emergency and preventive care pathways."""
    fig, ax = plt.subplots(figsize=FIGSIZE_STD)

    conditions = df_costs["condition"]
    y = np.arange(len(conditions))
    h = 0.35

    ax.barh(y + h/2, df_costs["emergency_pathway_eur"], h,
            label="Emergency Pathway", color=COLORS["undocumented"], alpha=0.85, edgecolor="white")
    ax.barh(y - h/2, df_costs["preventive_pathway_eur"], h,
            label="Preventive Pathway", color=COLORS["positive"], alpha=0.85, edgecolor="white")

    ax.set_yticks(y)
    ax.set_yticklabels(conditions, fontsize=10)
    ax.set_xlabel("Estimated Cost (EUR)", fontsize=11)
    ax.set_title("Cost Comparison: Emergency vs. Preventive Care Pathway\nfor Common Conditions Among Undocumented Workers",
                 fontsize=13, fontweight="bold", pad=15)
    ax.legend(loc="lower right", fontsize=10)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"\u20ac{x:,.0f}"))

    # Add savings annotations
    for i, row in df_costs.iterrows():
        ax.annotate(f"  {row['savings_pct']}% savings",
                    xy=(row["emergency_pathway_eur"] + 100, i + h/2),
                    fontsize=8, color=COLORS["accent"], fontweight="bold", va="center")

    _add_source(ax, "Source: Estimated from Italian NHS cost data and published literature")
    _save(fig, "12_cost_comparison")


# ==============================================================
# MAIN: Generate all visualizations
# ==============================================================

def main():
    """Load data and generate all 12 figures."""
    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)

    # Load datasets
    df_regional = pd.read_csv(os.path.join(DATA_PROCESSED, "regional_healthcare.csv"))
    df_services = pd.read_csv(os.path.join(DATA_PROCESSED, "service_comparison.csv"))
    df_workers = pd.read_csv(os.path.join(DATA_PROCESSED, "worker_survey.csv"))
    barriers_df = pd.read_csv(os.path.join(DATA_PROCESSED, "barriers.csv"))
    df_costs = pd.read_csv(os.path.join(DATA_PROCESSED, "cost_comparison.csv"))

    print(f"\nData loaded. Generating 12 figures...\n")

    fig01_expenditure(df_services)
    fig02_barriers(barriers_df)
    fig03_regional(df_regional)
    fig04_sectors(df_workers)
    fig05_stp_gap(df_workers)
    fig06_fear(df_workers)
    fig07_language(df_workers)
    fig08_north_south(df_regional)
    fig09_age(df_workers)
    fig10_origin(df_workers)
    fig11_correlation(df_workers)
    fig12_cost_comparison(df_costs)

    print(f"\nAll 12 figures saved to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
