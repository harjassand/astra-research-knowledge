# A closing-open-gap weak parent and a direct LTI repair

Date: 2026-11-05. Internal proof note and adversarial stress test. No general weak-parent completeness or novelty claim is made. The existing proper-parent proof files are not changed.

## Main conclusion

A unique product bulk ground and a fixed positive periodic gap do **not** imply a uniform open-chain gap, even for a positive, frustration-free, nearest-neighbor interaction in one dimension. An explicit three-state example below has periodic gap exactly 1/5 and exponentially closing open gap.

It is nevertheless **not** a counterexample to the unrestricted LTI hierarchy: a direct endpoint reset proves convergence for a class containing this example, without assuming any open gap. The key is a positive coercive onsite coboundary, whose expectation is unchanged by the full LTI constraint.

## 1. The coercive-coboundary class

Let h>=0 be a nonzero, translation-invariant two-site interaction on a finite-dimensional site with distinguished vacuum |0>. Suppose

    h|00>=0,
    h' = h + X tensor I - I tensor X,
    h' >= c (I-|00><00|),   c>0,

for a Hermitian onsite X. These assumptions already imply X|0> is proportional to |0>: h' is positive, its vacuum expectation is zero, and therefore h'|00>=0. Thus h' has exactly the strict vacuum kernel. Let M=||h||.

The periodic Hamiltonians of h and h' agree exactly by telescoping. They are positive, frustration free, and have a unique vacuum ground for all nontrivial sufficiently large periods. The original open Hamiltonians need not have a uniform gap, as the example below demonstrates.

For the unrestricted nearest-neighbor LTI hierarchy built from the **original h**, with n>=3,

    gamma_n -> lim_N Delta_N,
    gamma_n >= Delta_n - O(n^(-1/2)).

Here Delta_N is the periodic finite-size gap. The proof also implies existence of this periodic limit. The result is not an equality between the finite-level hierarchies of h and h'.

## 2. Proof on the original full-LTI dual

Take any dual-feasible rho>=0 on n sites:

    Tr_1 rho = Tr_n rho,    Tr rho h_1=1.

It need not be normalized and its trace need not be bounded. Write

    v=Tr rho [h_1^2+sum_(j=2)^(n-1){h_1,h_j}].

As in the original hierarchy, local translation invariance implies every Tr rho h_i=1. It also implies equality of neighboring one-site marginals, hence

    Tr rho h_i' = Tr rho h_i + Tr rho (X_i-X_(i+1)) = 1.       (A)

Set n_i=I-|0><0| on site i. Since I-|00><00|>=n_2 on the first pair and similarly at the right end,

    Tr rho n_2 <= 1/c,
    Tr rho n_(n-1) <= 1/c.                                  (B)

These are occupation bounds on the original LTI witness, not a ground-space compression. They remain true when rho contains arbitrarily much vacuum mass.

For n>=4, let Phi reset only sites 1 and n to |0>, tracing out those sites and leaving the entire interior marginal unchanged. Let H_c consist of the original h bonds completely inside sites 2,...,n-1; it has m_c=n-3 terms. Define H_b=H_per-H_c. The periodic endpoint bond annihilates the reset output. When H_b acts on that output, only h_(1,2) and h_(n-1,n) remain.

Let F=Phi^*(H_b^2). For Hermitian A,B, (A+B)^2<=2A^2+2B^2. Vacuum compression of h^2 on either endpoint has norm at most M^2 and annihilates the remaining site's vacuum. Thus the following is an operator inequality on the input, valid including arbitrary core references:

    0<=F<=2M^2(n_2+n_(n-1)).

Consequently, by (B),

    K:=Tr Phi(rho) H_b^2 <= K0:=4M^2/c.                     (C)

One can also use a looser positive-block bound on the two extended endpoint vacuum projectors; the direct square bound above gives the displayed constant.

The original h moments obey a=Tr rho h_i^2<=M, b_1>=-2M, b_r>=0 for r>=2. For any contiguous core of m_c bonds, the exact expansion gives

    Tr rho H_c=m_c,
    Tr rho H_c^2<=m_c v+2M.                                (D)

Phi preserves both moments. Put nu=Phi(rho); do not divide by its trace. Positivity of H_b gives Tr nu H_per>=m_c. The weighted Hilbert-Schmidt triangle inequality and H_per^2>=Delta_n H_per yield

    Delta_n <= [sqrt(m_c v+2M)+sqrt(K0)]^2/m_c.             (E)

