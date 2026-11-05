# Independent literature and priority audit

Checked 5 November 2026. This audits literature priority and scope, not the correctness of the new n=18 certificate.

## Assessment

The 19-qubit code is established prior art, including a computer-assisted exact-existence statement in 2023. The proposed substantive advance is exclusion of all complex rank-two codes at n=18, hence the exact minimum 19. I found no earlier unrestricted n=18 exclusion in the primary sources below or the focused current searches. This is a bounded search result, not a guarantee of novelty.

The weaker bracket 18 <= n_min <= 19 is already implicit in older published work: Okada tabulates the applicable SU(2) linear-programming bound, while Aydin–Alekseyev–Barg provide the upper bound. New exact rational certificates below 18 make that known bound independently replayable, rather than establish a new lower bound.

## Primary sources and exact scope

### Aydin–Alekseyev–Barg: existence at 19, not an unrestricted minimum theorem

- First preprint: 9 October 2023, https://arxiv.org/pdf/2310.05358v1 .
- Published: Quantum 8, 1321, 30 April 2024, https://doi.org/10.22331/q-2024-04-30-1321 .
- Current source: v3, 15 April 2024, https://arxiv.org/html/2310.05358v3 .

Section 7, Eq. (32), Proposition 7.1 restrict to odd n, real coefficients, even/odd Dicke support, and complementary logical words. The last part of that section exhibits the 19-qubit distance-five code via nine quadratic equations. Its displayed coefficients are approximations, but the authors say msolve produced intervals containing an actual solution. The same example and interval statement are already in v1, printed pp. 18–19. The local positive-control code is a reconstruction of this known code.

The sentence asserting that t=2 has no shorter code follows the restricted Proposition 7.1 discussion; no unrestricted complex/even-n no-go proof is supplied there. It should not be cited as a theorem excluding the present n=18 problem. Conversely, it should be acknowledged as an earlier restricted minimality assertion, not omitted.

### Okada: older applicable lower bound and explicit failure at 18

Rui Okada, December 2023 dissertation, posted 20 February 2025, https://arxiv.org/pdf/2502.14165 .

Theorem 3.2.2 gives the quantum LP bound. Example 3.2.2 supplies the SU(2) coefficients for Hilbert-space dimension n+1. Section 3.4, Table 3.1 (printed p. 89; PDF page index 92) tabulates distance-five code-dimension bounds: 1 at n=17, approximately 2.019 at n=18, and 2.096 at n=19. The shorter displayed lengths are also excluded. Thus, after identifying intrinsic and physical distance, the table already supplies the n>=18 lower bound, but not n>=19.

The text preceding the table describes numerical Gurobi bounds, agreement with exact GLPK arithmetic for smaller cases, and possible precision failures at larger parameters. It does not publish a separate exact certificate for every displayed entry. The local rational certificates remove this reproducibility/precision caveat. The text following Table 3.1 says self-dual inequalities were included and did not improve the integer dimension bounds. This agrees with the surviving n=18 LP feasibility in the candidate.

### Bumgardner: SU(2) MacWilliams/LP framework predates recent intrinsic notation

Christopher Bumgardner, dissertation dated March 2011, preprint 21 May 2012, https://arxiv.org/html/1205.4517 .

Theorem 4.4.1 and Section 4.5 derive SU(2) weight-enumerator relations using Wigner 6j symbols and explain the resulting LP code-dimension bounds. This is prior art for the basic method, not a located exact n=18 no-go.

### Kubischta–Teixeira and Teixeira: distance correspondence and reformulation

- Kubischta–Teixeira, arXiv:2604.16023v2, revised 26 August 2026, https://arxiv.org/html/2604.16023v2 .
- Teixeira, arXiv:2605.15372v1, 14 May 2026, https://arxiv.org/html/2605.15372v1 .

Kubischta–Teixeira Appendix B, Lemma B1 / Proposition B2 identify intrinsic depth on Sym^n(C^q) with physical qudit distance. Appendix A gives scalar LP conditions and the SU(2) 6j transform. Appendix B-D, Propositions B5–B6 and the concluding statement establish the seven-qubit distance-three extremum. They do not establish the nineteen-qubit distance-five minimum. Sections I-C and III explicitly attribute the multiplicity-free scalar theory to Bumgardner and Okada.

