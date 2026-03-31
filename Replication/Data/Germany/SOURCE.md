# Germany — Capital Stock Source

## File
`Germany.xls`

## Original Source
Piketty, T. and Zucman, G. (2014). "Capital is Back: Wealth-Income Ratios in Rich Countries 1700–2010." *Quarterly Journal of Economics*, 129(3), 1255–1310.

Data appendix available at: http://piketty.pse.ens.fr/en/capitalisback

## Sheet Used
`DataDE1c`

## Columns Used
- Column 75 (index 74): Agricultural fixed assets (billion Reichsmarks, net)
- Column 76 (index 75): Business assets (billion Reichsmarks, net)

## Variable Constructed
Net productive capital stock = Agricultural fixed assets + Business assets
(excludes land, residential dwellings, and government assets)

## Period
1860–1920 (we use 1870–1913)

## Notes
The original dataset includes land in total wealth. We strip land out by summing only the fixed productive asset categories (AgriFixed + BusinessAssets). This is consistent with the Marxian concept of productive capital (means of production, excluding unproduced assets).