Standard Slater duality identifies the full-LTI dual infimum with gamma_n for n>=3: the normalized identity is strictly dual feasible, and delta=-M is primal feasible using the usual three-site coboundary. No dual attainment is assumed. The unique periodic vacuum and a one-site orthogonal excitation give gamma_n<=2M, so a nearly optimal sequence may be bounded uniformly in v. Taking v down to gamma_n in (E) yields the explicit conservative comparison

    gamma_n >= Delta_n - [2M+K0
                   +2 sqrt((2M m_c+2M)K0)]/m_c,   n>=4.   (F)

It is O(n^(-1/2)). Finally gamma_n<=Delta_N for every N>=2n, the published certified lower-bound property of the unrestricted hierarchy. Hence

    Delta_n <= inf_(N>=2n)Delta_N+o(1),

which forces the periodic limsup and liminf to agree and squeezes gamma_n to that limit.

The proof never assumes an original open gap, never divides by an uncontrolled trace, and never treats the coboundary shift as a change of the finite-level objective. It uses h' only through (A)-(B).

### 2.1 Fixed-block version

The same conclusion holds under the more general condition: there are a fixed k>=2, onsite Hermitian X, and c>0 such that

    B_k=sum_(i=1)^(k-1) h_i+X_1-X_k
           >=c(I-|0^k><0^k|).

The individual shifted two-site term need not be positive. For n>=max(4,2k), full LTI gives Tr rho B_k=k-1 on both end blocks. Since each block vacuum-complement dominates any contained site's occupation,

    Tr rho n_2, Tr rho n_(n-1) <= (k-1)/c.

Thus the exact same reset works with K0=4M^2(k-1)/c in (C)-(F). Summing cyclic translates of B_k also shows that the periodic Hamiltonian is coercive: (k-1)H_per>=c sum Q_block>=c N_particle, for periods at least k. In particular the periodic vacuum is unique and the uniform periodic gap needed for the interpretation is itself certified. There is no need to assume a uniform gap for the original open chain.

This fixed-block formulation covers all native finite-species noncritical PVBS interactions, not just tensor-product layers. The full algebra is independently checked in `LITERATURE_AND_SECOND_REVIEW.md`; its short derivation follows.

### 2.2 All native finite-species noncritical PVBS models

Use species i=1,...,s with lambda_i>0, lambda_i!=1, vacuum label 0 with lambda_0=1, and the usual native PVBS pair projectors onto

    |ij>-exp(i theta_ij)(lambda_j/lambda_i)|ji>,  i<j,

plus |ii> for occupied i. The pair vectors are normalized in the interaction. Set Y_0=0, Y_i=lambda_i^2/(1+lambda_i^2)-1/2 and h'=h-Y tensor I+I tensor Y.

Every vacuum/species block of h' has eigenvalues 1/2 +/- lambda_i/(1+lambda_i^2)>0. For an occupied distinct pair, put x=lambda_i^2, y=lambda_j^2. The shifted block has trace one and determinant

    (y-x)^2(1+xy)/[(1+x)^2(1+y)^2(x+y)] >=0.

Thus h'>=0. Its only local kernel vectors besides |00> are exchange vectors within a group of exactly equal lambda values. If the largest such group has r species, the (r+1)-site open Hamiltonian of h' has unique vacuum kernel:

- no nonzero ground coefficient can have a vacuum/occupied interface;
- no occupied adjacent labels can have different lambda values;
- within an equal-lambda group, adjacent swaps of distinct labels have nonzero exchange coefficients;
- in any word longer than the group size, move a repeated species adjacent by such swaps; the |ii> penalty forces its coefficient, and hence the original coefficient, to zero.

Phases can only impose further consistency conditions; they cannot prevent the nonzero swap relation used to force a repetition to zero. Therefore for k=r+1 (or conservatively s+1), finite dimensionality supplies c>0 such that H'_k>=c(I-|0^k><0^k|). It is exactly the block condition above with X=-Y. Five independent random-phase finite checks, including three equal lambda=.5 species at k=4, are saved in `native_pvbs_coboundary_results.json`.

This gives unrestricted LTI convergence for the full native noncritical PVBS class without identifying its exact full spectral gap. The established one-particle mass formula must still not be misreported as the exact full many-species gap. The result remains an internal theorem extension, not a priority claim.

## 3. Explicit qutrit obstruction to the open-gap shortcut

Use the basis |0>,|a>,|b>. Fix q=1/2 and parameters lambda_a=q, lambda_b=1/q. Let h be the sum of two mutually orthogonal normalized hopping projectors

    |p_s><p_s|,   |p_s>=(|0s>-lambda_s|s0>)/sqrt(1+lambda_s^2),
    s=a,b,

