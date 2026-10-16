# Data and Code for "Beating the Break-Even Point with Autonomous Quantum Error Correction"

## Overview

This directory contains the **final plotted data** and simulation code accompanying the manuscript. All CSV files in `source_data/` provide the exact data points, error bars, fit parameters, and fitted curves as they appear in the published figures — no additional processing is required.

## Repository Structure

```
QEC data/
├── README.md
├── source_data/
│   ├── Fig2b_chi_matrix.csv           # Fig 2b: Chi matrix (real parts + bootstrap errors)
│   ├── Fig2c_source.csv               # Fig 2c: Population vs phase rotation
│   ├── Fig3d_source.csv               # Fig 3d: Population dynamics
│   ├── Fig3e_chi_matrix.csv           # Fig 3e: Chi matrix (error space |0_E>)
│   ├── Fig3f_chi_matrix.csv           # Fig 3f: Chi matrix (logical space |0_L>)
│   ├── Fig4a_source.csv               # Fig 4a: Fidelity vs time (ambient) + fit
│   ├── Fig4a_inset_source.csv         # Fig 4a inset: 15 phy/QEC fidelity pairs
│   ├── Fig4b_source.csv               # Fig 4b: Fidelity vs time (injected noise) + fit
│   ├── EDFig4a_source.csv             # ED Fig 4a: Unnormalized fidelity vs time + fit
│   ├── EDFig4a_inset_source.csv       # ED Fig 4a inset: Unnormalized 15-pair scatter
│   └── EDFig4b_source.csv             # ED Fig 4b: Unnormalized fidelity (injected) + fit
│
└── Extended_data_Fig6.py              # ED Fig 6: Numerical simulation code
```

## Data Format

Lines beginning with `#` are comments. The first non-comment row contains column headers, followed by data rows.

### Figure 4 / Extended Data Figure 4 CSVs
Each file has three sections separated by blank rows:
1. **Data points** — storage time (ms), QEC cycles, fidelity $F_{\chi}$ ± bootstrap s.d.
2. **Fit parameters** — Stretched exponential $a + c \cdot \exp(-(t/\tau)^2)$ parameters with standard errors.
3. **Fitted curves** — Fine-grid evaluation of fits with error bands clipped to $[0,1]$.

### Figure 2 / 3 CSVs
- **Chi matrices** — 16 elements in II, IX, ..., ZZ Pauli basis (row-major), real part ± bootstrap s.d.
- **Fig 2c** — Population vs phase $\phi/\pi$ for $|\pm_L\rangle$, $|\pm_E\rangle$ with binomial errors.
- **Fig 3d** — Population vs time ($\mu$s) for both initial states, with logical/error/phonon populations.

### Insets
15 interleaved (physical, QEC) fidelity pairs at 9 QEC cycles ($t = 29$ ms).


## Extended Data Figure 6

`Extended_data_Fig6.py` contains the numerical simulation code that models QEC performance under injected noise, producing the theoretical curves shown in Extended Data Fig 6.

Run with:
```bash
python Extended_data_Fig6.py
```



