# Data Construction — Code and Output Verification

**Script:** `01_build_data.py`
**Run from:** `Replication/` directory (`python 01_build_data.py`)
**Output:** `Data/Common/1st_global_net_rop.xlsx`

Each block below is the exact code that produces the output shown immediately beneath it.

---

## Step 1 — Imports and Load Dataset

```python
import xlrd
import openpyxl
import pandas as pd
import numpy as np
from pathlib import Path

DATA_COMMON = Path("Data/Common")
DATA_DE     = Path("Data/Germany")
DATA_UK     = Path("Data/UK")
DATA_SE     = Path("Data/Sweden")
DATA_FR     = Path("Data/France")

print("Loading original dataset...")
df = pd.read_excel(DATA_COMMON / "1st_global.xlsx")
print(f"Original data: {df.shape[0]} rows, countries: {df['Country'].unique().tolist()}")

df['rop']                = pd.to_numeric(df['rop'], errors='coerce')
df['Fixed_capital_stock']= pd.to_numeric(df['Fixed_capital_stock'], errors='coerce')
df['Year']               = pd.to_numeric(df['Year'], errors='coerce').astype(int)

df['profit_old']         = df['rop'] * df['Fixed_capital_stock']
df['net_capital_stock']  = np.nan
df['rop_net']            = np.nan
```

```
Loading original dataset...
Original data: 308 rows, countries: ['Germany', 'Spain', 'France', 'UK', 'Netherlands', 'Sweden', 'USA']
```

✅ 7 countries × 44 years = 308 observations. Matches manuscript panel.

---

## Step 2 — Germany: Piketty-Zucman (2014)

**Source:** `Data/Germany/Germany.xls` · Sheet `DataDE1c` · Col. 74 (Agricultural fixed assets) + Col. 75 (Business assets)

```python
print("\nExtracting Germany net capital stock (Piketty-Zucman 2014)...")

wb_de = xlrd.open_workbook(DATA_DE / "Germany.xls")
ws_de = wb_de.sheet_by_name("DataDE1c")

germany_net_k = {}
for r in range(ws_de.nrows):
    row = ws_de.row_values(r)
    if isinstance(row[0], float) and 1860 <= row[0] <= 1920:
        yr       = int(row[0])
        agri     = row[74] if row[74] != '' else np.nan
        business = row[75] if row[75] != '' else np.nan
        if not np.isnan(agri) and not np.isnan(business):
            germany_net_k[yr] = agri + business

print(f"  Germany net K available: {min(germany_net_k.keys())}–{max(germany_net_k.keys())}")
print(f"  Germany net K 1870: {germany_net_k.get(1870, 'N/A'):.3f} bn Reichsmarks")

for idx, row in df[df['Country'] == 'Germany'].iterrows():
    yr = row['Year']
    if yr in germany_net_k:
        df.at[idx, 'net_capital_stock'] = germany_net_k[yr]
```

```
Extracting Germany net capital stock (Piketty-Zucman 2014)...
  Germany net K available: 1860–1913
  Germany net K 1870: 33.530 bn Reichsmarks
```

✅ Full 1870–1913 coverage. Net productive K = Col. 74 + Col. 75 (excludes land and residential wealth).

---

## Step 3 — UK: Bank of England Millennium Data

**Source:** `Data/UK/a-millennium-of-macroeconomic-data-for-the-uk.xlsx` · Sheet `A55. Capital Stock` · Col. 4 (NonDwellings market sector, net, £mn)

```python
print("\nExtracting UK net capital stock (Bank of England 2023, Feinstein & Pollard)...")

wb_uk = openpyxl.load_workbook(
    DATA_UK / "a-millennium-of-macroeconomic-data-for-the-uk.xlsx",
    read_only=True, data_only=True
)
ws_uk = wb_uk["A55. Capital Stock"]

uk_net_k = {}
for row in ws_uk.iter_rows(min_row=7, values_only=True):
    if row[0] is not None and isinstance(row[0], (int, float)) and 1860 <= row[0] <= 1920:
        yr  = int(row[0])
        val = row[4]   # Col. 4: NonDwellings market sector, £mn, net
        if val is not None:
            uk_net_k[yr] = val

print(f"  UK net K available: {min(uk_net_k.keys())}–{max(uk_net_k.keys())}")
print(f"  UK net K 1870: {uk_net_k.get(1870, 'N/A')} £mn")

for idx, row in df[df['Country'] == 'UK'].iterrows():
    yr = row['Year']
    if yr in uk_net_k:
        df.at[idx, 'net_capital_stock'] = uk_net_k[yr]
```

