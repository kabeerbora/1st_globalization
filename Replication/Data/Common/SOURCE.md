# Common Data Files — Sources

---

## 1. `1st_global.xlsx` — Main Panel Dataset

The assembled panel of 7 countries × 44 years (1870–1913) containing:
- Rate of profit (gross, pre-correction): from country-specific sources
- Trade openness (exports + imports)/GDP
- Export/GDP, Import/GDP
- Terms of trade index
- Tariff rate
- Net foreign assets/GDP
- Capital-labor index (normalized 1870 = 1.0)
- Labor hours, GDP (real)

**Sources by variable:**

| Variable | Source |
|----------|--------|
| Trade openness, exp/GDP, imp/GDP, ToT | Jordà, O., Schularick, M., Taylor, A. (2017). "Macrofinancial History and the New Business Cycle Facts." *NBER Macroeconomics Annual* 31. Dataset: https://www.macrohistory.net/database/ |
| Tariff rate | Clemens, M. and Williamson, J. (2004). "Why Did the Tariff-Growth Correlation Change after 1950?" *Journal of Economic Growth* 9(1), 5–46 |
| Net Foreign Assets/GDP | Piketty, T. and Zucman, G. (2014). "Capital is Back." *QJE* 129(3) |
| GDP (real, constant prices) | Maddison Project Database 2023: https://www.rug.nl/ggdc/historicaldevelopment/maddison/ |
| Labor hours | Country-specific (Mitchell 1975; Maddison 2010) |
| Capital-labor index | Constructed by authors from capital stock and labor hour data |

---

## 2. `dyadic_trade_bilateral_pop.csv` — Bilateral Trade & Gravity Variables

Used to construct the instrumental variable (predicted trade openness) via PPML gravity estimation.

**Sources:**

| Variable | Source |
|----------|--------|
| Bilateral trade flows | CEPII TRADHIST Database. Fouquin, M. and Hugot, J. (2016). "Two Centuries of Bilateral Trade and Gravity Data: 1827–2014." CEPII Working Paper 2016-14. http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=32 |
| Maritime distances | CEPII GeoDist Database: http://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=6 |
| Colonial ties | CEPII Colonial Links database |
| Temperature anomaly (destination) | Berkeley Earth annual country-level temperature anomalies: https://berkeleyearth.org/data/ |
| Temperature uncertainty (destination) | Berkeley Earth: same dataset, uncertainty field |
| Population, GDP | Maddison Project Database 2023 (merged at country-year level) |

Coverage: 113 origin × 186 destination countries, 1870–1913, yielding up to 41,188 bilateral observations per year.

---

## 3. `population_data/1st_global.csv` — GDP Data for Gravity Model

Annual GDP in constant prices for all countries in the bilateral trade dataset.

**Source:** Maddison Project Database 2023.
- Bolt, J. and Van Zanden, J.L. (2020). "Maddison style estimates of the evolution of the world economy: A new 2020 update." Maddison Project Working Paper WP-15.
- Download: https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023

---

## 4. `net_productive_capital_stock_nl_1870_1913.csv` — Netherlands Net Productive Capital Stock

Columns: `Year`, `Machinery_Const`, `NonRes_Const`, `Productive_Stock_Machinery`, `Productive_Stock_NonResidential`, `Net_Productive_Capital_Stock`

Units: millions of guilders, constant 1913 prices.

**Construction method:** Asset-specific geometric Perpetual Inventory Method (PIM).
- GFCF data: Smits, J.P., Horlings, E., and Van Zanden, J.L. (2000). *Dutch GNP and its Components, 1800–1913*. Groningen Growth and Development Centre. Table E.2, Col. 1 (machinery & transport) and Col. 3 (other construction); residential dwellings (Col. 2) excluded.
- Depreciation rates: machinery & transport δ = 11%; non-residential construction δ = 2.28% (following Prados de la Escosura & Rosés 2021).
- Initialization: Harberger condition W₁₇₉₉ = I₁₈₀₀ / (δ + g), where g is long-run average real investment growth rate.
- Mid-year productive stock: W_t = K^net_beg + I_t / 2 (OECD 2009 manual convention).
- Used in: `02_run_regressions.py` to replace the Netherlands capital stock for all regressions.

---

## 5. `net_productive_capital_stock_fr_1820_1913.csv` — France Net Productive Capital Stock

Columns: `Year`, `Net_Inv_Current`, `Price_Index`, `Net_Inv_Const`, `Productive_Stock`, `Net_Wealth_End`

Units: `Productive_Stock` in constant 1908-1912 prices (millions of francs); `Price_Index` base = 100 (1908-1912 average).

**Construction method:** Cumulative net investment PIM.
- Net fixed capital formation drawn from: Levy-Leboyer, M. and Bourguignon, F. (2008). *The French Economy in the Nineteenth Century*. Cambridge University Press. Data Appendix. Series already net of depreciation in current prices.
- Deflated to constant prices using a Building Price Index (base: 1908-1912 average = 100).
- Initialization: Harberger condition W_1819 = I_1820 / g.
- Mid-year productive stock: W_t = K^net_beg + I_t / 2 (OECD 2009 manual convention).
- Current-price correction in `02_run_regressions.py`: `Productive_Stock_current = Productive_Stock * (Price_Index / 100)`.
- Used in: `02_run_regressions.py` to replace the France capital stock for all regressions.

---

## 6. `loo_results_net_rop.csv` — Leave-One-Out IV Estimates

Output from `02_run_regressions.py`. Columns: `Country_Dropped`, `Coefficient`, `SE`.
Seven rows, one per country dropped. Used in Table `tab:loo_results` in the manuscript.
