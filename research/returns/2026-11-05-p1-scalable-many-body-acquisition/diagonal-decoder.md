# Exact acquired decoder for known diagonal interactions

This independent result supplies an ideal output-only decoder for **every `r>0`** when the known local Hamiltonian is diagonal in one fixed product basis. Read the [complete standalone proof](package/construction/diagonal_hamiltonian_exact_acquired_decoder.txt), [integrated report](package/Astra_P1_Scalable_Many_Body_Acquisition.pdf), and [completed interface audit](package/construction/continuous_hamiltonian_interface_audit.txt). It uses the [specified pure coherent Weyl ports and acquired reset/export instrument](README.md), with all finite collection, receiver controls, storage and precision costs retained.

At each reset, the old quantum state is coherently exported into `B`. Measuring the purifier `A` in the known diagonal basis reveals the independently uniform replacement basis state of the source. Keep only each site's first export and process all later replacement labels. A reset site stays in a known basis state under diagonal interactions, so it can impose a known phase on unreset quantum sites without becoming a new quantum carrier.

For initial basis string `x`, let `z_i(t;x)` equal `x_i` before the site's first reset and its recorded replacement label afterwards. Once all sites have reset, the retained payload is exactly

```text
|x> -> exp(-i f_gamma(x)) |x>,
f_gamma(x)=integral sum_X h_X(t;z_X(t;x)) dt.
```

The surviving source and discarded exports have no remaining input dependence. Accumulate an at-most-`k`-local diagonal table `F_X,gamma(x_X)` for each term and apply `product_X exp(i F_X,gamma(B_X))`. These gates commute. The inverse recovers all superpositions and external-reference correlations exactly on completed ideal records. There is one fixed-dimensional correction gate per Hamiltonian term, rather than a global dense correction.

For `m` local terms of maximum degree `D` and `M` reset flags, classical integration/table work is `O(q^k[m+DM])` with `O(m q^k)` stored finite-precision numbers. Streaming retains `n` first-export payload qudits and `O(n)` collector workspace; later exports and the complete classical history need not be stored. Time dependence requires an efficiently integrable supplied local description. Interaction strength still affects timing, phase precision and finite controls.

Independent rate-`r` clocks, or the matching binned instrument, give `Pr[some site unreset by T] <= n exp(-rT)`. Hence `T=log(2n/epsilon)/r` gives unconditional ideal **full diamond** error at most `epsilon`, with exactly `n` retained payload qudits. Success branches are exact in the ideal instrument. Finite physical conditional guarantees must also account for implementation error divided by a lower bound on actual success probability; they are not obtained free from an unconditional error bound.

Every `nK` local interface execution, finite endpoint/readout/refresh deadline, loss, calibration, memory waiting, routing, precision and phase correction remains paid in the [finite-interface construction](finite-interface.md). A postprocessed earlier stopping prefix does not retroactively reduce collection latency. Fixed unavailable noise or fixed collection loss is not shown harmless at large `n`.

The result proves that the general theorem's `r>beta` condition is sufficient rather than a universal threshold. It does not solve general noncommuting weak-export Hamiltonians, unknown-Hamiltonian acquisition, whole mixed-bath compression or microscopic fixed-bandwidth implementation. No separate new numerical execution, hardware validation or historical-priority finding is claimed by this publication. [Original package and provenance](SOURCES.json).
