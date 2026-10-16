# Independent audit of grouped endpoint-subset bounds

Date: 2026-10-15. Mathematical/circuit-model analysis only; no Willow or other experimental outcomes were opened. Audited the grouped argument in ../joint/REPORT.md and the singleton endpoint theorem in INDEPENDENT_ENDPOINT_SUBSET_PROOF.md.

## Verdict
**The grouped finite-dimensional positive block-norm comparison and its endpoint effect inequality are valid under the precise group-incidence and initial-sector assumptions below.** The displayed beta constant and scalar transient formula are correct. The exponential simplification needs beta > 0; the finite matrix comparison itself does not. This proves neither a common-decoder threshold nor protection of logical information within a syndrome sector.

Scope: bounds joint endpoint syndrome changes on selected guard regions.

## 1. Required assumptions
Let the selected commuting binary checks be partitioned into groups i. Group i has at most d_i labels (one can safely take d_i=2^{k_i}, including unused labels). Denote a joint syndrome by a=(a_1,...,a_m), with projectors P_a. The finite joint Hilbert space includes the persistent bath; any reference may be included as well. Empty or unequal-dimensional syndrome subspaces cause no problem.

The Hamiltonian must admit H(t)=H_0(t)+sum_i V_i(t), with:

1. H_0 preserving every selected syndrome block.
2. V_i changing only group i. Equivalently, it commutes with every selected check outside group i. Its nonzero full-syndrome transition blocks can connect a and c only when a_j=c_j for j≠i.
3. After its full-syndrome diagonal part is absorbed into H_0, **every off-diagonal transition block** P_a V_i(t) P_c has operator norm at most J_i, uniformly in t and the other group labels.
4. Check dephasing is the actual Lindblad generator sum_j gamma_j (Z_j rho Z_j-rho), with fixed nonnegative rates. For each group, gamma_i below means a lower bound on every constituent check rate, normally their minimum. A difference in any one check then damps an off-diagonal group block by at least 2 gamma_i.
5. The initial state is supported in a known recorded joint selected syndrome. It can be arbitrarily entangled with the bath/reference. A coherent superposition across initial selected syndromes is not covered by the same initial-condition argument.
6. Hamiltonians are Hermitian with well-defined propagators and bounded stated transition strengths. Time dependence is allowed. The model does not include unaccounted measurements, corrections, feedback-dependent private clock trajectories, or extra dissipators that transfer selected syndrome populations.

Terms changing two retained groups are forbidden, regardless of geometric locality. Large terms that commute with every retained check may be put in H_0. Other commuting-check dephasers can be conditioned on their random-unitary trajectories if the underlying generator really has the specified form; this is not permission to replace arbitrary dissipation by dephasing.

### Norm distinction
A pre-removal bound ||V_i||≤J_i is sufficient for every transition block, since projections are contractions. Diagonal removal need not preserve ||V_i||, and no such claim is needed. Conversely, a per-transition bound J_i is **not** generally a whole-operator bound J_i: the number of allowed transitions matters and is charged in the d-dependent constants. If many Hamiltonian terms contribute to one transition, J_i must bound their total block; summing their individual norms is safe. One cannot assign J_i to each summand and then charge the combined transition only once without summing.

## 2. Block comparison and factorization
For rho_ab=P_a rho P_b, define x_ab=||rho_ab||_1. The H_0 propagator acts as U_a rho_ab U_b^dagger, preserving the rectangular block trace norm. Dephasing multiplies this block by exp[-D_ab(t-s)], where D_ab=2 sum_j gamma_j 1[a_j≠b_j]. Left/right multiplication by a transition block has trace-norm operator bound J_i. Duhamel and the triangle inequality therefore give a positive convolution inequality involving the two possible branch transitions, with no commutation or factorization of bath operators.

Replace every allowed within-group label transition by coefficient J_i, and if desired replace actual damping by its lower bound 2 gamma_i on each unequal pair. The scalar matrix M is Metzler. It can be chosen as a Kronecker sum of matrices M_i on local density-block labels (a_i,b_i):

