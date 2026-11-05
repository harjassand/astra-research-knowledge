# A finite thermal-projection certificate for signed full-cycle turnover

The [complete theorem](package/next_science/root_construction/catalysis/THERMAL_PROJECTION_THEOREM.txt), [finite-algorithm/comparator completion](package/next_science/root_construction/catalysis/THERMAL_PROJECTION_COMPLETION.txt) and [general-gate coefficient construction](package/next_science/invention/FINITE_GATE_COEFFICIENT.md) connect stationary net turnover to actual gate relaxation and complete chemical response. Established Poisson, entropy/current and logarithmic-mean machinery is credited; novelty of this composition is unproved.

For a finite irreducible process `(chemical i, gate g)`, retain explicit bath-only gate transitions, all reverse chemical channels and signed product rewards. Thermally average each chemical row and reward at its conditional bath law to obtain Kbar,rbar, with stationary current `Jth`. Solve `Kbar h=Jth-rbar`. For binary gates with actual hot fraction p_i and thermal fraction p_i*, the exact identity is

```text
J-Jth=sum_i mu_i (p_i-p_i*) w_i,
w_i=r1(i)-r0(i)+(K1-K0)h(i).
```

The Poisson correction contains all later consequences, including trapping, depletion and reverse traffic. The thermal projection uses the same chemical rates averaged over the bath reference; it is **not automatically the capture-off or bare material**.

For bath down-rate gamma_i and thermal ratio q_i, resolved bath-link entropy plus Pinsker and Cauchy–Schwarz give

```text
|J-Jth|^2 <= sigma_total V_mu <= sigma_total Vmax,
V_mu=sum_i mu_i w_i^2/[4gamma_i(1+q_i)].
```

All parallel physical channels and work/heat reservoirs must be resolved. With one affinity A conjugate **exactly** to counted product current, `sigma_total=A J`, `Jth>0` and `kappa=A Vmax/Jth`, the gain obeys `(G-1)^2<=kappa G`. Multiple affinities require their full entropy sum; gross donor activity cannot be silently replaced by net product current. A sharper binary constant and exact-cost convex dual are supplied. Numerical dual evaluations are explicitly **not outward-rounded certificates**.

For a supplied finite bath generator B and centered corrected observable w, solve `Bf=w`. A constructive uniform general-gate constant is `C=.5 max_x sum_y b_xy(f_y-f_x)^2`, using the logarithmic mean and actual link entropy. Dense algebra costs `O(N^3+N m^3)` for N chemical states and at most m gate states per chemical state, plus aggregation. State count can be exponential; ill-conditioning, uncertainty and missing bath states remain costs. A driven auxiliary needs its work/affinity accounted, not a bath label by definition.

The [matched relay](README.md) has `J_on=Jth` with zero bath-link dissipation yet improves on its matched off system. The two-comparator corollary therefore separately bounds `J1/Jth1` and `J0/Jth0`, including any change in projected pathways and off-system slowdown. Neither bound identifies unknown material counterfactuals from bulk current alone.

Two independent constructors checked the source proof and its 72-state identities at 55 digits; exact rational topology witnesses and sharpness/positive-effect examples are retained. These are supplied mathematical/synthetic checks, not physical validation or formal interval certificates. [Recorded checks](package/next_science/root_construction/catalysis/thermal_projection_checks.json), [exact witness results](package/next_science/invention/projection_exact_witnesses_results.json), [variational results](package/next_science/root_construction/catalysis/variational_gate_bound_results.json). An asymptotically sharp absolute example is a slowdown, not a positive enhancement; positive rational examples are separately named in the source. No new Capital execution or audit occurred. [Original package and attribution](SOURCES.json).
