# Cycle11 bounded contribution: full moments and the rare-sector obstruction

This contribution reads the actual Cycle10 `FULL_HAMMING_RESPONSE.tex` and governing bulk definitions in `QUADRATIC_CAPACITY_FLOOR.tex`. It does not rerun any predecessor suite.

## Complete results

`MOMENT_COMPARISON_AND_RARE_SECTOR.tex` proves a color-fiber-correct closed-walk trace/exponential comparison, valid for every analytic prefix density. It then proves that the absolute scalar majorant already has a divergent pressure at fixed `r=bk>0`, using only its distance-four Perron contribution.

A stronger abstract counterexample obeys all inherited pattern-block norm bounds, the conditional row-square estimate, charge preservation, zero pattern diagonal and even the physical compressed-output-charge spectral interval. Nevertheless its target logarithmic moment diverges at fixed small `r`. The active coherent subspace uses only `L=Theta_r(k^(3/4))` positions, so its negative eigenvalue has linear magnitude while the reference spectral weight is only `exp(-o(k))`.

**This operator is not claimed to be the physical `K_zeta`.** Its use is to exclude a proof based only on these inherited bounds. Actual signed unitary histories or a suitable analytic prefix must supply additional information. The theorem neither excludes the desired physical prefix bound nor proves a capacity converse.

## Executable diagnostic

Run `python3 -I counterexample_check.py` in this directory. The script checks the trace/color-fiber counting on a genuinely finite graph and the large-parameter inequalities using exact integer/rational formulas. Large matrices are never constructed; these are formula checks, not a simulation of the recurrent device. The saved JSON identifies exact inputs and measured script-body time. Discovery, inference and review costs remain unknown.

## Receiving interface

The comparison lemma works for rectangular color fibers and arbitrary pattern-diagonal reference weights, retaining the weights explicitly. Uniform binary-pattern mass `2^-k` is used only in the final normalized scalar trace. The false inference retired here is that a conditional second moment plus bounded physical displacement suffices for the exponential moment. The rare-sector construction is a load-bearing counterexample to that omission.

No private delivery, source replacement, external outreach or other programme work was performed by this contributor.
