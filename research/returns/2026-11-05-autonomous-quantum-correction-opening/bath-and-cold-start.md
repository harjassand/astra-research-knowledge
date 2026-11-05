# Exact-secular bath and cold/thermal transfer obstructions

The [complete dossier](NORTH_STAR_RESEARCH_DOSSIER.txt) contains the final full proofs and affine strengthening. These are obstructions to specified arguments or models, not universal quantum-memory impossibility results. Earlier Gibbs constructions and distinct generator classes remain unchanged.

## Theorem B: every encoder and final decoder

Let `H=sum_X h_X` on `N` qubits have simple spectrum and distinct ordered nonzero energy gaps, with per-site interaction norm at most `J`. Use the **exact fully secular Davies generator**, independent one-site X/Y/Z baths, and rates uniformly at least `g>0` for `|omega|<=4J`, independent of site and size. A commuting Lamb shift is allowed. Then every qubit encoding channel and every final decoding channel obey

\[
F_{ent}(t)\le[1+e^{-Ngt}]/2.
\]

Retention fidelity at least `1-epsilon`, `epsilon<1/2`, requires `t<=-log(1-2epsilon)/(Ng)`.

Distinct gaps make nonzero-frequency jumps rank one. At each site/eigenstate, off-diagonal Pauli weight is at least 2, while its energy-weighted second moment is at most `12J^2`. At least one unit lies inside the bounded-rate window. The total rank-one jump-loss operator therefore satisfies `R>=Ng I`.

The branch with no such jump is CP and trace-decreasing with mass at most `exp(-Ngt)`. Every other branch contains a rank-one jump and is entanglement breaking, even after arbitrary encoding/recovery and mixtures. A separable reference/output branch has Bell overlap at most half its mass, giving the bound. This is an operational arbitrary-encoder/decoder argument, rather than ordinary correlation decay.

The rate hypothesis can fail, for example for spectra vanishing at zero. Exact protected degeneracies also evade the distinct-gap premise. These conditions cannot be omitted.

## Affine applicability is proved on specified perturbation spaces

For **any fixed base Hamiltonian**, the allowed perturbation directions must contain onsite X/Z and ZZ bonds along one spanning nearest-neighbor path. Established nonresonant-witness machinery and a homogeneous gap-discriminant polynomial show that exceptional perturbations have measure zero in every arbitrarily small open coefficient box. Fully occupied rectangular lattices provide such a path, including finite-range many-body base terms.

With a uniform interaction bound and rate window, Theorem B consequently excludes an open robust long-memory region within that precisely specified exact-secular family. Local fields alone do not suffice; translation/symmetry-restricted, irregular-support and exact-gauge families need separate witnesses. The spectral genericity machinery is established prior art; the dossier supplies its affine composition with the operational bound.

## Why this is not a physical fixed-coupling no-go

Full secularization resolves arbitrarily close frequencies after an infinite weak-coupling time limit at each size. Resolving shrinking splittings can require microscopic system-bath coupling to decrease with `N`; in physical time, `g_N` can vanish. That violates uniform `g`. One-site microscopic coupling operators can also produce nonlocal spectral jump components.

Finite-resolution or quasi-local generators are different models. The separate annular-clustering phase-transfer theorem requires quasi-local terms and termwise stationary Gibbs state; generic fully secular generators do not automatically satisfy it. Theorem B does not refute that theorem or prove impossibility at fixed microscopic coupling.

## Exact mediator counterexample and its scope

The source supplies `H_e=(Delta I+e Z_L) tensor |1><1|_a`, `0<=e<Delta`, with the same coupling `I tensor X_a`. The ground logical space is identical for all `e`, the gap stays positive and Hamiltonian/Gibbs/fixed-time unitary errors converge to zero as `e->0`. Nevertheless, the exact secular bath separates the two logical transition frequencies at every positive `e`. Even the optimal decoder has

\[
F_{opt}(t)=[1+e^{-\Gamma_e t}]/2,\qquad
\Gamma_e=r e^{-\beta\Delta}\cosh(\beta e),
\]

while `e=0` stores perfectly in this toy coupling model. Negativity proves the optimal-decoder upper bound; tracing out the mediator attains it.

The toy logical qubit lacks protection against direct logical-site noise. It disproves an unrestricted Hamiltonian/Gibbs-to-Davies continuity argument, not every mediator encoding of the passive 3D incumbent. A replacement construction needs an exact all-sector logical/gauge commutant or a bath-resolution-aware dynamical transfer, followed by a protection theorem.

See [principal obstruction](package/north_star_round/principal/secular_bath_obstruction.txt), [researcher B and independent audit](package/north_star_round/researcher_b.txt), [recorded exact checks](package/north_star_round/checks_b.json) and the dossier's later final affine/time-unit refinements.

## Theorem W: an extensive cost defeats one cold-start proof

For the unit-strength commuting Pauli Hamiltonian `H=sum_a(I-S_a)/2`, with check weight at most `w`, degree at most `D` and no unprotected qubit, pack `M>=N/[D(w-1)+1]` qubits with disjoint check neighborhoods. Their independent valid syndrome excitations give

\[
Z_{syn}\ge(1+e^{-\beta D})^M=\exp(\Omega_\beta(N)).
\]

The least operator-order domination constant comparing a cold logical encoding with the same logical state in a thermal syndrome background is **exactly** `Z_syn`. An allowed IID `p` write still costs at least `Z_syn(1-p)^N`, exponential at sufficiently small fixed `p`.

Thus direct domination cannot turn a stretched-exponential thermal leakage bound into the wanted cold-write retention guarantee. This does not prove that cold states lose information quickly. A dynamics-specific occupation/committor bound or a genuine basin-entry protocol remains missing. A generic fault-tolerant encoder plus an equilibrium theorem does not supply it, and an unprotected incoming qubit has its own entry-error floor.
