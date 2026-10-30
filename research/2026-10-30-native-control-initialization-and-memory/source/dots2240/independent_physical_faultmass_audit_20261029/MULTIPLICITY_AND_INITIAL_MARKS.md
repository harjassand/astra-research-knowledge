# Physical-window fault MASS: factorial and exponential moments

2026-10-29. Uses all definitions and hypotheses in `ANCESTOR_WITNESS_THEOREM.md`, including genuine additive Poisson CPTP kicks, actual reset records, and epsilon J_R(D−1)≤r/2. Let rho=r/2 and

C_A=D alpha^−1 nu_0(Delta+1/rho).

This strengthens binary-cell occupancy to a count/multiplicity law. It does not assert any DATA-channel factorization.

## 1. Count distinct ancestors, not apparently independent emissions

For a finite cell set V of ONE witness-support color, let Y_V be the TOTAL NUMBER of marked terminal/abort reset emissions in V, allowing arbitrarily many per cell. Let A_V count the distinct physical last-kick ancestors of those emissions. Deterministically,

Y_V≤b A_V.

For each ancestor choose exactly one of its selected descendant emissions in V (use any deterministic ordering of cells and then emission time). For k distinct selected ancestors these representative emissions are distinct. Their shortened ancestor-to-cell-start survival intervals are disjoint for each repeated owner. Therefore the time-dependent product-witness estimate applies with k intervals and k prescribed kick insertions.

Using the ordered Poisson factorial expansion and summing each representative's destination over V yields

E[(A_V)_k] ≤ (epsilon C_A |V|)^k,       k≥0,        (1)

where (A)_k=A(A−1)...(A−k+1).

Detailed accounting: each representative contributes alpha^−1; each distinguished kick contributes D; its source/time integral summed over V is bounded by nu_0(Delta+1/rho)|V|. Unselected kicks remain in the noisy killed semigroup with rate rho. On valid assignments the witness intervals have disjoint interiors for any repeated owner. Only after using their bound do we enlarge to unrestricted nonnegative integrals; this enlargement factorizes the k integrals. The destination-cell sum allows repeated cells, so (1) genuinely includes multiplicity. Distinct ancestors use a factorial measure, not an ordinary kth power of the Poisson count. The case k=0 is 1.

### Explicit repeated-cell integrand check

Fix ordered distinct ancestor points (e_i,tau_i), i=1,...,k, and assigned representative cells v_i∈V, with repeated cells permitted. Let E(tau,v) be the actual record event that each inserted point is an ancestor whose canonical representative lies in its assigned cell. On this event representatives of different ancestors are distinct resets. Define Disj(tau,v) to mean that the nonempty shortened intervals [tau_i,s_(v_i)] have disjoint interiors whenever their owners coincide. Then

1_E = 0 whenever Disj(tau,v) fails,
P_insertion(E) ≤ 1_Disj alpha^−k D^k exp[−rho sum_i(s_(v_i)−tau_i)_+]

when all source-incidence/time-before-cell-end conditions hold. This is an event-inclusion bound, not a claim that endpoint existence follows from survival.

Why disjointness is necessary: if two emissions of the same owner occur in order u_i<u_j, then the later last-kick ancestor satisfies tau_j>u_i (otherwise the reset at u_i would have cleared its mark). Since u_i≥s_(v_i), its interval ends before tau_j. In particular, if both assigned cells are the SAME cell, at most one of their ancestors lies before its start; all later ancestors lie inside the cell and have empty shortened intervals. This explicitly handles repeated owner/cell labels.

Now sum the fixed-event bound and apply the Poisson factorial expansion. Dropping the nonnegative disjointness indicator enlarges the resulting integral; the larger integral factorizes. We NEVER apply the survival lemma to an invalid overlapping-interval assignment. No reset-time density or reset-rate factor is required because A_V counts distinct kick points with descendants, not the factorial moment of emission times. Every emission multiplicity is finally bounded by Y_V≤b A_V.

Equivalently, (1) follows by expanding the record-event CP instrument into selected distinct ancestor points. Uniformity of the operator survival bound means the factorial-moment inequality holds for every initial quantum/reference input, without conditioning on any future reset record.

Expand the nonnegative binomial series to get, for every z≥0,

E[(1+z)^(A_V)]
 =sum_(k≥0) z^k E[(A_V)_k]/k!
 ≤exp(epsilon C_A |V| z).

Hence, for every theta≥0,

E exp(theta Y_V)≤exp[epsilon C_A |V|(exp(b theta)−1)].       (2)

The bound is valid for arbitrarily late, disconnected sets V; ancestors before those cells are included all the way back to the initial time. No stationary-delay or fresh-at-block-boundary assumption is made.

## 2. All spatial colors

Partition a general finite V into P color classes V_c and write Y_V=sum_c Y_(V_c). Their counts can be arbitrarily correlated. Holder's inequality, not independence, gives

E exp(theta Y_V)
 ≤product_c {E exp(P theta Y_(V_c))}^(1/P)
 ≤exp[epsilon (C_A/P)|V|(exp(bP theta)−1)].                (3)

An empty color class contributes 1. This is an extensive bounded-cluster exponential moment, with constants independent of time/volume. It is stronger than a binary occupancy estimate.

