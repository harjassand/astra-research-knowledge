# Residual targeting does not repair the current beta3 triplet span

The bounded preview is complete. The accepted first connected increment was
left unchanged, and no new exact/cyclotomic thermal acquisition was launched.

For the existing16-dimensional triplet message span, residual minimization
at prescribed shifts294000--315000 lowers variance only from
5.238235387e9 to4.728672181e9, a factor1.108. The best-variance candidate is
at the lower shift boundary294000, with actual Rayleigh292531.83. Its lower
Rayleigh value reduces the useful separation from the deflated count.

The combined triplet upper remains328912.54, above the scalar lower322705.85.
The all-mode relative-loop-tail proposal remains393.70. No next connected
thermal input is acquired.

| Relative Gram cutoff | Retained rank | Gram condition | Best variance |
| ---: | ---: | ---: | ---: |
| 1e-6 | 13 | 3.68e4 | 4.81114e9 |
| 1e-8 | 15 | 4.73e7 | 4.73778e9 |
| 1e-10 | 16 | 3.97e9 | 4.72867e9 |
| 1e-12 | 16 | 3.97e9 | 4.72867e9 |

An additional exact Fraction LDL check treats the saved binary64 matrix
entries as exact dyadic data. It proves, for those finite forms,

    G>0, H<294200G,
    M2-588000H+294000^2 G > 4.7e9 G.

Every vector in that frozen numerical span with Rayleigh at least291900
therefore has variance above4.69559e9. Even the more favourable rest bound
291900 permits at most6.55638e7 for a Temple upper below322706, or2.10312e7
for one below303344. Thus optimizer or shift choice cannot fix these stored
forms. This exact finite-form statement does not certify the physical source
correlations, for which verified entrywise enclosures were not acquired.

The complete preview, including rebuilding full G/H/M2 from all physical
sectors of inhomogeneous open2--6 chains, took3.81s on one thread. The exact
finite-form/candidate replay took.046s. Conditioning, candidate amplification and all
assigned/unassigned transfer modes are charged in `PROOF.md` and the JSON.

Files:

- `results/minres_scan.json`: all shifts, candidates, cutoffs and loop counts.
- `results/triplet_matrices_beta3.npz`: raw and normalized G/H/M2.
- `results/dyadic_span_replay.json`: exact finite-form witness and boundaries.
- `code/minimize_residual.py`, `code/verify_dyadic_span.py`: replay sources.

The current result supports ending this bounded attack. It is not a no-go
for deeper or different message families, another transfer representation,
ordinary thermal methods, the next rung, or the spin-two gap.
