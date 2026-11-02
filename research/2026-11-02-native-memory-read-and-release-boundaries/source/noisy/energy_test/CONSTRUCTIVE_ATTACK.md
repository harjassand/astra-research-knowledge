# Constructive preparation-energy test: exact-charge-conserving driven attack

## Verdict and scope
There is a constructive polynomial-resource attack in the admitted **time-dependent, bounded-body energy-resolved contact model**, provided the bath species may include a fixed inverted virtual transition resonant with the code energy quantum. Heterogeneous fixed small Pauli flip rates readily supply this transition. This is stronger than failure of a divergence proof. It is NOT a construction for a fixed preassigned bath spectrum, native two-body controls, or a static autonomous controller.

Assume a bounded-degree local commuting CSS Hamiltonian with local Pauli energy changes in Δ times the integers, |ΔE|≤dΔ for constant d, and an explicit logical Pauli expressed as N≤poly(n) local Paulis. Standard uniform-coupling stabilizer Hamiltonians have this property. The code-specific existence/geometry must be checked against the actual code definition. No ground-state initialization of the code is required.

## 1. A constant-size noisy virtual work source
For a bath spin with gap E initially Gibbs at β>0 and independently X-flipped with probability p,
q(E,p)=p+(1−2p)/(1+exp(βE)).
Choose constant hot/cold gaps E_h=E_c+Δ and fixed rates 0<p_c<p_h≪1. Taking E_c sufficiently large (still independent of n) ensures q_h>q_c. A concrete sufficient condition is exp(−βE_c)<(p_h−p_c)/2, with a little slack. Set
 a=q_h(1−q_c), b=(1−q_h)q_c, r=a/b>1.
The exactly energy-conserving exchange |1_h,0_c,0_b>↔|0_h,1_c,1_b> raises a gap-Δ battery bit. Each contact uses a *fresh* noisy pair. No battery or clean sink is hidden in the initial bath.

This parameter choice requires the allowed fixed onsite-energy bound to accommodate E_c. If a smaller externally prescribed bound is part of the problem, this particular two-spin source must not be asserted. Constant-size multi-spin virtual transitions are an alternative, but require a separate resonance check.

Equal noise rates on different gaps do not invert the elementary two-spin transition: q(E,p) decreases with E. But a **concrete three-spin virtual source** does: choose two cold spins of gap E_c and one hot spin of gap E_h=2E_c+Δ, all flipped with the same fixed p∈(0,1/2). The resonant exchange is |1_h,00_c,0_b>↔|0_h,11_c,1_b>. Its up/down probabilities are a=q_h(1−q_c)^2 and b=(1−q_h)q_c^2. As E_c grows (remaining fixed in n), q_h,q_c→p, so a/b→(1−p)/p>1. Hence a sufficiently large fixed E_c supplies inversion even with equal noise rates. It uses one extra bath spin per fresh contact and otherwise exactly the same construction.

A prescribed finite onsite-gap upper bound can instead be handled for heterogeneous rates if the allowed bounded-body constant may depend on the fixed noise rates: choose E_c in the interior of that bound, E_h=E_c+δ with δ=Δ/m. At δ=0 the hot excitation probability strictly exceeds the cold one; continuity guarantees inversion for sufficiently large fixed integer m. Use battery gap δ and replace d by m d. The required contact body size is still independent of n, but larger. If a model fixes both a strict small body cap and a strict gap cap in advance, this tradeoff must be checked explicitly.

