# Netherlands — Capital Stock Source

## Data Location
The Netherlands capital stock data are **hardcoded directly in `01_build_data.py`** (the `nld_gfcf` and `nld_dep` dictionaries). No separate data file is needed.

## Original Source

### GFCF by asset type (Table E.2):
Smits, J.-P., Horlings, E., and Van Zanden, J.L. (2000). *Dutch GNP and its Components, 1800–1913*. Groningen Growth and Development Centre Monograph Series No. 5. University of Groningen.

Available at: https://www.rug.nl/ggdc/historicaldevelopment/na/

### Depreciation (Table F.1):
Same source: Smits, Horlings & Van Zanden (2000), Table F.1.

## Variable Constructed
Net productive capital stock via Perpetual Inventory Method (PIM):

```
Productive GFCF = Machinery & Transport + Infrastructure (excludes residential dwellings)
Total GFCF     = All asset types
Productive dep  = Total depreciation × (Productive GFCF / Total GFCF)

K_net_productive_t = K_net_productive_{t-1} + Productive GFCF_t − Productive dep_t
K_net_total_t      = K_net_total_{t-1}      + Total GFCF_t       − Total dep_t

Productive/Total ratio = K_net_productive_t / K_net_total_t
```

This ratio is applied to the original `Fixed_capital_stock` for the Netherlands in `1st_global.xlsx`, which represents total net capital, to obtain productive net capital (excluding residential dwellings).

## Units
Million guilders (current prices), 1800–1913

## Period
PIM from 1800 (K=0 baseline), using 1870–1913

## Notes
Depreciation data are available from 1807; years 1800–1806 use dep=0 (negligible effect on 1870+ ratios). The productive/total ratio is stable by the 1860s.
