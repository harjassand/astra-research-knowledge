# Independent audit of root's weak-endcap resonant path

This candidate was supplied by root after my independent construction and obstruction were recorded. This document validates its isolated-mediator identities, not the full overlapping many-check polymer theorem.

Let n=K-1, A=t(2I-adj_path_n), v=e_1+e_n, and endpoint amplitude g=eta*t/K. Here K>=3. Write mu=2t[1-cos(pi/K)].

## Exact identities

For 1<=i,j<=K-1,

`G_ij=(A^-1)_ij = min(i,j)[K-max(i,j)]/(tK)`.

Therefore:

- `G_1n=1/(tK)`.
- `vᵀ G v=2/t` exactly.
- `Gv=(1/t) 1`, hence `vᵀ A^-2 v=(K-1)/t²` exactly.
- `(A^-2)_1n=(K²-1)/(6t²K)`.
- Normalized winding mean time is `(K²-1)/(6t)`.
- `Tr A^-1=(K²-1)/(6t)`.

For excursion density `a(l)=g² vᵀ e^(-Al) v`, its integrated activity is `2g²/t` and first moment is `g²(K-1)/t²`. For winding density `w(l)=2g²[e^(-Al)]_1n`, its integrated activity is `2g²/(tK)=J0`.

Thus with g=eta*t/K, activities are `2eta²t/K²`, `eta²(K-1)/K²`, and `J0=2eta²t/K³`. The first moment is dimensionless; the winding normalized mean carries units of time.

## Exponential time tilt: uniform-in-K relative winding control

For 0<=b<mu, put theta=arccos(1-b/(2t)). The exact endpoint Green function is

`[(A-bI)^-1]_1n=sin(theta)/(t sin(K theta))`.

Its ratio to the untilted value is

`R(b)=K sin(theta)/sin(K theta)=Π_(r=1)^(K-1) lambda_r/(lambda_r-b)`.

The product formula follows because the endpoint cofactor is t^(K-2), independent of b. Consequently,

`1 <= R(b) <= exp{ b(K²-1)/[6t(1-b/mu)] }`.

At `b=c D eta² t/K²` with `c D eta² < K² mu/t` (asymptotically pi²), this is `1+O(D eta²)` for small D eta², uniformly in K. This is precisely the nontrivial relative control needed for a marked winding; replacing it with a crude 1/mu resolvent norm would lose the useful scaling.

For the unmarked excursion integral, positivity of spectral weights yields

`vᵀ(A-bI)^-1 v <= (1-b/mu)^-1 * 2/t`.

Its tilted first moment obeys

`vᵀ(A-bI)^-2 v <= (1-b/mu)^-2 * (K-1)/t²`.

These establish the quoted scaling of weighted activity and duration; a complete KP proof still must specify its overlap convention, hard-core exclusions, combinatorial constants, and sign bookkeeping.

## Operator lower bound survives overlapping data

Each individual excited path with unitary Pauli labels is gauge-equivalent to A by a clock-controlled prefix unitary, regardless of other gadgets. Thus its operator inequality is `H_internal,a >= mu Q_a`. Summation gives `Σa H_internal,a >= mu Σa Q_a` even when these terms do not commute. This does not justify simultaneous diagonalization; it does justify the sum lower bound. All Q_a commute as clock projectors.

## Single-check full-spectrum numerical test

In syndrome s, construct the K-dimensional matrix with clock 0 energy 0, path sites 1..K-1 energy 2t, internal hoppings -t, links 0–1 of -g and 0–(K-1) of -s*g. No levels are removed.

The included `path_check.py` computes full eigenvalues and exact full Gibbs traces. Across K=4,8,16,64,180 the ground syndrome gap divided by its predicted `2J0` is:

- eta=.1: approximately .9965–.9967;
- eta=.3: approximately .969–.9705;
- eta=.5: approximately .918–.923.

At beta*J0=5 the full-trace penalty equals the ground syndrome gap to displayed precision. In particular K=180, eta=.3 gives J0/t=3.08642e-8 and relative gap .970475. The proposal removes exponential K suppression but is still a very cold hardware scale at K=180.

The ordinary sufficient bound g<<mu fails for large K, since g/mu~eta K/pi². This is not evidence against the proposal: its endpoint-resolved self energy and duration norms remain small. It does mean a generic off-the-shelf perturbative gadget theorem is not an adequate proof.

## Thermal distinction from the fully resonant cycle

At beta*J0=c>0,

`beta*mu = c * K³[1-cos(pi/K)]/eta² ~ c*pi²*K/(2eta²)`.

Real excited-path wraps are consequently exponentially suppressed in K/eta² at the intended protection temperature, whereas the bare fully resonant cycle has no separate vacuum sector. Charging wraps via `(K-1) exp(-beta*mu)` includes a simple finite-level entropy bound, though the many-gadget interacting partition function requires a local relative estimate rather than a global Hilbert-space prefactor.

## Remaining deliverables

The isolated check and weighted Green identities are strongly positive. They do not alone prove the full equilibrium polymer estimate, perturbative stability, generic local bath control, or useful temperature at weight 180. No same-resource finite-temperature cap of this precise weak-endcap resonance was identified in the brief primary-source check; that is not a novelty claim.

## Additional isolated-check improvement: counterterm-centered resonance

A potentially useful refinement, **not yet a many-check construction**, is to add `+2g²/t |0><0|`. At zero spectral parameter its exact Schur complement is

`2g²/t I - g²[2(K-1)/(tK)I + 2/(tK)S] = J0(I-S)`.

Thus the isolated check Hamiltonian is positive semidefinite and the S=+1 ground energy is exactly zero. The corresponding path amplitudes are uniformly `g/t` after gauging, so exact ground-state excited occupancy is

`p_Q=(K-1)g²/t² / [1+(K-1)g²/t²]`.

This permits choosing `g=eta*t/sqrt(K)` while keeping p_Q~eta² and J0=2eta²t/K², instead of K^-3. The S=-1 self-energy derivative is also bounded because

`(e1-en)ᵀA^-2(e1-en)=(K-1)(K-2)/(3t²K)`.

For small eta, the isolated syndrome gap is `2J0[1+O(eta²)]`, uniformly in K, with higher levels separated on the same t/K² scale.

This counterterm is important: without it, g~t/sqrt(K) produces a scalar energy shift of order eta²t/K, much larger than mu; evaluation of the endpoint Green function at that negative energy can restore a stretched-exponential attenuation. Centering the vacuum removes that isolated mechanism.

**Unresolved many-check issue:** although each term is positive, the separate kernels need not intersect when prefix Pauli operators of neighboring clocks anticommute. The shared-data frustration and interacting excursion gas must be handled after scalar resummation. Positivity alone does not imply a frustration-free joint ground state or a thermal memory. Root was notified for finite-seed testing.