Teixeira derives an explicit Racah-polynomial expression for the symmetric-power transform and its orthogonality/involution properties. No distance-five minimum theorem was found there.

### Bond et al.: the exact target remains a conjecture in current primary literature

Bond, Minář, Ozols, Safavi-Naini, Visnevskyi, arXiv:2603.10981v1, 11 March 2026; current record still v1: https://arxiv.org/html/2603.10981v1 .

Section 3.1 searches unrestricted complex coefficients and finds first solutions at 7, 19, 37 for t=1,2,3. It uses up to 1,000 random starts and finite cost/gradient tolerances. Failure to find a solution is not nonexistence. Conjecture 3.1 states n_min(t)=3t^2+3t+1, with t=2 exactly the present minimum-19 question. Section 6 again calls the bound conjectural. Some earlier prose calls the numerical results minimal; that does not upgrade the search to a proof. The paper explicitly describes the AAB shorter-length result as a search in the PR family.

Theorem 2.3 gives the equivalent deletion formulation: for fully symmetric codes, correcting two arbitrary qubit errors is equivalent to correcting four deletions, as well as four erasures. It is not merely a two-deletion problem.

### Generic higher-order SDP and certificate technology are prior art

- Anglès Munné–Nemec–Huber, *SDP bounds on quantum codes*, first posted 19 August 2024, current v2 10 September 2025: https://arxiv.org/abs/2408.10323 . Complete state-polynomial SDP hierarchy for unrestricted qubit codes and symmetry-reduced bounds. Its displayed nonexistence results concern different parameters, not the symmetric n=18 target.
- Anglès Munné–Huber, *SDP bounds on quantum codes: rational certificates*, 20 March 2026: https://arxiv.org/abs/2603.19901 . Rationally certified SDP infeasibility is already a developed technique.
- Xiao, *A Three-Point Continuous-Variable Quantum MacWilliams Identity*, 16 July 2026: https://arxiv.org/abs/2607.14920 . Three-point quantum enumerators/SDP bounds are prior art in a different, bosonic setting; its collapse theorems do not establish the finite-spin target.

These references constrain method-novelty language. The concrete spin-three-copy PPT constraints, certified evaluation, and resulting n=18 exclusion should be compared explicitly; one should not claim to invent SDP quantum-code bounds or rigorous SDP certification.

## Model boundaries and equivalent formulations

The intended object is a two-dimensional complex code C contained in Sym^n(C^2), with exact Knill–Laflamme conditions for every error of weight at most two. Equivalently it detects all physical operators of weight at most four, has distance at least five, or is a rank-two intrinsic spin-n/2 code of depth at least five. Here spin errors use the degree/rank filtration, not arbitrary errors on the entire single-spin Hilbert space.

“Every codeword is permutation-fixed” and “the code projector commutes with every permutation” are different definitions in general. However, for this particular rank-two qubit problem they coincide at n>=5. This is an elementary independent deduction:

Schur–Weyl duality decomposes (C^2)^tensor n into SU(2) factors tensored with two-row Specht modules [n-k,k]. A commuting projector has blocks P_k tensor I_[n-k,k]. For k>=1, the Specht dimension is binom(n,k)-binom(n,k-1), which exceeds 2 for n>=5. A rank-two projector therefore has no support in any nonsymmetric block. Only [n] remains, exactly Sym^n(C^2). This argument assumes exact invariance under all ordinary qubit permutations. It does not address weaker permutation covariance, permutation-assisted recovery, arbitrary code dimension, or larger local dimension.

Quantum Singleton excludes the small n where those definitions can differ. A useful explicit counterexample to global equivalence is the n=4 spin-zero subspace: its rank-two projector is permutation-invariant, but its vectors are not all permutation-fixed.

## Priority conclusion and remaining caution

A valid unrestricted n=18 exclusion would settle the t=2 case of Bond et al. Conjecture 3.1, matching AAB's previously known 19-qubit code. It would not construct a new code, settle the conjecture for all t, improve the unrestricted binary quantum-code optimum, establish an efficient decoder, or prove experimental performance.

Searches included the current versions above, related spin-code literature, and targeted queries for nineteen/eighteen-qubit PI no-go results and August–November 2026 updates. No superseding exact exclusion was located. The independent certificate and the analytic necessity of every relaxation constraint still need their own mathematical audit; literature search cannot validate those steps.