```
Extracting UK net capital stock (Bank of England 2023, Feinstein & Pollard)...
  UK net K available: 1860–1920
  UK net K 1870: 1230 £mn
```

✅ NonDwellings market-sector series used directly — no further correction required (Table 1, manuscript).

---

## Step 4 — Sweden: Edvinsson (2016)

**Source:** `Data/Sweden/tablesAtoX.xls` · Sheet `Data` · Col. 107 (Private net total) − Col. 101 (Residential buildings)

```python
print("\nExtracting Sweden net capital stock (Edvinsson 2016)...")

wb_se = xlrd.open_workbook(DATA_SE / "tablesAtoX.xls")
ws_se = wb_se.sheet_by_name("Data")

sweden_net_k = {}
for r in range(ws_se.nrows):
    row = ws_se.row_values(r)
    if row[99] != '' and isinstance(row[99], float) and 1860 <= row[99] <= 1920:
        yr          = int(row[99])
        priv_total  = row[106] if row[106] != '' else np.nan  # Col. 107 (0-indexed: 106)
        residential = row[100] if row[100] != '' else np.nan  # Col. 101 (0-indexed: 100)
        if not np.isnan(priv_total) and not np.isnan(residential):
            sweden_net_k[yr] = priv_total - residential

print(f"  Sweden net K available: {min(sweden_net_k.keys())}–{max(sweden_net_k.keys())}")
print(f"  Sweden net K 1870: {sweden_net_k.get(1870, 'N/A'):.2f} mn SEK")

for idx, row in df[df['Country'] == 'Sweden'].iterrows():
    yr = row['Year']
    if yr in sweden_net_k:
        df.at[idx, 'net_capital_stock'] = sweden_net_k[yr]
```

```
Extracting Sweden net capital stock (Edvinsson 2016)...
  Sweden net K available: 1860–1920
  Sweden net K 1870: 956.77 mn SEK
```

✅ Productive net K = Col. 107 − Col. 101 (excludes residential buildings).

---

## Step 5 — France: Piketty-Zucman Perpetual Inventory Method (2014)

**Source:** `Data/France/France.xls` · Sheet `Table FR.12b` (Col. 8 GFCF/NI ratio; Col. 9 Dep/NI ratio) + Sheet `Table FR.1` (Col. 1 National Income, bn FF)
**Method:** PIM from 1820 baseline — accumulate net capital; apply resulting net/gross ratio to observed capital stock

```python
print("\nExtracting France net capital stock (Piketty-Zucman PIM, 2014)...")

wb_fr    = xlrd.open_workbook(DATA_FR / "France.xls")
ws_fr12b = wb_fr.sheet_by_name("Table FR.12b")
ws_fr1   = wb_fr.sheet_by_name("Table FR.1")

fr_gfcf_r, fr_dep_r, fr_ni = {}, {}, {}
for r in range(ws_fr12b.nrows):
    row = ws_fr12b.row_values(r)
    if isinstance(row[0], float) and 1820 <= row[0] <= 1913:
        yr = int(row[0])
        if row[8] != '': fr_gfcf_r[yr] = row[8]
        if row[9] != '': fr_dep_r[yr]  = row[9]

for r in range(ws_fr1.nrows):
    row = ws_fr1.row_values(r)
    if isinstance(row[0], float) and 1820 <= row[0] <= 1913:
        yr = int(row[0])
        if row[1] != '': fr_ni[yr] = row[1]

# PIM from 1820 (K=0 baseline)
k_gross_pz, k_net_pz = 0.0, 0.0
pz_net_gross_ratio = {}
for yr in range(1820, 1914):
    ni   = fr_ni.get(yr, 0)
    gfcf = fr_gfcf_r.get(yr, 0) * ni
    dep  = fr_dep_r.get(yr, 0)  * ni
    k_gross_pz += gfcf
    k_net_pz   += (gfcf - dep)
    if k_gross_pz > 0:
        pz_net_gross_ratio[yr] = max(0.0, k_net_pz / k_gross_pz)

print(f"  France PZ net/gross ratios: "
      f"1870={pz_net_gross_ratio.get(1870,0):.3f}, "
      f"1890={pz_net_gross_ratio.get(1890,0):.3f}, "
      f"1913={pz_net_gross_ratio.get(1913,0):.3f}")

for idx, row in df[df['Country'] == 'France'].iterrows():
    yr    = int(row['Year'])
    old_k = row['Fixed_capital_stock']
    ratio = pz_net_gross_ratio.get(yr)
    if ratio is not None and not np.isnan(old_k):
        df.at[idx, 'net_capital_stock'] = old_k * ratio
```

