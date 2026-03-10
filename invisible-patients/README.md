# Invisible Patients

**Healthcare Access Gaps for Undocumented Workers in Italy's Informal Economy**

A data science policy report analyzing how undocumented workers in Italy's hospitality, logistics, and gig economy sectors are systematically excluded from the healthcare system they are legally entitled to use.

---

## The Problem

Italy's National Health Service (SSN) legally guarantees healthcare to undocumented migrants through the **STP code** (*Straniero Temporaneamente Presente*). In practice, **92% of healthcare spending** for undocumented workers goes to emergency hospital admissions — compared to 51% for Italian citizens. They receive almost no preventive care, no GP access, and no continuity of treatment.

**Key Statistics (from published research):**

| Metric | Italian Citizens | Documented Migrants | Undocumented Migrants |
|--------|:---:|:---:|:---:|
| Hospital admission spend | 51% | 43% | **92%** |
| Pharmaceutical spend | 45% | 52% | **6%** |
| Under-30 share of services | 7% | 10% | **61%** |
| Preventable admissions | 12% | 18% | **35%** |

*Source: Lombardy Region STP records, published in Int. J. Environ. Res. Public Health (2022)*

---


---

## Visualizations

The project produces **12 publication-quality charts** covering:

1. Healthcare expenditure distribution (3-group comparison)
2. Top barriers to healthcare access
3. Regional comparison across 20 Italian regions
4. Sector analysis (4 metrics x 6 sectors)
5. STP awareness vs. actual usage gap
6. Fear of deportation impact on unmet needs
7. Language proficiency impact on unmet needs
8. North-South divide comparison
9. Age distribution of healthcare service users
10. Origin region and healthcare patterns
11. Correlation heatmap of access determinants
12. Cost comparison: emergency vs. preventive pathway

---

## Data Sources

| Source | Type | Status |
|--------|------|--------|
| Lombardy Region STP Study (2022) | Peer-reviewed | Verified |
| Eurostat EU-SILC (hlth_silc_08, hlth_silc_30) | Official statistics | Verified |
| ISTAT Foreign Resident Statistics (2023) | Official statistics | Verified |
| ISMU Foundation Estimates | Research organization | Verified |
| Italian Legislative Decree 286/98 | Legal framework | Verified |
| Worker-level dataset (n=2,000) | Synthetic | Modeled on published distributions |

> **Transparency note:** This project combines verified published data with synthetic modeling. The [DATA_SOURCES.md](docs/DATA_SOURCES.md) file documents exactly which numbers come from which sources, and which are estimates.

---

## Key Findings

1. **The Emergency Room Trap:** Undocumented workers spend 92% of healthcare budget on hospital admissions because they cannot access GPs, prescriptions, or specialist referrals.

2. **The Information Gap:** An estimated 48% of undocumented workers don't know the STP code exists. Even among those who do, fewer than half have used it.

3. **Fear as the Primary Barrier:** 65-68% of undocumented workers avoid healthcare due to fear of deportation, despite Italian law prohibiting healthcare workers from reporting patients.

4. **The North-South Divide:** Southern regions with larger informal economies show 2x higher unmet healthcare needs compared to northern regions.

5. **Gig Economy Workers Are Most Vulnerable:** Highest ER dependency, lowest STP awareness, highest unmet needs among all informal sectors.

---

## Tech Stack

- **Python 3.10+**
- **pandas** — Data manipulation
- **numpy** — Numerical computing
- **matplotlib** — Core visualizations
- **seaborn** — Statistical plots
- **scipy** — Statistical testing
- **reportlab** — PDF report generation

---

## Author

**Justin Plammootil Varghese**
Data Analyst | Aspiring Data Scientist

- Email: pv.justin16@gmail.com
- LinkedIn: [linkedin.com/in/pv-justin](https://linkedin.com/in/pv-justin)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

This project draws on the work of researchers at Bocconi University (Lombardy STP study), Eurostat, ISTAT, ISMU Foundation, and the many NGOs (Emergency, NAGA Milano, Caritas) working to close healthcare gaps for migrants in Italy.
