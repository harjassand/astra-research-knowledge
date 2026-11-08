# Status update

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

The current repaired theorem and remaining all-time boundary are summarized in REPORT.md. This file retains the original algebra and exploratory estimates. Any word-identity/source-extension discussion here is superseded by FIRST_DISCOVERY_PROOF.md for at-most-two-body interactions.

# Exact boundary-switch activities for noisy Hamiltonian marginals

8 November 2026. Work in progress. The algebraic expansion below is exact. The later proposed hypercontractive response estimate is an unproved transfer target, not a sampler theorem. The independently audited finite-patch lemma remains unchanged in the sibling b_many_region_transfer_20261108 directory.

## 1. Exact local normalization and polymer algebra

Partition the physical lattice into blocks. Keep the entire within-block Hamiltonian and all original on-site replacement noise in a baseline generator L_0. Let E be the coarse adjacency graph; each e groups all physical Hamiltonian terms crossing that block boundary. For B subset E, L_B retains exactly those crossing groups in B, without changing any internal Hamiltonian, input state or noise rate.

The initial state is a supplied product across physical sites and hence across blocks. Fix any terminal computational-basis marginal. In block v, let P_v be its marginal effect (identities on unmeasured sites), let b_v count measured sites, and set A_v=2^{b_v}P_v. For a finite vertex set W and boundary subset B supported in W, define

    G_W(B)=Tr[(product_(v in W) A_v) exp(T L_B)(rho_W)].

All internal terms and noise in W remain present. Unmeasured blocks have A_v=I. Put z_v=G_{v}(empty). These are actual normalized one-block marginal probabilities. At positive T with replacement noise they are positive. The audited g=1 bound, when its physical-time conditions hold, strengthens this uniformly to

    1-e^{-c_0} <= z_v <= 1+e^{-c_0},                 (1)

for every measured subset and outcome. Thus no exponentially small global prefix mass is divided into an additive error. The physical probability's known powers of two will be kept separately.

For a nonempty connected edge set C, let V(C) be its incident block vertices and define the activity

    w(C)= [sum_(B subset C) (-1)^{|C|-|B|} G_{V(C)}(B)]
                      / product_(v in V(C)) z_v.     (2)

Connectivity here refers to the coarse edge set. Two such polymers are compatible when their vertex sets are disjoint, even if unused edges connect those vertex sets in the full lattice.

**Exact identity.** For the full coarse graph,

    G_V(E)/(product_v z_v)
       = sum_(vertex-disjoint polymer collections C_1,...,C_k)
                         product_i w(C_i).          (3)

The empty collection contributes one.

**Proof.** Boolean Möbius inversion gives G_V(E)=sum_(C subset E) Delta_C G_V(empty), where Delta_C is the alternating sum over B subset C. For a fixed C, every B subset C has no Hamiltonian interactions between different connected components of C. Both the initial state and terminal effect factor, and the baseline generator is a sum of independent block generators. Therefore the alternating sum factors over C's connected components. Each isolated block contributes z_v. Dividing by the product of all z_v yields (3). This is exact factorization of switched Hamiltonians, not a declaration that separated regions of the actual full dynamics have disjoint backward light cones.

The original marginal equals 2^{-sum_v b_v} (product_v z_v) times the right side of (3). Its logarithm, if an absolutely convergent activity expansion is earned, can be evaluated without directly representing an exponentially small probability.

## 2. Paid local work

A polymer with v vertices and e edges involves only v physical blocks. In a bounded-degree coarse graph e=O(v). Equation (2) requires at most 2^e finite-patch evolutions. If each block has a sites, direct exact-reference arithmetic costs exp(O(av)), times a polynomial in paid input bits, numerical action and requested logarithmic precision. Taking a tiny global prefix probability as an input denominator is unnecessary; (1) bounds every local normalization away from zero.

This is not yet an efficient global algorithm. If one proves an appropriate uniform Kotecky-Preiss bound and needs only v=O(log(n/epsilon)), connected coarse edge sets can be enumerated in n exp(O(v)), giving polynomial dependence on n and 1/epsilon at fixed a. The exponent can be enormous. Without convergence and a rigorous tail bound, truncating (3) has no certified relative error and cannot be called a sampler.

## 3. Dense-mark contributions are controlled by the audited patch lemma

Write A_v=I+M_v. The numerator of (2) expands into terms indexed by marked subsets S subset V(C):

    Delta_C G = sum_S sum_(B subset C) (-1)^{e-|B|}
           Tr[rho Phi_B(product_(v in S) M_v)].       (4)