- diagonal: minus the group's damping rate;
- ket-label change a_i→c_i≠a_i: coefficient J_i;
- bra-label change b_i→c_i≠b_i: coefficient J_i.

Positive Volterra iteration yields x(t)≤exp(Mt)x(0). Initially there is a single nonzero norm entry, equal to one. Summing diagonal target entries for which every selected group differs from its own initial label gives

  Pr[every selected group changes at the endpoint] ≤ product_i q_i(t),
  q_i(t)=sum_{a_i≠a_i^0} [exp(M_i t)]_{(a_i,a_i),(a_i^0,a_i^0)}.

It is the **comparison matrix** that factorizes, not the physical channel, bath state, or Hamiltonian. Diagonal dependence of V_i on other groups and shared noncommuting bath couplings are allowed. Constraints among physical syndrome labels can only remove accessible blocks; padding with unused labels is conservative.

## 3. Exact counts and scalar constants
For one d-label group let A be the sum of comparison diagonal entries and B the sum of off-diagonal entries. Count outgoing branches from each source:

- each off-diagonal source has two diagonal targets, contributing 2J to A;
- each diagonal source has 2(d−1) off-diagonal targets;
- each off-diagonal source has 2(d−2) off-diagonal targets, besides damping at least 2gamma.

Thus

  A'=2JB,
  B'≤2(d−1)JA−beta B,
  beta=2gamma−2(d−2)J,
  A(0)=1, B(0)=0.

Comparing to equality, the upper solution satisfies A_bar''+beta A_bar'−4(d−1)J² A_bar=0, with A_bar(0)=1 and A_bar'(0)=0. Therefore

  A_bar(t)=exp(−beta t/2)[cosh(omega t)+(beta/(2omega))sinh(omega t)],
  omega=sqrt(beta²/4+4(d−1)J²).

The initial diagonal comparison component never decreases below one, hence q_i≤A−1≤A_bar−1. This is a conservative subtraction, not a physical normalization claim. The expansion is

  A_bar(t)−1 = 2(d−1)J²t² − (2/3)beta(d−1)J²t³ + O(t⁴).

In particular the reported quadratic coefficient 2(d−1) is correct. The actual local changed-label majorant starts at (d−1)J²t², so this scalar reduction already loses a factor of two at leading order. For d=2 with uniform damping, A_bar−1 equals exactly twice the sharper singleton q^+; use the singleton formula where available.

For beta>0, A_bar is nonnegative and increasing, and its Volterra equation gives

  A_bar'(t) = 4(d−1)J² integral_0^t exp[−beta(t-s)]A_bar(s) ds
             ≤ [4(d−1)J²/beta] A_bar(t).

Consequently q_i≤exp[4(d−1)J²t/beta]−1. If gamma>0 and gamma≥2(d−2)J, then beta≥gamma>0, giving exp[4(d−1)J²t/gamma]−1. For d=2, the condition gamma≥0 alone is insufficient to justify the division: explicitly require gamma>0 for this simplified formula. For J=0, the event factor is zero, by continuity without evaluating 0/0.

### Zero/weak damping
The finite Metzler bound and the A_bar transient remain valid even at beta=0 or beta<0. At beta=0, A_bar=cosh(2sqrt(d−1)Jt). At gamma=0,d=2 this gives q≤cosh(2Jt)−1, while the sharper singleton bound is sinh²(Jt). For gamma=0,d>2 the transient is still finite but does not establish dephasing-improved J²/gamma scaling. No negative or zero denominator should be substituted into the exponential simplification. If d=1 the changed-label event is impossible and the factor is zero; omit that trivial group rather than applying unnecessary singular formulas.

