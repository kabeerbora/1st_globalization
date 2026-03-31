# USA — Capital Stock Source

## Data Location

The USA capital stock data are embedded in `Data/Common/1st_global.xlsx` (column `Fixed_capital_stock` for Country == 'USA'). **No separate correction is applied.**

## Original Source

Duménil, G. and Lévy, D. (2013). *The Crisis of Neoliberalism*. Harvard University Press.

Dataset: "The profit rate in the United States from 1869 to 2012."
Available at: https://people.umass.edu/dbasu/Data/DumenilLevyData2016

## Variable Used

The `Fixed_capital_stock` column for the USA in `1st_global.xlsx` is taken directly from Duménil & Lévy (2013), which already reports the **net productive capital stock** (private non-residential fixed assets, net of depreciation, in billion USD).

No additional correction is needed because:

1. The series is already net of depreciation (not gross)
2. It already excludes residential dwellings
3. It covers private industries only (consistent with the Marxian productive capital concept)

## Period

1869–2012 (we use 1870–1913)

## Notes

The rate of profit for the USA is thus `rop = profit / Fixed_capital_stock`, where profit = surplus value proxy drawn from the same Duménil & Lévy dataset. In `01_build_data.py`, the USA net capital stock is set equal to `Fixed_capital_stock` without modification (line: `df.loc[mask_usa, 'net_capital_stock'] = df.loc[mask_usa, 'Fixed_capital_stock']`).