and all four occupied-pair projectors

    |st><st|,   s,t in {a,b}.

This h is an orthogonal projector of rank six and norm M=1. Set

    X=diag(0,3/10,-3/10),
    h'=h+X tensor I-I tensor X,
    n=diag(0,1,1).

In each vacuum-particle block, the diagonal entries of h' become 1/2 and the off-diagonal entries are -2/5. Its block eigenvalues are 1/10 and 9/10. The four occupied-pair entries are 1,1,8/5,2/5. The sole zero eigenvector is |00>. Thus h'>=(1/10)(I-|00><00|).

There is also the exact stronger particle-number inequality

    h' >= (1/10)(n tensor I+I tensor n).

The eigenvalues of the difference are

    {0,0,0,1/5,4/5,4/5,4/5,4/5,7/5}.

Summing on a ring cancels the X coboundary and gives H_per>=(1/5)N_particle. A uniform one-a-particle vector (or one-b-particle vector) has energy 1/5. Therefore

    Delta_N=1/5

for every N>=3. The periodic ground is uniquely the vacuum. Since the h and h' interactions differ by a coboundary, they give the same infinite-volume local dynamics; the strict product representative also establishes the unique product bulk ground in the usual ground-state sense.

### Open kernel and exponentially small positive energy

The open zero-energy space is exactly three-dimensional: vacuum, one a-particle mode localized to the left, and one b-particle mode localized to the right. The hopping constraints propagate every fixed ordered particle word among configurations separated by vacancies. If a word has at least two particles, it can be moved to a configuration with an adjacent occupied pair, whose amplitude must be zero; connectivity then forces that entire word sector to vanish. Single-particle amplitudes are fixed geometric sequences. This proves the stated kernel without relying on a numerical threshold.

For an N-site chain, consider the normalized two-particle trial vector proportional to

    |Psi_N> = sum_(1<=x<y<=N) q^(x-1+N-y) |a_x b_y>.

It is orthogonal to the exact open kernel. All hopping projectors annihilate it. Its only energy comes from adjacent a,b pairs, so its Rayleigh quotient is exactly

    [(N-1) q^(2N-4)] / [sum_(k=0)^(N-2) (k+1) q^(2k)].

This decays exponentially. Thus the actual positive open gap tends to zero despite the constant periodic gap.

**No false hierarchy inference:** this particular simple trial has Tr |Psi_N><Psi_N| H_open^2 / Tr |Psi_N><Psi_N| H_open = 1: the vectors h_i|Psi_N> are orthogonal adjacent-pair configurations. It is not an LTI dual witness, nor does the small Rayleigh quotient itself furnish a small objective. The coercive-coboundary proof above establishes convergence for this exact model instead of disproving it.

## 4. Significance and limits

- This provides an explicit adversarial failure of the implication 'positive periodic/bulk gap plus unique product ground implies a uniform open gap.' Any broader proof using that implication is invalid.
- It also provides a valid repair for the coercive-coboundary class, including the adversarial example. The operation is just a one-site endpoint reset, and its analysis uses exact full-LTI occupation control.
- The model's gap 1/5 is already proved by the elementary onsite potential certificate. The new hierarchy argument does not improve that gap value or supply a new physical capability for this example.
- The result does not identify all weak parents admitting a coercive coboundary, and it does not settle general injective-MPS weak-parent completeness. Existence of such an X is an additional substantive condition, not a consequence assumed from uniqueness.
- No claim is made that the construction or this sufficient criterion is novel. A literature screen and independent coefficient/bound checks are documented separately. The two reviewed weak-parent extensions are kept separate from the original proper-parent package.

## 5. Evidence

The helper independently derived the qutrit construction, its potential, trial energy, and full finite spectra. Its source/results are `check_boundary_gap_counterexample.py` and `boundary_gap_counterexample_results.json`. At N=3,...,7 the positive open gaps are approximately

    0.2, 0.0550096, 0.0164688, 0.0050206654, 0.0015164292,

while the periodic gaps are 0.2. Those floating spectra are sanity checks only; the exact algebraic inequalities and trial quotient above establish the claims.

The endpoint-reset estimate has been independently checked by both the main auditor and the helper. A separate exact-rational local check and full-input reset check accompany this note. No numerical SDP optimum is needed for the proof.

References: the unrestricted hierarchy is Rai et al., https://arxiv.org/html/2411.03680v3; the established PVBS family and its boundary states are Bachmann and Nachtergaele, https://arxiv.org/abs/1212.3718. The opposite-edge forbidden-pair construction here is recorded as an internal explicit construction, not assigned a literature identity without verification.