```
Extracting France net capital stock (Piketty-Zucman PIM, 2014)...
  France PZ net/gross ratios: 1870=0.518, 1890=0.509, 1913=0.493
```

✅ Net/gross ratio applied to observed capital stock. Declining ratio reflects depreciation of accumulated stock over time.

---

## Step 6 — Netherlands: Smits, Horlings & Van Zanden (2000) — Hardcoded

**Source:** Data hardcoded from PDF monograph: Table E.2 (GFCF by type) + Table F.1 (Depreciation)
**Method:** PIM from 1800 — productive GFCF (machinery + infrastructure, excluding dwellings) accumulated net of depreciation

```python
print("\nExtracting Netherlands net capital stock (Smits, Horlings & Van Zanden 2000)...")

# nld_gfcf: year -> (machinery+transport, residential_dwellings, infrastructure, total_gfcf)
# nld_dep:  year -> total depreciation
# (Full dictionaries: lines 192–251 of 01_build_data.py)

k_net_total, k_net_prod = 0.0, 0.0
nld_prod_ratio = {}

for yr in range(1800, 1914):
    data = nld_gfcf.get(yr)
    if data is None:
        continue
    mach, dwell, infra, total_gfcf = data
    dep       = nld_dep.get(yr, 0.0)
    prod_gfcf = mach + infra
    prod_dep  = dep * (prod_gfcf / total_gfcf) if total_gfcf > 0 else 0.0

    k_net_total += total_gfcf - dep
    k_net_prod  += prod_gfcf - prod_dep

    if k_net_total > 0 and yr >= 1860:
        nld_prod_ratio[yr] = max(0.0, min(1.0, k_net_prod / k_net_total))

print(f"  NLD productive/total net K ratio: "
      f"1870={nld_prod_ratio.get(1870,'N/A'):.3f}, "
      f"1890={nld_prod_ratio.get(1890,'N/A'):.3f}, "
      f"1913={nld_prod_ratio.get(1913,'N/A'):.3f}")

for idx, row in df[df['Country'] == 'Netherlands'].iterrows():
    yr    = row['Year']
    ratio = nld_prod_ratio.get(yr)
    if ratio is not None:
        df.at[idx, 'net_capital_stock'] = row['Fixed_capital_stock'] * ratio
```

```
Extracting Netherlands net capital stock (Smits, Horlings & Van Zanden 2000)...
  NLD productive/total net K ratio: 1870=0.534, 1890=0.563, 1913=0.603
```

✅ Matches manuscript prose exactly: *"By 1870, this ratio is 0.534 for the Netherlands, rising to 0.603 by 1913"* (Section 3.1).

---

## Step 7 — Spain: Prados de la Escosura (2022) — Hardcoded

**Source:** Data hardcoded from Table A1 — Net Capital Stock by type
**Method:** Productive K = Total − Dwellings; ratio applied to observed capital stock

```python
print("\nExtracting Spain net capital stock (Prados de la Escosura 2022)...")

# spain_nk: year -> (dwellings, other_construction, machinery, transport, total, cfc)
# (Full dictionary: lines 291–314 of 01_build_data.py)

spain_prod_ratio = {}
for yr, vals in spain_nk.items():
    dwell, other, mach, trans, total, cfc = vals
    prod = total - dwell
    if total > 0:
        spain_prod_ratio[yr] = prod / total

print(f"  Spain productive/total net K ratio: "
      f"1870={spain_prod_ratio.get(1870,'N/A'):.3f}, "
      f"1890={spain_prod_ratio.get(1890,'N/A'):.3f}, "
      f"1913={spain_prod_ratio.get(1913,'N/A'):.3f}")

for idx, row in df[df['Country'] == 'Spain'].iterrows():
    yr    = row['Year']
    ratio = spain_prod_ratio.get(yr)
    if ratio is not None:
        df.at[idx, 'net_capital_stock'] = row['Fixed_capital_stock'] * ratio
```

