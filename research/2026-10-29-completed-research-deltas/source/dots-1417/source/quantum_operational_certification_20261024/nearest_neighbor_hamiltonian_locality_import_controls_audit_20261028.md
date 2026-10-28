# Independent primary-source import: finite-time nearest-neighbor unitary locality

28 October 2026. **PASS for the narrow structural transfer below.** This review reads the primary theorem directly, applies it only to unitary Hamiltonian dynamics, and derives a state-independent local-reflection witness. It does not supply or learn a Hamiltonian, invert a source, prove the Pauli/gauge noise model, or establish a new hardware/control advantage. No source calls or new sampling were performed. Received manuscripts remain unchanged.

## 1. Precisely imported primary result

The inspected primary PDF is [Barthel–Kliesch, arXiv:1111.4210v2](https://arxiv.org/pdf/1111.4210v2), version marked 9 August 2012. Definitions (3)–(7) specify interaction diameter a, overlap count Z including the term itself, the interaction extension bar(V), term-count volume, and truncation to terms contained in a region. Equations (8)–(9) fix the Heisenberg propagator convention. Theorem 2, equation (14), uses the truncation on **bar(V)** and states

`||tau(r,t)O_Y - tau_bar(V)(r,t)O_Y||`

`<= (2M/Z)||O_Y|| D^k exp(e Z b (t-r)-D)`,

where `b=|ell|`, `D=ceil[d(Y,Lambda\V)/a]`, and `D>2k+1`. Its shell assumption (13) bounds the number of terms at normalized distance in `[m,m+1)` by `M m^k` for positive integers m, with positive M and k. These are the only external theorem facts imported here. The letter k below denotes the graph-growth exponent, not the calibration margin kappa.

## 2. Proposed physical family and independent parameter substitution

Work on an open line of n physical qubits with metric `d(x,y)=|x-y|`. Assume a single common unitary propagation generated for duration T by

`H(t)=sum_(j=1)^(n-1) h_(j,j+1)(t)`, `||h_(j,j+1)(t)||<=J`.

The finite propagator is assumed well defined, for example for bounded piecewise-continuous terms. Interaction labels are nearest-neighbor edges, with one grouped term per edge. The initial logical label i occupies one unknown site `y_i`, with the map i to y_i injective. All other sites form the gauge. This initial placement is fixed across encoders. The Hamiltonian, its terms, and the site assignment are unknown; only valid structural bounds such as J and T are supplied.

For a nonzero edge-commutator decomposition:

- `a=1` using the edge labels; a term may be labeled by its edge even if it acts trivially on one endpoint.
- Each edge intersects at most its predecessor, itself, and its successor. Thus `1<=Z<=3`.
- `ell_j(O)=i[h_j,O]` has induced operator-norm bound `||ell_j||<=2J`; hence `b<=2J`.
- At positive integer distance m from a single site, at most two edge labels occur. Therefore `M=2`, `k=1` is valid because `2<=2m`. Choosing k=1 respects the primary theorem's positive-exponent wording rather than silently substituting k=0.

These constants apply to the stated grouped-edge model. Additional independently bounded onsite terms must first be grouped and their new edge norm bounds charged, or the overlap/shell constants must be recomputed. Periodic or higher-dimensional geometry is not silently identified with this open line.

## 3. Time orientation: reversed negative Hamiltonian, only as a proof device

Let `U(t,s)` solve `partial_t U(t,s)=-i H(t)U(t,s)`, and set `U=U(T,0)`. The desired logical operator is `U sigma_y U†`. The paper's ordinary Heisenberg convention for the same H instead gives `U† sigma_y U`.

For general time-dependent H, replacing H(t) by merely -H(t) is not enough. Define

`H_rev(t)=-H(T-t)`.

Its Schrödinger propagator is `U_rev(t,0)=U(T-t,T)`, so `U_rev(T,0)=U†`. The paper's Heisenberg action for H_rev is therefore exactly `U sigma_y U†`. Time reversal and negation preserve every edge norm, overlap and shell bound.

This manipulation proves an existence bound; it is not an operational inverse query, a supplied backwards source, or an instruction to implement an unknown Hamiltonian. Truncation commutes with the reversal operation. If `U_S` is the forward propagator for the original H with terms restricted to S, the corresponding truncated reverse-Heisenberg map sends `sigma_y` to `U_S sigma_y U_S†`.

## 4. Spatial truncation and boundary cases

Choose an integer `D>=4` and a single initial site y. Put

`V={z in Lambda: |z-y|<D}`.

If V is proper, its distance to the complement is exactly D, so the primary theorem's distance parameter is the chosen integer D and its strict threshold `D>2k+1=3` is satisfied. The interaction extension bar(V) adds at most one site at either endpoint. Its truncated generator includes **all interaction terms whose supports are contained in bar(V)**, as in definition (7); it is not silently replaced by truncation to V.

Use the containing physical interval

`I_D=[y-D,y+D] intersect Lambda`.

It contains `{y} union bar(V)` and has width at most `min(n,2D+1)`. Including y explicitly handles an isolated initial site: the union defining bar(V) need not contain an isolated site, while the unchanged observable still acts there. A shorter boundary interval can be padded to the supplied common width without changing support.

If `V=Lambda`, all nonzero interaction terms are retained and the truncation is exact. Use that equality; do not substitute an infinite complement distance into a finite-D formula. An identically zero commutator generator, including scalar Hamiltonians producing only global phases, is also exact and needs no undefined Z denominator. T=0 is likewise exact. In particular n=1 under this edge-only model is trivial dynamically, though its unknown logical labeling remains part of the source convention.

## 5. Exact local reflections and the quantitative tail

Let S=bar(V), retain the original site if it is isolated, and define the proof-only proxy

`V_(j,y)=U_S sigma_(j,y) U_S†`, `j=X,Z`.

The restriction remains a Hamiltonian evolution, so U_S is unitary. Consequently each proxy is an exact Hermitian reflection and the pair obeys exact Pauli anticommutation, because the same U_S is used for both axes. Distinct sites may use different truncated regions and need not yield commuting proxy pairs. Each proxy is supported in I_D. No entry of U_S is supplied to the learner.

Substitution in the imported inequality gives, for each Pauli of norm one,

`||U sigma_(j,y) U† - V_(j,y)||`

`<= (4/Z) D exp(e Z b T-D)`

`<= 4D exp(6eJT-D)`.

The trivial distance bound between reflections is two. Thus, away from the separately exact cases, a valid uniform tail is

`tau_D=min{2, 4D exp(6eJT-D)}`,

with supplied local width `w=min(n,2D+1)`. For every normalized physical state rho, including all the received mixed gauges,

`Tr rho(B_(j,y)-V_(j,y))^2 <= ||B_(j,y)-V_(j,y)||^2 <= tau_D^2`.

This is stronger than the weighted proxy promise, without a gauge spectral floor. The unknown injective assignment y_i is harmless to existence and is precisely why the ordinary learner still has to locate the physical intervals.

For a chosen target `0<tau_req<2`, a convenient sufficient integer choice is

`D >= max{4, 2[6eJT + ln(4/tau_req)]}`.

Indeed `ln D<=D/2` for D>=4, so `4D exp(6eJT-D)<=4 exp(6eJT-D/2)<=tau_req`. Taking a ceiling makes the choice integral. If the resulting ball covers the finite chain, exact full-register truncation is available instead. To invoke the received approximately local theorem, require the chosen structural tail to obey `tau_req<=kappa/8`; any stronger final-risk target must also pay its q/width-dependent approximation floor.

## 6. What this transfer does and does not establish

The conclusion supplies a physically recognizable sufficient condition for the received approximate-local proxy promise. It does **not** import the primary paper's known-generator simulation algorithm into the learner. The learner still receives ordinary reset data, acquires local CPTP candidates/reflections, pays their dense width-dependent synthesis and routing, and qualifies its newly frozen joint receiver. Neither U nor H nor their inverses are learned or provided by this argument.

The source must separately retain the common Pauli/gauge channel model, calibrated positive aggregate contrasts, fixed common U across encoder choices, and global identity dominance if an unrestricted noisy-source oracle comparison is claimed. Generic Hamiltonian scrambling followed by arbitrary local noise, or arbitrary Markovian open-system dynamics, does not automatically have that form. The restriction to unitary dynamics is essential here: a general truncated dissipative propagator need not preserve reflections.

For fixed target tail the displayed width is `O(JT+log(1/tau_req))`, but the learner's actual `4^w` and other width factors must be substituted. The argument is not a constant-cost, time-independent, or generic scalable decoder claim. Equally informed conventional subsystem identification receives the same structural implication and learning procedure.

## 7. Provenance

Primary access used the versioned PDF linked in Section 1 and inspected definitions (3)–(7), propagator conventions (8)–(9), shell condition (13), and Theorem 2/equation (14). The full approximate-local result being connected is `ordinary_approximately_local_joint_recovery_20261028.md`, received SHA256 `1ae8d8f836d366268a4c8f182b9c8b679ba77aea9fde5ebe669e5e576ad74c4d`.

No source samples or simulations were introduced, and no received result was modified. This audit binds only the primary-import/physical-structure lemma; any forthcoming combined construction requires its own source-specific receipt.
