# Autonomous reset bridge: exact local renewal gadget, not yet a fault-tolerant compiler
Date: 2026-10-29. Status: one exact constructive lemma plus explicit obstructions.

## 1. What the primary sources actually permit
- D. Dünnweber, G. Styliaris, R. Trivedi, *Quantum Memory and Autonomous Computation in Two Dimensions*, arXiv:2601.20818v1, §§III.2, IV, Discussion. https://arxiv.org/html/2601.20818v1
  Discrete QCA uses local coherent fault-path noise. Continuous construction uses local CPTP attempted updates Φα, generator Σα(Φα−Id), and perturbing **unitary** Poisson jumps. Its discussion explicitly leaves general non-unitary Lindbladian noise open. Its marching-soldier mean-speed estimate is not, by itself, a joint local fault-tail estimate. Prepared hierarchical encoded input is assumed; initialization must be counted separately.
- S. Balasubramanian, M. Davydova, E. Lake, *A local automaton for the 2D toric code*, arXiv:2412.19803v2. https://arxiv.org/html/2412.19803v2
  Uses measurement/feedback gadgets and p-bounded sets of faults, not merely a mean error density; imperfect measurements have a distinct treatment. Does not supply the microscopic reset compiler here.
- V. Kashyap, G. Styliaris, S. Mouradian, J.I. Cirac, R. Trivedi, *Accuracy guarantees and quantum advantage in analogue open quantum simulation with and without noise*, arXiv:2404.11081v2. https://arxiv.org/html/2404.11081v2
  Very close comparator: damped ancilla + engineered Hamiltonian, geometric locality and Lieb–Robinson bounds, size-independent local-observable simulation bounds. Time-uniform local-observable claims require rapid mixing. This is not a uniform fault-path bound for a memory, and the couplings inherit jump support (not generally two-body).
- Verstraete–Wolf–Cirac, arXiv:0803.1447. https://arxiv.org/abs/0803.1447
  Dissipative universal computation is established prior art. No novelty is claimed for dissipative computation or the basic reset gadget.
- Aliferis–Gottesman–Preskill, quant-ph/0504218. https://arxiv.org/abs/quant-ph/0504218
  Local coherent fault amplitudes, not independent stochastic errors, are the appropriate comparator once ancilla memory is retained.

## 2. Exact isolated update construction
Let Φ(ρ)=Σ_{s=1}^m K_sρK_s† be a fixed constant-support CPTP update, so Σ K_s†K_s=I. Use a single (m+1)-level ancilla, basis 0,1,...,m, with

V=Σ_s K_s⊗|s><0|,
H=g(V+V†),
L_s=√κ I⊗|0><s|.

All dissipators act on the ancilla alone. Ancilla dimension and Hamiltonian support are constants when the update is fixed. **The Hamiltonian is not yet two-body if Φ acts on several cells.**

Initialize ancilla in |0>. For arbitrary system state, including a purification by an arbitrary reference, V is an isometry from the ancilla-ground sector into the excited sector. With |u>=|ψ>|0>, |v>=V|u>, the no-emission evolution is exactly

|ψ_no(t)>=a(t)|u>−i y(t)|v>,
a'=−g y, y'=g a−κy/2, a(0)=1,y(0)=0.

The entire no-jump evolution is thus scalar in the protected system/reference degrees of freedom. A first reset jump of type s at time t gives −i√κ y(t) K_s|ψ>⊗|0>. Summing the record s gives exactly Φ, and its time density f(t)=κ y(t)^2 is independent of ψ. Conditioning only on the emission time therefore applies exactly Φ; keeping s gives the usual Kraus instrument. After emission the ancilla is exactly reset, so repetition is an exact renewal process. No g/κ approximation was used.

Writing z=a²,w=y²,c=ay yields
z'=−2gc, w'=2gc−κw, c'=g(z−w)−κc/2.
Laplace elimination gives

E[e^(−sT)] = 2κg² / [(s+κ/2)(s²+κs+4g²)].

For 0<g≤κ/4 put r±=(κ±√(κ²−16g²))/2. Then

T has exactly the distribution Exp(κ/2)+Exp(r+)+Exp(r−),

with independent summands (including the repeated-rate limit at g=κ/4). Hence
E[T]=κ/(4g²)+2/κ,
E[e^(θT)] = (κ/2)/(κ/2−θ) · r+/(r+−θ) · r−/(r−−θ)
for θ<r−.

This gives an exact finite-phase clock suitable for a last-passage scheduling analysis, *if conflicting updates are excluded*. The inverse mean update rate is not precisely 4g²/κ at finite κ. Γ=4g²/κ is only its leading weak-coupling limit.

