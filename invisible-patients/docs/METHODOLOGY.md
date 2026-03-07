# Methodology

## Approach

This project uses a **mixed-methods data science approach**, combining verified published statistics with synthetic microdata modeling to analyze healthcare access gaps for undocumented workers in Italy.

## Why Synthetic Data?

Individual-level data on undocumented populations is not publicly available for privacy and safety reasons. EU-SILC surveys explicitly exclude people not in registered households. The STP code system anonymizes records every 6 months, preventing longitudinal tracking. Therefore, we generate synthetic worker-level data calibrated to published aggregate statistics.

## Conditional Dependency Modeling

Unlike naive random generation, our synthetic data builds in realistic conditional relationships:

- **Language level** depends on **years in Italy** (longer stay = better Italian)
- **Fear of deportation** depends on **years in Italy** and **origin region**
- **STP awareness** depends on **sector**, **language level**, and **years in Italy**
- **STP usage** depends on **awareness** AND **absence of fear**
- **ER-only healthcare** depends on **STP usage** and **language level**
- **Unmet healthcare needs** depends on **fear**, **language**, **STP awareness**, and **sector**

## Statistical Methods

1. **Descriptive statistics** — means, proportions, cross-tabulations
2. **Chi-square tests** — independence testing between categorical variables
3. **Pearson correlations** — bivariate relationships between access determinants
4. **Composite risk scoring** — normalized multi-indicator regional ranking

## Limitations

- Synthetic data cannot capture real-world complexity
- Regional estimates (outside Lombardy) are calibrated approximations
- Sector-specific figures have no direct published source
- The STP code system inherently undercounts the undocumented population
- Self-reported data (from EU-SILC) is subject to response and social desirability bias
