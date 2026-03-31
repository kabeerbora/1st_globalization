# France — Capital Stock Source

## File
`France.xls`

## Original Source
Piketty, T. and Zucman, G. (2014). "Capital is Back: Wealth-Income Ratios in Rich Countries 1700–2010." *Quarterly Journal of Economics*, 129(3), 1255–1310.

Data appendix available at: http://piketty.pse.ens.fr/en/capitalisback

## Sheets Used

### Table FR.12b
- Column 9 (index 8): Gross Fixed Capital Formation / National Income ratio
- Column 10 (index 9): Depreciation / National Income ratio

### Table FR.1
- Column 2 (index 1): National Income in absolute values (billion current francs)

## Variable Constructed
Net productive capital stock constructed via Perpetual Inventory Method (PIM):

```
K_gross_t = K_gross_{t-1} + GFCF_t
K_net_t   = K_net_{t-1}   + (GFCF_t − Depreciation_t)
Net/Gross ratio_t = K_net_t / K_gross_t
```

The PIM is run from 1820 (K=0 baseline) through 1913. The net/gross ratio at each year is then applied to the original productive capital stock series for France (which captures the *scope* of productive assets, excluding residential dwellings and government assets) to convert it to a net basis.

GFCF_t = (GFCF/NI ratio from FR.12b) × (NI in billion FF from FR.1)
Depreciation_t = (Dep/NI ratio from FR.12b) × (NI in billion FF from FR.1)

## Period
PIM runs 1820–1913; we use 1870–1913

## Notes
Direct annual net capital stock series for France at the required disaggregation (productive only, excluding residential) are not available. The PIM approach follows Boucekkine, Le Van, and Licandro (BLL) depreciation methodology as compiled in the Piketty-Zucman data. The net/gross ratio stabilizes by the 1850s, so the 1820 starting point of the PIM introduces minimal endpoint bias for our 1870–1913 sample.