Every activated-edge subset B obeys the same local-strength and replacement-noise bounds. If s=|S| is at least eta v for a fixed eta>0, pad disconnected components with decoupled identity sites as needed. The total finite patch has N<=O(a v)<=O(a/eta)s. The existing many-region lemma then bounds each moment by exp(-c s), provided its physical-time conditions are applied with that actual N/s bound.

Consequently a deliberately crude dense-mark contribution is at most

    2^{e+v} exp(-c eta v).                           (5)

All factors are paid. The constants c and the block radius must be chosen jointly; merely setting c large while holding the earlier physical time unchanged is invalid.

## 4. The precise sparse-mark transfer target

For s<eta v, equation (5) loses its size-v decay. Yet the edge difference Delta_C requires sensitivity to every boundary in C, including boundaries far from the marked input blocks. The desired estimate must control these simultaneous sensitivities even when operator support travels out and back, so a final-support tail alone is not sufficient.

A useful representation introduces one conserved classical switch bit per coarse edge. Conditional on switch values sigma, the physical Hamiltonian is the corresponding H_B. Operators remain block diagonal in these switch variables. The coefficient of the product of all switch Z variables is exactly 2^{-e} Delta_C Phi(M_S). This converts repeated boundary use into a Fourier coefficient, without declaring different histories a positive mixture after cancellation.

A promising but NOT YET PROVED lemma would strengthen the many-commutator response estimate from equal Schatten exponents to p-to-q hypercontractive exponents. The proposed mechanism is:

1. In the source's irreducible-path resummation, retain every physical depolarizing term in each reducible propagator; remove only the Hamiltonian terms specified by the path equivalence class.
2. Each resulting physical propagator is hypercontractive. Increase the exponent continuously as p(t)=1+(p(0)-1)exp(2 gamma t). Local commutator insertions have the same 2||H_e|| bound in every Schatten norm.
3. With K conserved classical switches, per-switch-branch hypercontractivity loses at most 2^{K(1/p-1/q)} when passing between normalized direct-sum norms. Those factors telescope over successive time intervals.
4. Taking p=1+1/a and q=1+a makes ||M_S||_{p,tau}<=3^s, rather than ||M_S||_infty roughly 2^{a s}. The final physical norm conversion on av sites costs only 2^v, while K=O(v) contributes another exp(O(v)) factor.

If this response bound also retains a product of spatial tails for a positive fraction of well-separated boundary groups, it may make (4) absolutely small in v at fixed physical time. This is a target, not an established implication.

### Two material proof obligations

**Noise retention in the exact resummation.** On-site replacement is diagonal in physical Pauli coefficients and does not create support or switch dependence. This suggests it may be retained in every reducible propagator. However, an exact identity for the equivalence classes with those dissipators must be written and checked, not inferred just from contractivity or from a Pauli-jump trajectory that has discarded hypercontractivity.

**Shared-switch geometry.** One switch controls a whole coarse boundary containing O(r) physical terms. Assigning an ordinary control qubit to all those terms creates artificial long-range edges or O(r) degree in a naive tensor-product interaction graph. Using one switch per physical bond instead costs K=O(rv), which can erase the gain. A valid response proof must exploit that the switches are central classical coefficients: Hamiltonian terms with disjoint physical supports still commute even when they share a switch variable. The boundary probe changes only terms on its actual physical boundary. Extending the path proof to this classically valued local algebra requires proof; treating it as an ordinary local ancillary Hamiltonian is not justified.

## 5. Status

Equation (3), local normalization and the work needed to evaluate each finite activity are established algebraically. Equation (5) uses the independently audited finite-patch result at its actual parameters. The sparse-mark response bound and its two obligations remain under investigation. No Kotecky-Preiss criterion, global zero-free region, relative/log evaluator, or full-output sampler is claimed here.

## 6. Executed exact-algebra diagnostic and a failed truncation

`check_edge_mobius.py` assembles the full Lindblad output for all sixteen switched boundary sets of a noncommuting four-qubit square. It checks full outcomes and partial marginals in three physical parameter cases. Möbius component factorization and exact compatible-polymer reconstruction agree to at most 1.55e-14. This is a floating diagnostic of the separately proved identity, not interval certification.

The same test deliberately keeps only polymers involving at most two block vertices, without a convergence certificate. At gamma=0.1, T=1.4 and full outcome1000, that truncation is approximately -0.213439, while the exact normalized partition function is +0.225402. Thus exact compatibility does not make arbitrary activity truncations positive or accurate. The physical states have positive eigenvalues in all executed cases. No simulation advantage is inferred.