```
Extracting Spain net capital stock (Prados de la Escosura 2022)...
  Spain productive/total net K ratio: 1870=0.481, 1890=0.500, 1913=0.528
```

✅ Matches manuscript prose exactly: *"For Spain, the ratio runs from 0.481 (1870) to 0.528 (1913)"* (Section 3.1).

---

## Step 8 — USA: Duménil & Lévy (2013) — No Correction

**Source:** Already embedded in `Data/Common/1st_global.xlsx` (`Fixed_capital_stock` column)
**Method:** Net productive capital already — no transformation required

```python
mask_usa = df['Country'] == 'USA'
df.loc[mask_usa, 'net_capital_stock'] = df.loc[mask_usa, 'Fixed_capital_stock']
print("\nUSA — Duménil & Lévy (2013) already uses net productive K; no change.")
```

```
USA — Duménil & Lévy (2013) already uses net productive K; no change.
```

✅ Direct use of Duménil & Lévy net capital series.

---

## Step 9 — Compute Net Rate of Profit and Coverage Check

```python
print("\nComputing net rate of profit (rop_net = profit / net_capital_stock)...")
df['rop_net'] = df['profit_old'] / df['net_capital_stock']

print("\n=== Net RoP Coverage Check ===")
for country in ['Germany', 'UK', 'Sweden', 'France', 'Netherlands', 'Spain', 'USA']:
    sub      = df[df['Country'] == country]
    n_miss   = sub['rop_net'].isna().sum()
    n_total  = len(sub)
    print(f"  {country:<12}: {n_total - n_miss}/{n_total} obs with rop_net")
```

```
Computing net rate of profit (rop_net = profit / net_capital_stock)...

=== Net RoP Coverage Check ===
  Germany     : 44/44 obs with rop_net
  UK          : 44/44 obs with rop_net
  Sweden      : 44/44 obs with rop_net
  France      : 44/44 obs with rop_net
  Netherlands : 44/44 obs with rop_net
  Spain       : 44/44 obs with rop_net
  USA         : 44/44 obs with rop_net
```

✅ Zero missing values across all 7 countries.

---

## Step 10 — Summary Statistics and Save

```python
df_1870_1913 = df[(df['Year'] >= 1870) & (df['Year'] <= 1913)]
print("\n=== Summary Statistics for 1870–1913 panel ===")
print(f"  Net RoP:  N={df_1870_1913['rop_net'].count()}, "
      f"mean={df_1870_1913['rop_net'].mean():.3f}, "
      f"sd={df_1870_1913['rop_net'].std():.3f}, "
      f"min={df_1870_1913['rop_net'].min():.3f}, "
      f"max={df_1870_1913['rop_net'].max():.3f}")

output_path = DATA_COMMON / "1st_global_net_rop.xlsx"
df.to_excel(output_path, index=False)
print(f"\nSaved: {output_path}")
print("Key columns added: 'net_capital_stock', 'rop_net', 'profit_old'")
print("\nStep 1 complete. Run 02_run_regressions.py next.")
```

```
=== Summary Statistics for 1870–1913 panel ===
  Net RoP:  N=308, mean=0.242, sd=0.109, min=0.071, max=0.697

Saved: Data\Common\1st_global_net_rop.xlsx
Key columns added: 'net_capital_stock', 'rop_net', 'profit_old'

Step 1 complete. Run 02_run_regressions.py next.
```

### Verification against Manuscript Table 3 (`tab:summary_stats`)

| Statistic | Script | Manuscript | Match |
|-----------|--------|------------|-------|
| N         | 308    | 308        | ✅    |
| Mean      | 0.242  | 0.242      | ✅    |
| SD        | 0.109  | 0.109      | ✅    |
| Min       | 0.071  | 0.071      | ✅    |
| Max       | 0.697  | 0.697      | ✅    |
