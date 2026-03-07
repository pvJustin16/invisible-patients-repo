"""
Configuration module for Invisible Patients project.
Defines colors, paths, constants, and shared settings.
"""

import os

# ==============================================================
# DIRECTORY PATHS
# ==============================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED = os.path.join(PROJECT_ROOT, "data", "processed")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "figures")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

# Create directories if they don't exist
for d in [DATA_RAW, DATA_PROCESSED, FIGURES_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)


# ==============================================================
# COLOR PALETTE
# Designed for accessibility and print quality
# ==============================================================
COLORS = {
    "italian":       "#2C3E50",   # Dark blue-gray — Italian citizens
    "documented":    "#2980B9",   # Medium blue — Documented migrants
    "undocumented":  "#E74C3C",   # Red — Undocumented migrants (highlight)
    "accent":        "#F39C12",   # Orange — Accent / warning
    "positive":      "#27AE60",   # Green — Positive outcomes
    "bg":            "#FAFAFA",   # Light gray — Plot background
    "grid":          "#E0E0E0",   # Grid lines
    "text":          "#333333",   # Body text
    "muted":         "#7F8C8D",   # Secondary text
}

# Ordered palette for multi-group comparisons
PALETTE_3GROUP = [COLORS["italian"], COLORS["documented"], COLORS["undocumented"]]
GROUP_LABELS = ["Italian Citizens", "Documented Migrants", "Undocumented Migrants"]


# ==============================================================
# MATPLOTLIB DEFAULTS
# ==============================================================
MPL_STYLE = {
    "font.family":       "DejaVu Sans",
    "font.size":         11,
    "axes.facecolor":    COLORS["bg"],
    "figure.facecolor":  "white",
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.color":        COLORS["grid"],
    "axes.spines.top":   False,
    "axes.spines.right": False,
}


# ==============================================================
# VERIFIED STATISTICS (from published sources)
# Each entry includes source citation
# ==============================================================

# Source: Lombardy Region STP Study
# DOI: 10.3390/ijerph192416447
EXPENDITURE_HOSPITAL = {"italian": 51, "documented": 43, "undocumented": 92}
EXPENDITURE_PHARMA   = {"italian": 45, "documented": 52, "undocumented": 6}
EXPENDITURE_SPECIAL  = {"italian": 3,  "documented": 4,  "undocumented": 1}
EXPENDITURE_ER       = {"italian": 1,  "documented": 1,  "undocumented": 1}

AVG_COST_PER_SERVICE = {"italian": 2850, "documented": 2200, "undocumented": 3800}
PREVENTABLE_ADMISSIONS = {"italian": 12, "documented": 18, "undocumented": 35}
UNDER_30_PCT = {"italian": 7, "documented": 10, "undocumented": 61}

# Source: ISTAT 2023
FOREIGN_RESIDENTS_ITALY = 5_000_000
PREVENTIVE_CARE_FOREIGN_WOMEN = 0.43
PREVENTIVE_CARE_ITALIAN_WOMEN = 0.67

# Source: ISMU Foundation / Caritas-Migrantes
EST_UNDOCUMENTED_LOW  = 500_000
EST_UNDOCUMENTED_HIGH = 700_000

# Source: Eurostat EU-SILC (hlth_silc_30)
UNMET_NEEDS_NONEU_2024 = 4.0   # % (EU-wide, documented non-EU)
UNMET_NEEDS_NATIONALS_2024 = 3.8  # % (EU-wide)

# Source: PLOS ONE (2023) — EHIS microdata study
UNMET_NEEDS_MIGRANTS_EUROPE = 27.8  # % (overall, all migrants)

# Source: Italian Law — Legislative Decree 286/98, Art. 35
STP_LEGAL_RIGHTS = [
    "Emergency care",
    "Essential and continuous care for illness and injury",
    "Preventive medicine (vaccinations, screenings)",
    "Maternal and child healthcare",
    "Treatment of infectious diseases",
    "Substance abuse treatment",
]


# ==============================================================
# RANDOM SEED (for reproducibility)
# ==============================================================
RANDOM_SEED = 42


# ==============================================================
# FIGURE SETTINGS
# ==============================================================
FIG_DPI = 200
FIG_FORMAT = "png"
FIGSIZE_WIDE = (14, 7)
FIGSIZE_STD = (10, 6)
FIGSIZE_TALL = (10, 8)
FIGSIZE_QUAD = (14, 10)
