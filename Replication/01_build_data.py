"""
Step 1: Build net rate of profit dataset for 1st globalization paper.

Constructs net productive capital stock for each of the 7 countries by
applying country-specific corrections to raw capital stock data, then
computes the net rate of profit (rop_net = profit / net_capital_stock).

Output: Data/Common/1st_global_net_rop.xlsx

Run from the Replication/ directory:
    python 01_build_data.py
"""

import xlrd
import openpyxl
import pandas as pd
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Paths (all relative to Replication/ directory)
# ─────────────────────────────────────────────────────────────────────────────
DATA_COMMON  = Path("Data/Common")
DATA_DE      = Path("Data/Germany")
DATA_UK      = Path("Data/UK")
DATA_SE      = Path("Data/Sweden")
DATA_FR      = Path("Data/France")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Load original dataset
# ─────────────────────────────────────────────────────────────────────────────
print("Loading original dataset...")
df = pd.read_excel(DATA_COMMON / "1st_global.xlsx")
print(f"Original data: {df.shape[0]} rows, countries: {df['Country'].unique().tolist()}")

df['rop'] = pd.to_numeric(df['rop'], errors='coerce')
df['Fixed_capital_stock'] = pd.to_numeric(df['Fixed_capital_stock'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype(int)

df['profit_old'] = df['rop'] * df['Fixed_capital_stock']
df['net_capital_stock'] = np.nan
df['rop_net'] = np.nan

# ─────────────────────────────────────────────────────────────────────────────
# 2. GERMANY — Piketty-Zucman DataDE1c
#    Net K = AgriFixed (col74) + BusinessAssets (col75)
#    Source: Data/Germany/Germany.xls
#    See Data/Germany/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
print("\nExtracting Germany net capital stock (Piketty-Zucman 2014)...")

wb_de = xlrd.open_workbook(DATA_DE / "Germany.xls")
ws_de = wb_de.sheet_by_name("DataDE1c")

germany_net_k = {}
for r in range(ws_de.nrows):
    row = ws_de.row_values(r)
    if isinstance(row[0], float) and 1860 <= row[0] <= 1920:
        yr = int(row[0])
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

# ─────────────────────────────────────────────────────────────────────────────
# 3. UK — Bank of England A55: NonDwellings market sector (col index 4)
#    Source: Data/UK/a-millennium-of-macroeconomic-data-for-the-uk.xlsx
#    See Data/UK/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
print("\nExtracting UK net capital stock (Bank of England 2023, Feinstein & Pollard)...")

wb_uk = openpyxl.load_workbook(
    DATA_UK / "a-millennium-of-macroeconomic-data-for-the-uk.xlsx",
    read_only=True, data_only=True
)
ws_uk = wb_uk["A55. Capital Stock"]

uk_net_k = {}
for row in ws_uk.iter_rows(min_row=7, values_only=True):
    if row[0] is not None and isinstance(row[0], (int, float)) and 1860 <= row[0] <= 1920:
        yr = int(row[0])
        val = row[4]  # NonDwellings market sector, £mn, net
        if val is not None:
            uk_net_k[yr] = val

print(f"  UK net K available: {min(uk_net_k.keys())}–{max(uk_net_k.keys())}")
print(f"  UK net K 1870: {uk_net_k.get(1870, 'N/A')} £mn")

for idx, row in df[df['Country'] == 'UK'].iterrows():
    yr = row['Year']
    if yr in uk_net_k:
        df.at[idx, 'net_capital_stock'] = uk_net_k[yr]

# ─────────────────────────────────────────────────────────────────────────────
# 4. SWEDEN — Edvinsson (2016): Net K = Col.107 − Col.101
#    Source: Data/Sweden/tablesAtoX.xls
#    See Data/Sweden/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
print("\nExtracting Sweden net capital stock (Edvinsson 2016)...")

wb_se = xlrd.open_workbook(DATA_SE / "tablesAtoX.xls")
ws_se = wb_se.sheet_by_name("Data")

sweden_net_k = {}
for r in range(ws_se.nrows):
    row = ws_se.row_values(r)
    if row[99] != '' and isinstance(row[99], float) and 1860 <= row[99] <= 1920:
        yr = int(row[99])
        priv_total  = row[106] if row[106] != '' else np.nan  # Col.107: Private net total
        residential = row[100] if row[100] != '' else np.nan  # Col.101: Residential buildings
        if not np.isnan(priv_total) and not np.isnan(residential):
            sweden_net_k[yr] = priv_total - residential

print(f"  Sweden net K available: {min(sweden_net_k.keys())}–{max(sweden_net_k.keys())}")
print(f"  Sweden net K 1870: {sweden_net_k.get(1870, 'N/A'):.2f} mn SEK")

for idx, row in df[df['Country'] == 'Sweden'].iterrows():
    yr = row['Year']
    if yr in sweden_net_k:
        df.at[idx, 'net_capital_stock'] = sweden_net_k[yr]

# ─────────────────────────────────────────────────────────────────────────────
# 5. FRANCE — Piketty-Zucman PIM depreciation ratio applied to original K
#    Source: Data/France/France.xls
#    See Data/France/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
print("\nExtracting France net capital stock (Piketty-Zucman PIM, 2014)...")

wb_fr = xlrd.open_workbook(DATA_FR / "France.xls")

# Table FR.12b: GFCF/NI (col8) and Dep/NI (col9)
ws_fr12b = wb_fr.sheet_by_name("Table FR.12b")
fr_gfcf_r = {}
fr_dep_r  = {}
for r in range(ws_fr12b.nrows):
    row = ws_fr12b.row_values(r)
    if isinstance(row[0], float) and 1820 <= row[0] <= 1913:
        yr = int(row[0])
        if row[8] != '': fr_gfcf_r[yr] = row[8]
        if row[9] != '': fr_dep_r[yr]  = row[9]

# Table FR.1: NI absolute values (col1, billion FF)
ws_fr1 = wb_fr.sheet_by_name("Table FR.1")
fr_ni = {}
for r in range(ws_fr1.nrows):
    row = ws_fr1.row_values(r)
    if isinstance(row[0], float) and 1820 <= row[0] <= 1913:
        yr = int(row[0])
        if row[1] != '': fr_ni[yr] = row[1]

# Run PIM from 1820 (K=0 baseline)
k_gross_pz = 0.0
k_net_pz   = 0.0
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
    yr = int(row['Year'])
    old_k = row['Fixed_capital_stock']
    ratio = pz_net_gross_ratio.get(yr)
    if ratio is not None and not np.isnan(old_k):
        df.at[idx, 'net_capital_stock'] = old_k * ratio

# ─────────────────────────────────────────────────────────────────────────────
# 6. NETHERLANDS — Smits, Horlings & Van Zanden (2000), hardcoded
#    Source: See Data/Netherlands/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
print("\nExtracting Netherlands net capital stock (Smits, Horlings & Van Zanden 2000)...")

# Table E.2: GFCF by type (million guilders, current prices), 1800–1913
# Format: year -> (machinery+transport, residential_dwellings, infrastructure+other, total_gfcf)
nld_gfcf = {
    1800:(6.2,18.8,7.6,32.6),  1801:(6.1,19.8,8.3,34.1),  1802:(5.1,17.5,7.4,30.0),
    1803:(4.7,19.3,8.4,32.4),  1804:(4.4,21.0,10.2,35.6), 1805:(5.1,21.0,9.6,35.7),
    1806:(5.0,21.0,9.5,35.5),  1807:(4.4,21.6,10.4,36.3), 1808:(5.2,22.0,10.2,37.4),
    1809:(4.7,20.8,13.6,39.1), 1810:(4.5,19.6,8.6,32.6),  1811:(3.7,19.1,9.1,31.8),
    1812:(3.7,18.6,8.2,30.6),  1813:(3.6,18.0,8.0,29.6),  1814:(6.4,17.1,7.3,30.8),
    1815:(6.3,17.1,7.5,30.9),  1816:(5.7,16.8,9.7,32.2),  1817:(7.3,18.3,10.9,36.4),
    1818:(8.4,19.8,10.2,38.4), 1819:(7.8,18.6,10.1,36.5), 1820:(7.8,18.2,12.1,38.1),
    1821:(7.3,17.5,9.9,34.7),  1822:(7.2,17.4,11.1,35.7), 1823:(7.5,18.0,11.1,36.6),
    1824:(8.2,18.2,11.3,37.6), 1825:(7.6,20.9,9.5,38.1),  1826:(7.2,20.5,11.3,39.0),
    1827:(7.7,19.7,10.0,37.4), 1828:(7.3,19.8,8.6,35.7),  1829:(7.9,20.0,9.0,36.8),
    1830:(8.3,19.9,8.7,37.0),  1831:(7.4,19.7,8.9,36.0),  1832:(7.9,19.6,9.5,37.1),
    1833:(8.3,18.9,8.3,35.5),  1834:(8.8,19.5,9.8,38.1),  1835:(11.6,20.7,9.7,41.9),
    1836:(13.1,22.5,10.5,46.1),1837:(14.3,22.8,8.8,45.9), 1838:(14.6,22.5,10.6,47.7),
    1839:(15.6,22.3,9.4,47.3), 1840:(13.5,21.6,13.8,48.9),1841:(12.2,23.3,11.2,46.7),
    1842:(9.9,19.7,10.7,40.3), 1843:(9.4,18.7,12.8,40.9), 1844:(8.4,20.3,12.0,40.6),
    1845:(10.1,22.6,13.0,45.7),1846:(11.0,22.1,11.4,44.4),1847:(11.4,23.1,14.5,49.0),
    1848:(11.3,20.7,10.2,42.2),1849:(11.3,20.7,9.2,41.2), 1850:(10.9,21.2,9.4,41.5),
    1851:(11.9,20.4,8.8,41.1), 1852:(13.9,21.4,25.0,60.3),1853:(19.1,21.6,15.6,56.3),
    1854:(21.1,21.4,16.3,58.8),1855:(20.2,21.9,15.1,57.3),1856:(22.2,22.6,15.9,60.7),
    1857:(21.5,21.7,13.6,56.8),1858:(16.0,22.7,15.6,54.3),1859:(14.9,22.8,15.3,53.0),
    1860:(13.4,24.0,21.0,58.4),1861:(14.3,26.1,19.5,59.9),1862:(17.8,26.1,20.3,64.3),
    1863:(16.6,26.5,24.3,67.4),1864:(18.7,27.7,26.7,73.1),1865:(18.9,28.2,30.9,77.9),
    1866:(20.5,27.0,34.7,82.2),1867:(18.4,27.0,33.6,78.9),1868:(15.4,28.5,32.0,75.9),
    1869:(16.0,31.2,34.0,81.2),1870:(17.1,30.9,39.6,87.7),1871:(19.0,34.4,32.9,86.3),
    1872:(24.2,36.9,44.7,105.8),1873:(33.7,32.2,39.5,105.4),1874:(29.2,32.1,38.3,99.6),
    1875:(23.1,41.6,39.1,103.8),1876:(27.3,45.8,42.4,115.6),1877:(27.2,50.7,56.7,134.5),
    1878:(24.1,41.9,46.2,112.1),1879:(27.4,53.4,45.7,126.5),1880:(26.9,51.5,46.1,124.5),
    1881:(26.3,56.8,54.0,137.1),1882:(34.9,57.9,42.0,134.8),1883:(45.1,57.6,47.1,149.8),
    1884:(38.6,52.4,48.5,139.6),1885:(28.4,54.2,45.9,128.5),1886:(28.1,61.4,49.4,138.9),
    1887:(24.4,55.4,43.7,123.5),1888:(29.8,70.0,46.4,146.2),1889:(33.3,60.7,37.9,131.9),
    1890:(42.7,61.8,47.9,152.4),1891:(50.1,58.9,48.0,157.0),1892:(40.9,59.0,48.0,147.9),
    1893:(33.1,58.0,43.3,134.3),1894:(34.4,59.1,45.0,138.5),1895:(36.0,58.9,47.1,142.0),
    1896:(43.0,64.6,47.9,155.5),1897:(47.1,68.1,48.9,164.1),1898:(51.1,63.3,50.1,164.5),
    1899:(78.0,72.8,53.5,204.3),1900:(78.0,78.2,61.0,217.2),1901:(84.4,76.0,61.2,221.7),
    1902:(70.7,79.5,64.2,214.4),1903:(72.4,88.0,71.5,231.9),1904:(66.1,90.3,74.5,230.8),
    1905:(70.8,89.4,75.6,235.8),1906:(89.3,95.5,86.1,270.8),1907:(106.9,78.1,76.2,261.2),
    1908:(97.1,81.1,78.7,256.9),1909:(91.2,91.2,74.9,257.3),1910:(90.1,100.5,84.7,275.3),
    1911:(101.7,104.8,84.9,291.4),1912:(139.9,112.3,91.6,343.8),1913:(182.9,124.1,112.9,419.8),
}

# Table F.1: Depreciation (million guilders, current prices), 1807–1913
nld_dep = {
    1807:31.6,1808:32.9,1809:35.3,1810:34.1,1811:31.9,1812:31.6,1813:30.5,
    1814:29.3,1815:26.9,1816:25.1,1817:26.4,1818:28.3,1819:28.8,1820:28.5,
    1821:27.7,1822:27.2,1823:26.7,1824:26.9,1825:29.5,1826:30.5,1827:28.9,
    1828:28.1,1829:27.1,1830:26.7,1831:25.3,1832:25.2,1833:25.0,1834:26.6,
    1835:27.8,1836:28.3,1837:31.8,1838:31.2,1839:31.1,1840:31.1,1841:31.5,
    1842:30.7,1843:29.0,1844:28.8,1845:31.2,1846:34.1,1847:35.3,1848:35.1,
    1849:32.8,1850:30.9,1851:30.8,1852:33.1,1853:37.7,1854:41.2,1855:42.5,
    1856:41.2,1857:42.5,1858:40.0,1859:37.4,1860:37.9,1861:39.9,1862:40.9,
    1863:43.4,1864:45.8,1865:43.6,1866:43.3,1867:44.0,1868:44.6,1869:45.2,
    1870:48.0,1871:47.2,1872:54.3,1873:73.0,1874:80.3,1875:65.6,1876:64.7,
    1877:64.9,1878:63.8,1879:63.6,1880:66.5,1881:68.3,1882:67.6,1883:68.5,
    1884:69.7,1885:70.3,1886:70.0,1887:71.2,1888:74.6,1889:77.7,1890:83.2,
    1891:92.1,1892:90.4,1893:86.0,1894:85.0,1895:88.6,1896:96.5,1897:107.7,
    1898:109.8,1899:114.7,1900:121.5,1901:122.7,1902:119.3,1903:126.5,1904:129.1,
    1905:129.5,1906:139.9,1907:148.2,1908:155.6,1909:153.1,1910:156.1,
    1911:165.5,1912:177.3,1913:199.2,
}

k_net_total = 0.0
k_net_prod  = 0.0
nld_prod_ratio = {}

for yr in range(1800, 1914):
    data = nld_gfcf.get(yr)
    if data is None:
        continue
    mach, dwell, infra, total_gfcf = data
    dep = nld_dep.get(yr, 0.0)
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
    yr = row['Year']
    ratio = nld_prod_ratio.get(yr)
    if ratio is not None:
        df.at[idx, 'net_capital_stock'] = row['Fixed_capital_stock'] * ratio

# ─────────────────────────────────────────────────────────────────────────────
# 7. SPAIN — Prados de la Escosura (2022), hardcoded
#    Source: See Data/Spain/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
print("\nExtracting Spain net capital stock (Prados de la Escosura 2022)...")

# Table A1: Net Capital Stock by type (million current euros), 1850–2019
# Format: year -> (dwellings, other_construction, machinery, transport, total, cfc)
spain_nk = {
    1850:(24,15,0,1,40,0.9),  1851:(23,15,0,1,40,0.9),  1852:(24,15,0,1,40,0.9),
    1853:(24,15,0,1,40,0.9),  1854:(23,15,1,1,40,0.9),  1855:(23,14,1,1,39,0.9),
    1856:(23,14,1,1,39,0.9),  1857:(23,14,1,1,40,0.9),  1858:(23,15,1,2,41,1.0),
    1859:(24,15,1,2,42,1.1),  1860:(25,16,1,2,44,1.1),  1861:(26,17,1,2,46,1.2),
    1862:(27,18,1,3,48,1.2),  1863:(27,19,1,3,50,1.3),  1864:(28,19,1,3,51,1.4),
    1865:(28,20,1,3,53,1.4),  1866:(28,20,1,4,53,1.5),  1867:(28,20,1,4,54,1.5),
    1868:(28,21,1,4,55,1.6),  1869:(28,21,1,4,54,1.5),  1870:(28,21,1,4,54,1.5),
    1871:(28,21,1,4,55,1.5),  1872:(29,21,1,4,55,1.5),  1873:(29,22,1,4,56,1.5),
    1874:(29,22,1,4,56,1.5),  1875:(30,22,1,3,56,1.5),  1876:(30,22,1,3,56,1.5),
    1877:(30,22,1,3,57,1.5),  1878:(30,22,1,3,57,1.5),  1879:(30,22,1,4,57,1.6),
    1880:(30,22,2,4,58,1.6),  1881:(30,22,2,4,58,1.6),  1882:(30,22,2,4,58,1.6),
    1883:(30,22,2,4,59,1.7),  1884:(31,23,2,5,60,1.8),  1885:(31,23,2,5,60,1.8),
    1886:(31,23,2,5,60,1.8),  1887:(31,23,2,5,60,1.8),  1888:(31,23,2,4,60,1.8),
    1889:(31,23,2,4,61,1.8),  1890:(31,24,3,4,62,1.8),  1891:(32,24,3,4,63,1.8),
    1892:(33,25,3,4,64,1.9),  1893:(33,26,3,4,66,1.9),  1894:(34,27,3,3,68,1.9),
    1895:(35,27,3,3,70,2.0),  1896:(36,28,4,3,72,2.0),  1897:(37,29,4,3,74,2.1),
    1898:(38,30,4,3,76,2.1),  1899:(40,31,4,4,79,2.3),  1900:(41,33,5,5,84,2.5),
    1901:(43,34,5,6,88,2.7),  1902:(44,35,5,6,90,2.8),  1903:(45,36,6,6,92,2.8),
    1904:(46,37,6,5,95,2.9),  1905:(48,38,6,5,97,2.9),  1906:(49,39,6,5,99,3.0),
    1907:(50,40,7,5,102,3.1), 1908:(51,41,7,5,105,3.2), 1909:(53,43,8,5,109,3.3),
    1910:(56,45,8,5,114,3.5), 1911:(59,49,9,6,121,3.7), 1912:(62,53,9,6,130,4.0),
    1913:(67,57,11,7,142,4.4),
}

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
    yr = row['Year']
    ratio = spain_prod_ratio.get(yr)
    if ratio is not None:
        df.at[idx, 'net_capital_stock'] = row['Fixed_capital_stock'] * ratio

# ─────────────────────────────────────────────────────────────────────────────
# 8. USA — Duménil & Lévy (2013): already net productive K, no change
#    Source: See Data/USA/SOURCE.md
# ─────────────────────────────────────────────────────────────────────────────
mask_usa = df['Country'] == 'USA'
df.loc[mask_usa, 'net_capital_stock'] = df.loc[mask_usa, 'Fixed_capital_stock']
print("\nUSA — Duménil & Lévy (2013) already uses net productive K; no change.")

# ─────────────────────────────────────────────────────────────────────────────
# 9. Compute net rate of profit
# ─────────────────────────────────────────────────────────────────────────────
print("\nComputing net rate of profit (rop_net = profit / net_capital_stock)...")
df['rop_net'] = df['profit_old'] / df['net_capital_stock']

# ─────────────────────────────────────────────────────────────────────────────
# 10. Verify coverage
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== Net RoP Coverage Check ===")
for country in ['Germany', 'UK', 'Sweden', 'France', 'Netherlands', 'Spain', 'USA']:
    sub = df[df['Country'] == country]
    n_missing = sub['rop_net'].isna().sum()
    n_total   = len(sub)
    print(f"  {country:<12}: {n_total - n_missing}/{n_total} obs with rop_net")

# ─────────────────────────────────────────────────────────────────────────────
# 11. Summary statistics (should match Table 3 in manuscript)
# ─────────────────────────────────────────────────────────────────────────────
df_1870_1913 = df[(df['Year'] >= 1870) & (df['Year'] <= 1913)]
print("\n=== Summary Statistics for 1870–1913 panel ===")
print(f"  Net RoP:  N={df_1870_1913['rop_net'].count()}, "
      f"mean={df_1870_1913['rop_net'].mean():.3f}, "
      f"sd={df_1870_1913['rop_net'].std():.3f}, "
      f"min={df_1870_1913['rop_net'].min():.3f}, "
      f"max={df_1870_1913['rop_net'].max():.3f}")
# (Manuscript: N=308, mean=0.242, SD=0.109, min=0.071, max=0.697)

# ─────────────────────────────────────────────────────────────────────────────
# 12. Save
# ─────────────────────────────────────────────────────────────────────────────
output_path = DATA_COMMON / "1st_global_net_rop.xlsx"
df.to_excel(output_path, index=False)
print(f"\nSaved: {output_path}")
print("Key columns added: 'net_capital_stock', 'rop_net', 'profit_old'")
print("\nStep 1 complete. Run 02_run_regressions.py next.")