For prescribed positive integer multiplicities m_v on distinct cells v∈V, put m=sum_v m_v. The event Y_v≥m_v for all v implies Y_V≥m and |V|≤m. Set H=C_A/P and B=bP. If epsilon H≤1, choosing exp(B theta)=1/(epsilon H) in (3) gives

P(Y_v≥m_v for every v∈V)
 ≤[e (epsilon H)^(1/B)]^m.                              (4)

The estimate is useful when its bracket is <1. It supplies a local-stochastic MASS law, not just at-least-one occupancy. The corresponding CP record-event instrument has diamond norm bounded by the same expression. One can again rewrite epsilon H=(epsilon Delta)(H/Delta).

## 3. Add direct physical-kick insertion mass

Suppose each physical CPTP kick contributes at most a direct fault-mass units to a bounded collection of physical cells at its occurrence. For the chosen physical-cell interface assume the rate measure of kick points which can contribute direct mass to V is ≤epsilon nu_dir Delta |V|. This is the usual bounded spatial incidence condition; it must be verified for the proposed dressed-insertion support convention.

Then X_V, the direct insertion mass in V, is bounded by a Poisson count times a, and

E exp(theta X_V)≤exp[epsilon nu_dir Delta |V|(exp(a theta)−1)].

X_V and Y_V are NOT independent: the very same kicks may contribute to both. A further Holder step gives

E exp[theta(X_V+Y_V)]
 ≤exp{epsilon |V|/2 [nu_dir Delta(exp(2a theta)−1)
                    +(C_A/P)(exp(2bP theta)−1)]}.          (5)

Let B_tot=2 max(a,bP) and H_tot=[nu_dir Delta+C_A/P]/2. Then the right side is at most

exp[epsilon H_tot |V|(exp(B_tot theta)−1)].               (6)

Thus for prescribed positive integer TOTAL fault masses m_v and m=sum m_v,

P(X_v+Y_v≥m_v for every v∈V)
 ≤[e (epsilon H_tot)^(1/B_tot)]^m,                        (7)

when epsilon H_tot≤1. This is a concrete physical-window CP faultmass envelope with a power loss, not an assertion that marked emissions already are valid bounded-arity faulty DATA maps. If the latter factorization is established independently, (7) is an appropriate record-weight interface to combine with it.

## 4. Initial marks and block-boundary correlations

All noise-vanishing formulas above assume marks are zero at the global initial time. They DO allow arbitrary quantum state and arbitrarily late target windows. In particular, at the beginning of a late block, residual marks may be correlated with the current data, locks, and forthcoming emissions. The proof never resets those marks analytically; it retains their actual earlier kick ancestors. Therefore applying (3) or (5) to a late V does not invoke fresh independence.

These statements are NOT uniform conditional bounds after observing an arbitrary rare past record: such a record can reveal many surviving marks. A restart at a deterministic boundary must carry an initial-mark term.

For a specified initial marked set M0, any marked reset whose last cause is an initial mark rather than a post-boundary kick can occur at most once per owner. Let I_V count those emissions. Then deterministically I_V≤|M0|. The proof of (1)–(3) for post-boundary kick ancestors remains uniform over the initial quantum state and initial marks, since their passive annotations do not affect physical dynamics. Consequently the simple rigorous restart bound is

E exp(theta Y_V)≤exp(theta |M0|)
                exp[epsilon (C_A/P)|V|(exp(bP theta)−1)]. (8)

For random initial marks correlated with quantum state, replace exp(theta |M0|) by its expectation: the bound is uniform within each classical mark sector. This is an unconditional ensemble statement; it does not assume mark/data independence.

### Optional burn-in improvement

If every target cell starts at time at least u after the restart, any descendant of an initial mark must have no designated reset during [0,u]. For a same-color subset of initial owners, the actual noisy product witness gives joint survival ≤alpha^−k exp(−rho u k). Therefore, with m0=|M0|,

E exp(theta I_V)
 ≤[1+alpha^−1 exp(−rho u)(exp(P theta)−1)]^(m0/P).         (9)

Proof: expand the Bernoulli survival product for each color, then use Holder over colors. Counting only actual emissions in V is dominated by counting survivors to u. The coarse prefactor alpha^−1 may exceed one at small u; the bound remains valid, albeit loose.

Initial descendants and post-restart kick descendants may be correlated. Combine their moments by Holder, for example

E exp(theta Y_V)
 ≤[1+alpha^−1 exp(−rho u)(exp(2P theta)−1)]^(m0/(2P))
   exp[epsilon (C_A/(2P))|V|(exp(2bP theta)−1)].          (10)

This gives an explicit burn-in term instead of fictional fresh marks. For random M0, average the first factor using its actual initial distribution (uniform conditional quantum bounds justify this); no factorization of M0 from quantum data is needed.

## 5. What this supplies and what remains

Supplied: an actual-record, finite-physical-time local-stochastic MASS envelope for direct kicks plus delayed marked reset emissions, including many overlapping kicks, arbitrary per-cell multiplicity, correlated delays, and a correct initial-mark interface.

Not supplied: identification of each marked reset with an ordinary faulty DATA instrument; control of in-flight histories at an SSF block boundary; a serialization of overlapping quantum transactions; or any quantum-memory threshold. The probabilistic envelope can be used only after those separate semantic requirements are established.
