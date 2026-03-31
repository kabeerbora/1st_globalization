# Replication Package
## "An Unequal Equalization: Understanding the Response of Rates of Profit during the First Age of Globalization (1870--1913)"
### *Review of Social Economy* (Resubmission, March 2026)

---

## Overview

This package contains all code and data required to replicate every table and figure in the manuscript. Running the two scripts in order reproduces the full analysis from raw sources to regression output.

## Requirements

- Python 3.9+
- Packages: `pandas`, `numpy`, `openpyxl`, `xlrd`, `linearmodels`, `statsmodels`, `pyfixest`, `scipy`

Install with:
```
pip install pandas numpy openpyxl xlrd linearmodels statsmodels pyfixest scipy
```

> **Note:** Reading Stata `.dta` files (Pascali data) also requires the `pyreadstat` package:
> `pip install pyreadstat`

## Directory Structure

```
Replication/
├── README.md                      <- This file
├── 01_build_data.py               <- Step 1: construct net rate of profit dataset
├── 02_run_regressions.py          <- Step 2: run all regressions (TWFE, IV, LOO)
├── Data/
│   ├── Common/
│   │   ├── 1st_global.xlsx        <- Main assembled panel (all 7 countries, 1870-1913)
│   │   ├── net_productive_capital_stock_nl_1870_1913.csv  <- Netherlands net productive K
│   │   ├── net_productive_capital_stock_fr_1820_1913.csv  <- France net productive K
│   │   ├── dyadic_trade_bilateral_pop.csv  <- Bilateral trade flows for IV gravity model
│   │   ├── population_data/
│   │   │   └── 1st_global.csv     <- GDP/population data (Maddison 2023)
│   │   └── pascali_data/          <- Pascali (2017) replication data (AER)
│   │       ├── BILATERAL_TRADE_PUBLIC.dta      <- Bilateral trade flows, 1845-1900
│   │       ├── BILATERAL_DISTANCES_PUBLIC.dta  <- Sail/steam travel times (time-invariant)
│   │       ├── COUNTRY_LEVEL_PUBLIC.dta        <- Country-year panel (GDP, population)
│   │       ├── FREIGHT_RATES_PUBLIC.dta        <- Shipping freight rates by route
│   │       └── CLIWOC_PUBLIC.dta               <- Historical voyage durations (CLIWOC)
│   ├── Germany/
│   │   ├── Germany.xls            <- Piketty-Zucman (2014) German national accounts
│   │   └── SOURCE.md
│   ├── UK/
│   │   ├── a-millennium-of-macroeconomic-data-for-the-uk.xlsx  <- Bank of England (2023)
│   │   └── SOURCE.md
│   ├── Sweden/
│   │   ├── tablesAtoX.xls         <- Edvinsson (2016) Swedish capital stock
│   │   └── SOURCE.md
│   ├── France/
│   │   ├── France.xls             <- Piketty-Zucman (2014) French national accounts
│   │   └── SOURCE.md
│   ├── Netherlands/
│   │   └── SOURCE.md              <- Data hardcoded in 01_build_data.py
│   ├── Spain/
│   │   └── SOURCE.md              <- Data hardcoded in 01_build_data.py
│   └── USA/
│       └── SOURCE.md              <- Dumenil & Levy (2013), via 1st_global.xlsx
```

## How to Replicate

Run from the `Replication/` directory:

```bash
python 01_build_data.py
python 02_run_regressions.py
```

**Step 1** (`01_build_data.py`) reads raw country-level capital stock data, applies net productive capital corrections for each country, and writes `Data/Common/1st_global_net_rop.xlsx`.

**Step 2** (`02_run_regressions.py`) is the single primary replication script. It:
1. Reads the dataset produced by Step 1
2. Applies revised net productive capital stock series for France (Piketty-Zucman constant-price productive stock, deflated to current francs) and the Netherlands (Smits-Horlings-Van Zanden net productive capital stock in million guilders), then recomputes the net rate of profit
3. Constructs the gravity instrument via PPML
4. Runs all TWFE and IV regressions
5. Prints results corresponding to all tables in the manuscript
6. Saves leave-one-out results to `Data/Common/loo_results_net_rop.csv`

## Correspondence Between Outputs and Manuscript Tables

| Script Output                               | Manuscript Location                        |
|---------------------------------------------|--------------------------------------------|
| Summary stats (end of Step 2)               | Table 3 (Summary Statistics)               |
| TWFE full, with lag (Section 5)             | Table 2, Columns (1)-(2)                   |
| TWFE no-controls, no lag                    | Table 2, Column (0)                        |
| Alt. trade measures (exp_gdp, imp_gdp, etc) | Table: other_trade_measures                |
| IV uncertainty bare + full                  | Table 4 (IV Results, `table:iv_results`)   |
| LOO results                                 | Appendix A.3 (`tab:loo_results`)           |
| Export/Import IV decomposition (Section 10) | Table `table:iv_exp_imp`                   |
| Pascali (2017) IV robustness (Section 11)   | Table `table:iv_pascali`                   |
| Beta-convergence (Section 12)               | Table `table:beta_convergence`             |
| Sigma-convergence plot (Section 12)         | Figure `fig:sigma_conv`                    |

## Instrument Descriptions

### Climate Uncertainty Instrument (primary)
Constructed via PPML gravity model using `dyadic_trade_bilateral_pop.csv`. Temperature
uncertainty in destination countries is interacted with maritime distance and colonial
ties to predict bilateral trade flows. Predicted flows are aggregated to country-level
predicted openness and used as an instrument for observed trade openness.

### Pascali (2017) Instrument (robustness)
Constructed from `pascali_data/BILATERAL_TRADE_PUBLIC.dta` and
`pascali_data/BILATERAL_DISTANCES_PUBLIC.dta`. An OLS gravity model is estimated on
bilateral trade data (1845-1900), regressing log exports on the interaction of
5-year period dummies with log sail and steam travel times, plus origin, destination,
and year fixed effects. Period-specific coefficients on sail/steam times are then applied
to the time-invariant distance grid to produce predicted bilateral trade flows for
1870-1913. For years 1901-1913 (beyond the bilateral trade data coverage), the
1895-1900 period coefficients are applied. Predicted flows are aggregated to
country-level predicted openness and used as a second, independent instrument.

### Export/Import IV Decomposition
Uses the same PPML gravity model as the primary instrument, but aggregates predicted
flows separately by direction: flows where the country is the origin identify the
export instrument; flows where the country is the destination identify the import
instrument. The two instruments are estimated from the same gravity model and thus
cannot be used jointly (high collinearity in the first stage).

## Data Sources Summary

See individual `SOURCE.md` files in each country subfolder. Common sources:

- **Bilateral trade & gravity variables**: CEPII (2016), `dyadic_trade_bilateral_pop.csv`
- **GDP (Maddison)**: Maddison Project Database 2023, `population_data/1st_global.csv`
- **Temperature uncertainty**: Berkeley Earth (berkeleyearth.org/data/), merged into `dyadic_trade_bilateral_pop.csv`
- **Trade openness, tariffs, ToT, NFA**: Jorda-Schularick-Taylor Macrohistory Database; Clemens & Williamson (2004); Piketty & Zucman (2014)
- **Pascali (2017) data**: Pascali, L. (2017). "The Wind of Change: Maritime Technology, Trade, and Economic Development." *American Economic Review*, 107(9), 2821-2854. Data downloaded from AEA RCT Registry / AER replication package.