## 2. Logarithmic battery and a legitimate rare branch
Use L=2M=O(log n) battery spins of gap Δ. The valid subspace consists of unary strings |k>=|1^k0^(L−k)>, k=0,…,L. Start on the branch |M>, together with one zero degenerate flag. Their initial product-Gibbs probabilities, even after the independent preparation noise, obey
 w≥exp(−C L)=n^(−C').
All their gaps, flip rates, and Gibbs probabilities are fixed constants. This is NOT postselection or a clean-resource gift: run the same deterministic control schedule on the full initial mixture, and lower-bound its error contribution from this explicitly identified component. Only O(log n) spins are constrained. The many thermal routing carriers are never conditioned.

## 3. Refill to the middle, not to the top
For each ladder edge k↔k+1 below M, implement the virtual-source exchange conditioned on the nearby unary-wall pattern. This touches at most a fixed number of battery and bath spins. Up/down probabilities are a,b. Above M, use a fresh gap-Δ spin with excitation probability q_0<1/2; the analogous exchange has up/down probabilities q_0,1−q_0. Thus every edge kernel preserves the distribution
 π(k) ∝ r^(k−M), k≤M;
 π(k) ∝ [q_0/(1−q_0)]^(k−M), k≥M.
It is sharply peaked around M and places exponentially small mass within d of either boundary. The upper-side contacts dump released code energy into ordinary mixed bath spins; no clean entropy sink is used.

Use a fixed forward-and-back sweep through all edges, with fresh reservoir spins at every contact. Each edge preserves π, so the full sweep does. Here is a deliberately crude but sufficient **polynomial-time mixing proof**, avoiding an appeal to efficient global thermal permutations. All required moves and self-loops have probabilities bounded below by a constant c>0. In a forward/back sweep of O(L) contacts, every starting k can follow a path to M (use the ascending sweep if below M; the descending sweep if above M), and otherwise remain put. Therefore Q(k,M)≥c^(O(L))=:ε=n^(−O(1)). Doeblin contraction gives total-variation distance ≤(1−ε)^t after t sweeps, uniformly in the starting k. Taking t=ε^−1 O(log n) is polynomial and makes the mixing error n^−A for any fixed A. Sharper mixing bounds are unnecessary.

Choose M large enough that π({k<d or k>L−d})≤n^−A. Refill before every code step. Conditioned on every past success, the next shortage/overflow probability is ≤2n^−A, uniformly over the current syndrome and battery state.

## 4. Implement each local Pauli once, reversibly
For a desired local P, resolve its finitely many local stabilizer syndromes s, with energy difference ΔE_s=d_sΔ, |d_s|≤d. For each admissible k and s, perform the transposition
 |flag=0,s,k> ↔ |flag=1,P(s),k−d_s>,
including P on the physical data. Both sides have identical K. Different (s,k) pairs have disjoint source/target states because flag values differ and (s,k)↦(P(s),k−d_s) is injective. Accordingly these transitions can be applied sequentially without undoing one another. A fixed-phase Hermitian exchange realizes the same desired phase on every flag-0 source. At the end, flip the degenerate flag, resetting it on every successful branch. Failure branches need not be repaired.

A shift by |d_s| flips a constant-size segment at the unary wall. Its wall guards, local syndrome projectors, flag, and data support have bounded body size. This is precisely where the admitted energy-resolved contact primitives are used. The construction does NOT establish a native two-body realization. There are O(L) wall positions and O(1) local syndrome patterns per P.

## 5. Geometry, controls, and resource ledger
- Battery/flag low-entropy initialization: O(log n) conditioned bits, probability n^−O(1).
- Fresh hot/cold pairs and upper-side sink spins: N times polynomial(n) refill contacts; total polynomial bath volume, initially product Gibbs and then independent fixed-rate Pauli noise.
- All baths are used once; their spent entropy and energy remain in the physical system.
- Equal-gap nearest-neighbor SWAPs transport logical bath/battery states through thermal carriers. No carrier is initialized clean. Constant-size contact groups can be brought to local service ports, then routing can be undone or tracked.
- Bounded-density 3D layouts with polynomially many sites and wires permit a polynomial-depth sequential routing schedule. At most a constant number of gates run at a site at once. The code itself is not SWAP-routed unless such code-preserving transport is separately available.
- Local contact Hamiltonians and equal-gap swaps commute exactly with K. Pulse amplitudes are O(1), pulse times O(1); route lengths and total pulse count are polynomial.
- Time-dependent switching is expressly admitted. Every active term commutes with K, so d⟨K⟩/dt=0 exactly. This counts reference-charge injection, not the full thermodynamic fabrication/control cost of an external clock. A static autonomous claim would need a real clock construction and is not made.

The geometric service-port statement presumes bounded-size local code stars can be contacted by a constant number of bath lines without changing the prescribed code Hamiltonian. If the actual geometry forbids such access, that is a genuine extra model restriction, not solved by this note.

## 6. Failure probability
Take A>deg(N)+2. On the initial unary/flag branch, the union probability of any energy-boundary gate failure is ≤2N n^−A=o(1). The product of the implemented code Paulis is the known logical Pauli. Its total energy change is zero, but intermediate positive work is provided by the noisy virtual source, and negative work is stored/dumped. The controller thus implements a logical flip with conditional probability 1−o(1) in polynomial time. For a protected initial decoded logical eigenstate, this contributes physical decoded-error probability at least n^−C'(1−o(1)), up to any separately quantified initial logical decoding error. This is much greater than exp(−n^η) for every fixed η>0.

This last interpretation assumes the standard syndrome-based decoder is covariant under the chosen logical Pauli. If the proposed guarantee concerns a different operational memory observable, specify its failure event and test it explicitly rather than substituting raw logical-Pauli expectation.

## Consequence
A uniform noise-thickened lifetime theorem that quantifies over these bath species and all admitted driven K-conserving controls is physically false. The mechanism spends preparation-induced free energy, not control-supplied reference energy. Exact-Gibbs stationarity remains intact: with p_h=p_c=0 the resonant source has r=exp(−βΔ)<1 and cannot maintain the middle-peaked battery. The decisive residual checks are actual-code energy commensurability, contact geometry, and whether the claimed quantifiers include the chosen bath species/gaps.

## Established mechanism, not claimed novelty
Negative-temperature virtual transitions powering work storage are standard quantum heat-engine physics. A primary theoretical source explaining the virtual-temperature engine regime is Mitchison et al., “Realising a quantum absorption refrigerator with an atom-cavity system,” Quantum Sci. Technol. 1, 015001: https://doi.org/10.1088/2058-9565/1/1/015001 . The logarithmic unary-buffer/minorization/flag construction above supplies the resource-accounting argument needed here; the source is not being cited as proving this memory attack.
