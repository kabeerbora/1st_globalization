# Spain — Capital Stock Source

## Data Location
The Spain capital stock data are **hardcoded directly in `01_build_data.py`** (the `spain_nk` dictionary). No separate data file is needed.

## Original Source
Prados de la Escosura, L. (2022). "Capital in Spain, 1850–2019." Unpublished dataset (Table A1).

Companion paper: Prados de la Escosura, L. (2017). *Spanish Economic Growth, 1850–2015*. Palgrave Macmillan.

## Sheet / Table Used
Table A1: Net Capital Stock by type, million current euros, 1850–2019

## Columns Used (from Table A1)
- Column 1: Dwellings (residential buildings)
- Column 2: Other construction
- Column 3: Machinery & equipment
- Column 4: Transport equipment
- Column 5: Total net capital stock (sum of all types)
- Column 6: Consumption of fixed capital (depreciation)

## Variable Constructed
Net productive capital = Total − Dwellings = Col.5 − Col.1

```
spain_prod_ratio = (Total - Dwellings) / Total
```

This ratio is applied to the original `Fixed_capital_stock` for Spain in `1st_global.xlsx` to convert it to a productive (non-residential) net capital basis.

## Period
1850–2019 (we use 1870–1913)

## Notes
The original data are in current euros (the series is constructed in euros retroactively for historical comparability). Since we use the ratio productive/total (not absolute levels), the currency denomination cancels out.
