# Local ancillary detector/reset extension audit

24 October 2026. Bounded check of `COMPILED_CONTROL_ACTUAL_RISK_THEOREM.txt`; this concerns only its fixed finite-library scope. The all-smooth-control window claim remains open.

## Exact-zero-risk support with local jumps

For a zero-risk input, positivity and `gamma>0` give `P_e rho(t)=0` throughout a primitive. Let `S=I-P_e-P_dead` and `K(t)=P_e H_g(t) S`. The `e`-to-safe block of the master equation gives `K(t)rho(t)=0`: the local jump `L_l(t)=I_sample tensor M_l(t)` contributes zero to that block when `P_e rho=0`, since it preserves the sample sector. The dephasing and terminal-loss terms likewise add no `e`-safe source on this face.

At a fixed time put `G=K†K`. From `K rho=0` and positivity, `G rho=rho G=0`. The contribution of any Lindblad jump `L` to the derivative of `Tr(G rho)` is then

\[
\operatorname{Tr}(G\mathcal D[L](\rho))
=\operatorname{Tr}(L^\dagger G L\rho)
=\|K L\sqrt\rho\|_2^2\ge0,
\]

because both anticommutator terms vanish. The Hamiltonian commutator term vanishes on the same zero face. Thus the independent dephasing jump gives `K Z sqrt(rho)=0`; each ancillary jump adds the nonnegative constraint `K(I tensor M_l)sqrt(rho)=0`, rather than a cancelling term. Repeating with `KZ` gives `K Z^2 sqrt(rho)=0` (the extra ancillary terms remain nonnegative). With `P_a=(Z^2+Z)/2` and `P_e H_c P_a=0`, one obtains `g |e><a| sqrt(rho)=0`; `g>=ell>0` forces `P_a rho=0`. The argument is pointwise in time and also accommodates time-dependent bounded rates/waveforms; at times a jump rate is zero it imposes no jump constraint. It relies on independent Lindblad channels and the exact sample-identity form of `L_l`; a sample-changing or correlated jump is not covered.

This validates the local-jump extension at the stated scope. For a monitored trajectory calculation, the no-click drift must still include `-1/2 sum_l (I tensor M_l†M_l)` along with the Hamiltonian, dephasing, and terminal-loss terms. Dropping it can give the wrong invariant subspace even though the unconditional carré-du-champ calculation above is positive.

## Hardware and composition boundary

A detector or reset is covered only when it is an actual finite-rate local jump on the finite working register, with its records and no-click evolution included in the primitive's full effect. The primitive's duration and all sample occupation during routing, smooth boundary connections, preparation, readout, and cleanup count in `A_j` and its risk in `W_j`. A local ancilla jump is not a free instantaneous sample measurement/reset: it cannot change `a/e`, and any transfer or feedback that touches the sample must be an explicitly paid library primitive. A fresh ancilla, output mode, reset channel, or optical sector is covered only if its finite working dimension and actual operation are included; enlarging active arity/library can change `C_library`.

For an untouched reference `R`, primitive effects are `A_j tensor I_R` and `W_j tensor I_R`, so the local inequality holds on entangled inputs of arbitrary reference dimension. Adaptive **classical** choice among the fixed library is also covered: apply the effect inequality to each subnormalized history-conditioned live state and sum/integrate over histories. Terminal-death increments are disjoint because the sample is never restarted after death. Old records/references may therefore grow as spectators without changing the local constant. If they coherently control the primitive, are routed into its active interaction, or supply a new waveform, they are no longer spectators: count them in the active register and re-certify the library constant. A finite reset protocol is covered only when each reset and any connection/routing step is physically in the library; a reset-to-pure-state oracle or indefinitely many fresh active registers is outside a fixed-`D` certificate.
