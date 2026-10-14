# Correction delta 001: passive-shunt energy accounting

**Status:** append-only correction created after the original owned-file manifest was frozen. The frozen `PROOF.md` and `MANIFEST.json` are preserved byte-for-byte; that manifest is a snapshot of the original packet and does not include this later delta. This delta supersedes the energy-accounting sentence at `PROOF.md:303` and clarifies the interpretation of the hydraulic-work ledger at `PROOF.md:298`.

## Cold recheck

The supplied physical source, `work/FJ-sources/physical_PASTED_SOURCE.txt:53–84`, defines positive `p_i Q_i + V_i I_i` as power entering each wet transducer and gives the composite identity

\[
 p^T Q = \sum_i (p_i Q_i+V_i I_i)+V^T Y V.
\]

For the shunt experiment, the dry network is `Y_t=Y+tuu^T`. Applying the same balance to that assembled passive network gives

\[
\begin{aligned}
 p^TQ
 &= \sum_i(p_iQ_i+V_iI_i)+V^T Y_tV\\
 &= D_{\rm wet}+V^T YV+t(u^TV)^2,
\end{aligned}
\]

where `D_wet:=Σ_i(p_iQ_i+V_iI_i)≥0` under the stated reciprocal wet-block passivity assumption, `V^TYV=V^T sym(Y)V≥0`, and `t(u^TV)^2≥0` is the added shunt dissipation. Thus passive shunt heat is already a destination in the same composite power balance whose left side is the **net signed hydraulic port power**. Do not add measured shunt dissipation to that hydraulic input a second time. Measuring or calculating it is still useful to close and partition the energy balance and diagnose losses.

This identity is a balance across the physical hydraulic and electrical network ports; it is not a statement that arbitrary apparatus power is free or included. Powered shunt switching, voltage/current/flow readout, pressure control, gate maintenance or charging, magnetic-field generation, refrigeration/temperature stabilization, and other supplies that cross the chosen system boundary must be metered and counted once as external acquisition or auxiliary resources. If any such power is drawn from a hydraulic source or recovered through a port, record that port flow and avoid counting the same transfer twice.

## Net versus donor-only hydraulic work

With the source's “power entering the device” convention, define signed hydraulic port powers `P_j(t)=p_j(t)Q_j(t)`. For an interval `[0,T]`,

\[
 W_{\rm net}=\int_0^T\sum_jP_j(t)\,dt,
\quad
 W_{\rm donor}=\int_0^T\sum_j\max(P_j(t),0)\,dt,
\quad
 W_{\rm receiver}=\int_0^T\sum_j\max(-P_j(t),0)\,dt.
\]

Then `W_net=W_donor-W_receiver`. The theorem's instantaneous `p^TQ` is net, not gross donor-only pump work. For a multiport transfer or an acquisition-cost ledger, report port-resolved donor input and receiver output (and, when relevant, actual pump electrical input including pump inefficiency) alongside the net balance. In the frozen proof, `W_hyd=Σ∫p^TQ dt` is therefore to be read as signed net hydraulic port work; it is not by itself a gross pumping-cost estimate.

## Scope impact

No Schur identity, identifiability claim, rank certificate, noise bound, or Gaussian sample-count formula changes. The passive shunt affects the measured response `H(t)` exactly as proved, while its dissipation is handled in the power balance above. Only the interpretation of the energy ledger is corrected: account shunt dissipation once as an internal loss, distinguish net port work from donor-only input, and add separately metered external switching/readout/gate/field/thermal resources once at their respective boundary ports. No apparatus powers or work values were measured, so numerical cost remains **UNKNOWN**.
