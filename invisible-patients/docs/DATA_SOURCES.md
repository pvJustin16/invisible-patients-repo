# Data Sources & Reliability

## Verified Data (from peer-reviewed and official sources)

### Lombardy Region STP Study
- **Citation:** Int. J. Environ. Res. Public Health 2022, 19, 16447
- **DOI:** 10.3390/ijerph192416447
- **Data:** Official Lombardy NHS records for STP code holders (2018-2019)
- **Verified figures:** Hospital admission 92%, pharmaceutical 6%, under-30 share 61%, preventable admissions 35%

### Eurostat EU-SILC
- **Datasets:** hlth_silc_08, hlth_silc_30
- **Coverage:** 2015-2024, EU member states
- **Verified figures:** Unmet medical needs by citizenship status, self-perceived health

### ISTAT (Italian National Statistics)
- **Source:** dati.istat.it
- **Verified figures:** 5M+ foreign residents, 43% preventive care for foreign women vs 67% Italian women

### Italian Law
- **Legislative Decree 286/98, Article 35:** STP code rights, prohibition on reporting

## Estimated Data (calibrated but not directly measured)

- Regional breakdowns (except Lombardy)
- Sector-specific healthcare patterns
- Barrier percentages (ranking order verified, exact % estimated)

## Synthetic Data

- Worker-level dataset (n=2,000): generated with conditional dependencies
- Correlations built in to reflect published relationships

## How to Replace with Real Data

1. **Eurostat:** https://ec.europa.eu/eurostat/databrowser/ (hlth_silc_08, hlth_silc_30)
2. **ISTAT:** https://dati.istat.it/ (foreign residents, health by region)
3. **INAIL:** https://dati.inail.it/ (workplace injuries by nationality)