Numerical checks in renewal_test.py verify the transform, mean and operator closure for a nonunitary amplitude-damping Φ, with an arbitrary complex pure input. They corroborate the algebra, not a many-body threshold.

## 3. Where the construction fails to close the requested bridge
### Overlapping pending updates
For two overlapping gadgets α,β, Hβ generally maps Vα|ψ,0> outside the two-dimensional α no-jump subspace. Even if update superoperators commute, their individual Kraus operators and adjoints need not commute; superoperator commutation does not prove this microscopic closure. The exact renewal lemma applies to isolated or mutually commuting interaction algebras, not an arbitrary overlapping automaton.

One may attach a local busy/lock register and prohibit conflicting starts, but the projectors checking neighboring locks create multi-body controlled Hamiltonians. Assuming such a reliable autonomous lock already exists would assume a decisive part of the target capability. Replacing it with externally scheduled disjoint boxes yields a controlled construction, not the requested autonomous result.

### Thermal resets
For a single two-level ancilla with down/up rates κd,κu, K=κd+κu, second-order elimination yields

L_eff = (4g²κd/K²) D[J] + (4g²κu/K²) D[J†].

This is a leading-order effective expression, not an exact generator for reduced dynamics. The reverse/forward ratio is κu/κd and does not vanish by taking g/K→0 at fixed bath temperature. A bundled m-channel ancilla with each upward rate κu has p0=κ/(κ+mκu), ps=κu/(κ+mκu), coherence decay (κ+mκu)/2, giving forward coefficient 4g²κ/(κ+mκu)² for each D[Ks], and reverse coefficient 4g²κu/(κ+mκu)² for each D[Ks†]. Reverse terms are generally nonunitary perturbations outside the continuous-time theorem of 2601.20818.

### Retained ancilla memory
A reduced-system channel bound for an initially reset ancilla cannot be iterated while silently reinitializing it. Appropriate local boxes must either include the outgoing ancilla as part of the noisy channel, use an explicit physical reset, or keep a memory/process-tensor expansion. Joint endpoint error can be O(g/κ), even when reduced errors start at O((g/κ)²).

### Local observable bounds are weaker
For each fixed time, an N-independent bound on one observable is not the family ||E(I_r)||≤η^r for every marked spacetime set, nor a bound uniform in computation time. Global rapid mixing is also not an innocuous assumption for a long-lived encoded memory.

### Two-body and physical energy interface
The isometric Kraus Hamiltonian retains the full update support. An energy-penalty gadget that reduces its locality must itself preserve a local fault-path bound, including leakage and finite-temperature excitation. Low-energy spectral approximation alone is insufficient for open driven dynamics over arbitrary runtime.

A phenomenological local dissipative reset is a resource, not free entropy deletion. For a physical thermal gap E, detailed balance gives κu/κd≈exp(−βE) in its valid regime. Reset emissions export energy of order E each; at constant event density the total cooling/entropy-export capacity scales with device size. An arbitrary static J⊗σ+ interaction need not be energy-conserving with that reset gap. A drive/work reservoir or a consistent microscopic bath model must be specified; treating a local master equation as exact outside its validity can falsely supply a thermodynamic resource.

## 4. Candidate cluster route — not proved
Take independent fast resets L0 and local Hamiltonian perturbations gVα. A projection onto reset ancillas gives a memory kernel. Each return excursion requires at least two couplings, producing Γ~g²/κ. Connected higher excursions plausibly have support-size weights ~(Cz g/κ)^n; the first genuinely overlapping corrections are fourth order for diagonal reset states and parity-symmetric couplings. Boundary memory costs O(g/κ).

A useful desired theorem would control a **marked connected polymer/process-tensor expansion**, retaining outgoing ancillas, and prove that every set of r marked coarse boxes has total bad norm ≤[C(g/κ+q+δ/Γ)]^(r/b), with fixed overlap exponent b. This formula is a proof target only: neither its powers nor constants are established here. A formal global Feshbach expansion is insufficient since ||ΣVα|| scales with N. One must prove local connected cancellation and summability, including tails across arbitrarily many time boxes.

With bounded g, increasing κ slows correction Γ~g²/κ while ordinary data noise δ continues. Thus arbitrarily strong damping is not a free route to threshold: δ/Γ grows. Any completed compiler must exhibit a nonempty finite parameter window, not merely a formal κ→∞ limit.

## 5. Present conclusion
Established: an exact constant-size, one-body-reset renewal implementation of any CPTP update, including an explicit three-phase waiting law in the overdamped regime. This avoids pretending finite κ creates a simple Markov update error in an isolated box.
Not established: autonomous overlap control, a uniform multi-box coherent fault bound, two-body short-range reduction, or an end-to-end autonomous fault-tolerance threshold with imperfect resets. These are mathematical/physical open steps, not tool-access blockers.
