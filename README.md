# An Unequal Equalization

**Understanding the Response of Rates of Profit during the First Age of Globalization (1870--1913)**

*Kabeer Bora*

Under review at *Review of Social Economy*

---

## Overview

This paper examines how trade integration influenced the rate of profit in seven capitalist economies (UK, USA, Germany, France, Netherlands, Sweden, Spain) during the First Age of Globalization (1870-1913), from a Marxian perspective.

**Main finding:** A 1% increase in trade openness raised the net rate of profit by approximately 0.30-0.33 percentage points, operating primarily through the export channel (surplus realization on global markets). We also document beta-convergence of profit rates across countries, with a half-life of 25-36 years.

## Repository Structure

```
.
├── sample_revised.tex            # Manuscript (LaTeX, compile with XeLaTeX)
├── references.bib                # Bibliography
├── presentation.tex              # Beamer slide deck (17 slides)
├── Replication/                  # Full replication package
│   ├── README.md                 # Replication instructions
│   ├── 01_build_data.py          # Step 1: Construct net rate of profit dataset
│   ├── 02_run_regressions.py     # Step 2: Run all regressions (produces all tables)
│   ├── data_construction.md      # Documentation for data construction
│   ├── regressions.md            # Documentation for regression specifications
│   └── Data/                     # Raw and intermediate data files
│       ├── Common/               # Shared datasets (trade, gravity, population)
│       ├── France/               # Country-specific capital stock data
│       ├── Germany/
│       ├── Netherlands/
│       ├── Spain/
│       ├── Sweden/
│       ├── UK/
│       └── USA/
└── images_plots/                 # Figures used in manuscript and slides
```

## Replication

**Requirements:** Python 3.9+ with pandas, numpy, openpyxl, xlrd, linearmodels, statsmodels, pyfixest, scipy, pyreadstat.

```bash
cd Replication
python 01_build_data.py       # Constructs net RoP dataset from raw capital stock data
python 02_run_regressions.py  # Runs all regressions, prints all manuscript tables
```

The replication package is also available on [OSF](https://osf.io/pv8ak/?view_only=d4f0acf2e34a4ccbba72e5ea95d2aeb6).

## Identification Strategy

Two independent instrumental variable strategies are employed:

1. **Climate uncertainty instrument:** Temperature uncertainty in trading partner countries, interacted with time-invariant maritime distance and colonial ties, predicts trade openness via a PPML gravity model. First-stage F > 50.

2. **Pascali (2017) instrument:** The differential spread of steamship technology across bilateral trade routes generates exogenous variation in predicted trade. First-stage F > 10.

The two instruments exploit entirely different sources of variation (demand-side annual weather shocks vs. supply-side secular technology adoption) and yield consistent estimates.

## Key Results

| Specification | Coefficient on Openness | SE |
|---|---|---|
| IV Climate (bare) | 0.325*** | (0.062) |
| IV Climate (full) | 0.317*** | (0.064) |
| IV Pascali (bare) | 0.311*** | (0.072) |
| IV Pascali (full) | 0.296** | (0.094) |

- Export channel (instrumented): 0.302\*\*\*-0.350\*\* (significant)
- Import channel (instrumented): 0.157-0.191 (insignificant)
- Leave-one-out: all 7 subsamples positive (range 0.227-0.429)

## Citation

```bibtex
@article{bora2026unequal,
  title={An Unequal Equalization: Understanding the Response of Rates of Profit during the First Age of Globalization (1870--1913)},
  author={Bora, Kabeer},
  journal={Review of Social Economy},
  year={2026},
  note={Under review}
}
```