## 7. Time dependence is another paid boundary

Even if the proposed activity bound were proved, taking spatial block radius r=Theta(hT) and computing every activity by dense finite-patch evolution costs exp(O(r^2 v)) in two dimensions. A cluster cutoff v=O(log(n/epsilon)) would be polynomial only at each fixed numerical physical time and coupling ratio, with a time-dependent exponent. Letting T grow to the entropy-mixing cutoff O(log(n/epsilon)/gamma) would generally make this cost quasipolynomial; a faster activity evaluator or a time-uniform invariant would still need proof.

One cannot simply simulate a final constant-length interval with a new product input. The actual earlier state is correlated, and the exact switched-graph factorization in Section1 used the original product input. Replacing that state would change the problem. Any eventual all-time claim must pay this dependence or establish an additional composition/late-time argument.

## 8. A valid hypercontractive response lemma without spatial improvement

There is a rigorous intermediate bound that does not require switch registers or the unproved resummation extension. It keeps the input normalization small, but by itself has no useful large-coupling spatial decay.

Let H(lambda)=H_0+sum_(e in C) lambda_e V_e with 0<=lambda_e<=1, and retain the original every-site noise. Let Phi_lambda(T) be its Heisenberg semigroup. For 1<p<=q and exp(2gamma T)>=(q-1)/(p-1), the exact finite difference obeys

    ||Delta_C Phi(T)(M)||_(q,tau)
       <= (2T)^|C| product_(e in C)||V_e||
                                  ||M||_(p,tau).    (6)

**Proof.** The mixed derivative with respect to the distinct lambda_e is a sum over all |C|! orderings of commutator insertions i[V_e,.], integrated over a time simplex of volume T^|C|/|C|!. Between insertions the full propagator at the same lambda is present, with all original noise. Assign the increasing exponent p(s)=1+(p-1)exp(2gamma s) along the physical time. Every intervening propagator is hypercontractive between its two endpoint exponents; every insertion costs at most 2||V_e|| in the instantaneous Schatten norm. The factors multiply, the permutation count cancels the simplex factorial, and exponent monotonicity permits any smaller final q. Integrating each lambda from zero to one gives the finite difference and (6). There is no inverse channel, positive-trajectory assumption or rare-probability division.

For a polymer with v blocks of at most a sites, choose p=1+1/a, q=1+a and gamma T>=log a. Its full normalized projector product M=product A_v satisfies ||M||_(p,tau)<=2^v. Converting the output q-norm to operator norm costs at most another 2^v. Hence the exact normalized activity obeys the paid bound

    |w(C)| <= [4/(1-e^{-c_0})]^v
                  (2T)^|C| product_e ||V_e||.        (7)

The same bound with source 3^s applies to a centered marked subset, with the corresponding physical dimension conversion retained.

Equation (7) alone does not prove convergence for the target strong two-dimensional interactions. A coarse interface generally has ||V_e||=O(hr), so its action factor can be large. The still-missing spatial response bound must improve this action estimate for the many distant interfaces of a sparse marked subset without losing the p-to-q gain. Interpolating a separate equal-exponent locality estimate with (6) generally weakens the spatial exponent when p is near1 and q is large; merely quoting both estimates is not a proof of their simultaneous use.

## 9. Prior credit and audit boundary

Boolean Möbius inversion, linked-cluster factorization, Duhamel differentiation and hypercontractivity are established mechanisms. Numerical dynamical linked-cluster methods predate this work; for example Mallayya and Rigol, Phys. Rev. Lett.120,070603 (2018), https://doi.org/10.1103/PhysRevLett.120.070603 . Wild and Alhambra, PRX Quantum4,020340 (2023), https://arxiv.org/abs/2210.11490 , prove short-time dynamical cluster-expansion algorithms. These sources do not by themselves establish the proposed all-strength noisy activity decay. The known noisy-circuit comparator remains Nelson et al., https://arxiv.org/html/2610.00548v2 ; its result is not being claimed again as a continuum theorem.

The exact boundary-switch algebra and local denominator accounting have an independent proof in ../b_global_activity_audit_20261108/REPORT.md. The reviewer independently derived the normalized mixed-response bound (6). Their earlier audit of the finite-patch lemma does not endorse the pending simultaneous spatial-hypercontractive resummation. No historical-first or practical-performance claim is made for the exact algebra or the derivative estimate.
