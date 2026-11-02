# Stronger source: fixed gaps, fixed body cap, every fixed common noise rate

This addendum independently verifies the root-proposed improvement. It supersedes the bath gap/arity caveats of the first construction, while retaining its driven-controller and actual-code contact assumptions. The original is preserved as `CONSTRUCTIVE_ATTACK_v1_preserved.md`.

## 1. Common independent bit-flip noise strictly lowers effective beta more at larger gaps
Let the physical inverse temperature β>0, fixed bit-flip rate q∈(0,1/2), and
 p(E)=q+(1−2q)/(1+exp(βE)),
 β_eff(E)=E^−1 log[(1−p(E))/p(E)].
Write s=1−2q∈(0,1), x=βE/2, and f(x)=atanh(s tanh x). Then β_eff(E)=β f(x)/x and
 f''(x)=−2s(1−s²)tanh(x)sech²(x)/(1−s²tanh²(x))²<0 for x>0.
Since f(0)=0, strict concavity implies f(x)/x is strictly decreasing. Thus for the **fixed gap set {0,Δ,2Δ}**, β_h:=β_eff(2Δ)<β_c:=β_eff(Δ).

## 2. Composite virtual inversion with fixed onsite gaps
Choose the integer m strictly larger than β_c/[2(β_c−β_h)]. For fixed q,β,Δ this is a finite constant independent of n. Use m hot spins of gap 2Δ and 2m−1 cold spins of gap Δ. The battery target is also gap Δ. Define
 A=(hot=1^m, cold=0^(2m−1), battery=0),
 B=(hot=0^m, cold=1^(2m−1), battery=1).
Both have energy 2mΔ. The fresh resource probabilities give upward/downward rates
 a=p(2Δ)^m [1−p(Δ)]^(2m−1),
 b=[1−p(2Δ)]^m p(Δ)^(2m−1),
 log(a/b)=2mΔ(β_c−β_h)−β_cΔ>0.
Both rates may be very small as functions of q, but remain positive n-independent constants. The prior unary-buffer minorization still yields polynomial n resource/time bounds, with q-dependent constants and polynomial exponent. This does not assert a uniform polynomial bound as q→0 together with n.

## 3. Compile the apparent many-body swap using fixed-body exact-charge-conserving gates
Never assume a 3m-body primitive. Let F(x) be the indicator that the resource+battery bit string equals A or B, also requiring the two fixed neighboring unary-wall guards. Use O(m) zero-energy scratch bits and one zero-energy predicate flag.

Build a reversible oracle O_F: |x>|0_scratch>|f> → |x>|0_scratch>|f XOR F(x)> using Toffoli/CNOT gates. It is important to compute the predicate, copy its value to the flag, and **uncompute all temporary scratch BEFORE changing x**. Otherwise old predicate garbage would prevent valid uncomputation after A↔B. All gates targeting scratch/flag commute exactly with K, because their physical bath controls are diagonal energy-basis projectors and all targets have zero energy. Negative controls use |0><0| projectors; no energy-changing physical NOT is used.

Apply O_F. Conditional on flag=1, perform m disjoint triplet exchanges
 |1_hot,00_low> ↔ |0_hot,11_low>.
Partition the 2m low-energy spins into m pairs; the final pair contains the battery target and one cold spin. Each triplet exchange is an exactly resonant 3-body Hamiltonian, or **4-body including its predicate flag**. Every hot spin and low pair is used once. Starting in A, these exchanges produce B; starting in B, they produce A. Their common pulse phase is irrelevant to the diagonal refill channel. All other initial patterns have flag=0 and remain fixed.

The final x still has F(x)=1 on the active sector. Apply O_F again to clear the predicate flag, with scratch again returned to zero. Hence the complete circuit is the desired A/B exchange (up to a common active-sector phase), identity off the selected sector, and reusable clean scratch. It acts correctly on the full physical Hilbert space and every gate conserves K. Unary-sector guards ensure validity is preserved; outside valid unary configurations no correctness claim is needed, but K conservation still holds.

Maximum bath-gate body size is four, independent of q and n. Number of scratch bits, gates, and resources per compiled exchange depends on m(q), not n. The code-contact body size remains its original fixed local-star size, independent of q.

## 4. Initialization, locality, and conditional independence
The O(m) degenerate scratch/flag bits are initially maximally mixed, with clean branch probability 2^−O(m). Common independent Pauli noise leaves them maximally mixed. Combine this with the O(log n) unary-battery branch: total probability is 2^−O(m)n^−O(1), still much greater than exp(−n^η) for every fixed q and η>0. There is no measurement or postselection; this is a positive component in the unconditional initial mixture.

Logical scratch states and flag states can travel along zero-gap thermal wires by SWAPs. Hot and cold states travel on equal-gap wires. Route each required constant-size gate group to a local port, act, and restore/track the SWAP permutation. No wire carrier starts clean. The possibly large m is n-independent; the construction never requires all m spins simultaneously inside one bounded-range gate.

For a unary ladder edge k, route the target bit and its constant-size neighboring guard segment to a fixed port, and restore after the compiled exchange. For the original memory Pauli gate, route the constant-size wall segment to the local code-contact port, together with the flag. This avoids a nonlocal gate between a distant ladder position and the code. Routing overhead is polynomial, bounded-density 3D suffices, and each elementary pulse has bounded strength and fixed local range.

All fresh resource groups start independent of the initial selected workspace branch and all previously used groups. Their conditional probabilities remain a,b because no previous operation touches them (routing permutations track their identities without entangling unused states). Spent resources remain physically present and are never reused as fresh.

## 5. Buffer proof and operational memory caveats
A forward/backward edge sweep has O(L), NOT O(L²), contact stages. For each starting unary position, select a path to the center using the ascending sweep if below and the descending sweep if above. All other stages either act identically or choose a self-loop. Thus the all-start minorization is c^O(L), and L=O(log n) makes it inverse polynomial. Conditioning on successful previous code gates may change the battery distribution arbitrarily; uniform mixing handles every such distribution. π/2 exchanges and diagonal initial baths preserve syndrome/battery classical blocks, while the logical subsystem may retain arbitrary coherence.

For the cleanest logical-error lower bound, allow zero preparation noise on memory and common q on the constant-density resource bath (and, if desired, all ordinary bath carriers). Begin with exact encoded logical |0>, or an encoded half-Bell pair with the admitted thermal syndrome/gauge state. The completed Pauli path is logical X independently of the initial syndrome. This avoids presuming an unproved robustness theorem for memory preparation noise. Extending the claim to an identical nonzero noise rate on every memory carrier is a distinct task requiring a quantitative decoded-initial-state estimate.

## Conclusion
For any fixed common q∈(0,1/2) on the resource bath, the fixed bath gap set {0,Δ,2Δ} and fixed-body exactly K-conserving gates suffice for the prior polynomial-time attack. No q-dependent large onsite gap or q-dependent native body cap is necessary. The protocol remains explicitly driven; no static autonomous clock/controller has been constructed.