## 4. Actual CP effect with arbitrary shared bath
Let Phi_t be the genuine joint CPTP evolution, F the projector for the stated endpoint event, and P_s the initial selected-syndrome projector. For every normalized density operator supported in P_s, including every pure bath-entangled vector, the proof bounds Tr[Phi_t(rho)F] by Q=product_i q_i. Thus the quadratic-form criterion implies

  P_s Phi_t^*(F) P_s ≤ Q P_s.

The effect Phi_t^*(F) itself is positive and at most identity because Phi_t is CPTP and 0≤F≤I. The comparison map exp(Mt) is not being claimed to be a physical CP map. The operator inequality is restricted to the initial sector; it is not an unrestricted bound on Phi_t^*(F) over other initial sectors. Uniformity in bath/reference dimension and initial state is genuine under the finite-dimensional bounded assumptions. It does not establish the corresponding infinite-dimensional/unbounded-generator theorem without additional analytic hypotheses.

Actual final measurements and subsequent conditional states permit serial use of this effect bound when each next interval starts in its recorded sector and all interval hypotheses still hold. Imaginary intermediate measurements cannot be inserted into an unmeasured evolution. Adaptive corrections, unbounded controls, or changing support incidence need their own verification before such iteration.

## 5. Why individual caps are legitimate
Let R retain only groups with an applicable q_i<1. The full all-groups-changed event is contained in the all-R-changed event. Each dropped V_j commutes with every retained check, so it can be included in the new H_0. For a retained group, combining dropped labels into its environment does not enlarge a transition bound: V_i is block diagonal in those dropped labels, so the combined block norm is the maximum of its constituent block norms, still at most J_i. Subsequent H_0 interaction-picture unitaries preserve that bound.

Reapply the theorem on R to obtain product_i min(1,q_i). The same argument applies to valid scalar upper factors, although the finite-matrix q_i are tighter. It is essential that dropping groups preserve the support and uniform norm hypotheses. Taking min(1,Q) on a single proved total product is always possible; replacing each factor by a smaller separately proved one-event bound is **not** generally valid without another product proof.

## 6. Failure boundaries and missing decoder support
- A term J X_1 X_2 changes two singleton groups and produces a joint endpoint probability J²t²+O(t³), whereas a product of two singleton quadratic factors is O(t⁴). This explains why incidence, not a casual assertion of locality, is indispensable.
- Syndrome-preserving H_0 may implement a damaging logical operator with arbitrarily large norm. Small endpoint syndrome-change probability is not itself small logical error or protection of a memory.
- Endpoint cancellation can hide multiple within-interval excursions. The theorem supplies no positive local fault-history decomposition and no all-subset bound on intermediate support births.
- Common-decoder threshold use still needs a proved mapping from allowed physical interactions and measurement/correction operations to space-time fault supports; coverage of overlapping stabilizers; a valid instrument or history interface through corrections; logical-action control for syndrome-preserving terms; and the decoder's required all-subset bounds at the relevant coarse-grained scale. A bound for sufficiently separated guard groups alone does not supply these.
- No claim of sharpness, new fault-tolerance theorem, physical feasibility of independent dephasing clocks, or novelty relative to existing strong-damping/non-Markovian fault-path techniques follows.

## 7. Independent numerical checks
Own script grouped_independent_check.py constructs three 4-label × 2-label group systems with a shared two-dimensional bath, noncommuting random transition blocks, and arbitrary syndrome-dependent bath Hamiltonians. It checks all eight initial group sectors at two times, giving 48 exact Lindblad endpoint-effect eigenvalue checks. These maximize over the entire initial bath subspace rather than a chosen bath vector.

All pass the finite-matrix product, scalar transient, and exponential bounds. Maximum physical effect / matrix-product bound: 0.4102167569705799. Per-transition J_1=0.15, while whole ||V_1|| ranges from 0.31998590874522803 to 0.34986796123773517, directly exercising the distinction between block and whole norms. Separate matrix counting checks for d=2,4,8 with heterogeneous check rates verify the A/B identities and inequalities entrywise. Results are in grouped_independent_check.json. These finite checks support implementation algebra only; the argument above supplies the proof.
