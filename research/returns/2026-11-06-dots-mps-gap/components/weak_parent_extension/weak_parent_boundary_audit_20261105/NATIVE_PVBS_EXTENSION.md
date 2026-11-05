# Native multispecies PVBS: finite-block coercive coboundary

Date: 2026-11-05. Independent algebraic proof and finite numerical audit. This extends the fixed-block coboundary repair criterion in `COBOUNDARY_REPAIR.md` to the native, interacting PVBS model. It is not a novelty or external-verification claim.

## 1. Exact source conventions

Use Bachmann and Nachtergaele, *Product Vacua with Boundary States and the Classification of Gapped Phases*, arXiv:1212.3718v3, Sec. 2, Eqs. (2.1)-(2.2), and the exclusion convention in Eq. (2.11): https://arxiv.org/pdf/1212.3718 . The source was checked directly.

There are s occupied labels i=1,...,s and vacuum 0. Set lambda_0=1; all lambda_i>0 and theta_ij=-theta_ji are real phases. For 0<=i<j<=s define

    phi_ij=|ij>-exp(i theta_ij)(lambda_j/lambda_i)|ji>.

The local interaction is the orthogonal projector onto these vectors together with |ii>, i=1,...,s. Thus explicitly

    h=sum_(0<=i<j<=s) |phi_ij><phi_ij|/||phi_ij||^2
        +sum_(i=1)^s |ii><ii|.

The summands have mutually orthogonal supports. There is no |00><00| summand. In the ordered basis (|ij>,|ji>), with x=lambda_i^2,y=lambda_j^2, its occupied two-label block is exactly

    [ x/(x+y),  -sqrt(xy)exp(-i theta_ij)/(x+y) ]
    [ -sqrt(xy)exp(i theta_ij)/(x+y),  y/(x+y) ].

This fixes the phase and ratio conventions used below. Assume lambda_i!=1 for every occupied label; no distinctness between occupied labels is required.

## 2. A positive shifted interaction

Define the diagonal onsite operator Y by

    Y_0=0,
    Y_i=lambda_i^2/(1+lambda_i^2)-1/2  (i>=1),
    h'=h-Y tensor I+I tensor Y.

The shifts telescope on open blocks and cancel on periodic chains.

### Vacuum-particle blocks

For (|0i>,|i0>) the shifted block is

    [ 1/2,  -t_i exp(-i theta_0i) ]
    [ -t_i exp(i theta_0i),  1/2 ],
    t_i=lambda_i/(1+lambda_i^2).

Its eigenvalues are 1/2 +/- t_i. Both are positive because lambda_i!=1.

### Occupied different-label blocks

For i,j>=1, put x=lambda_i^2,y=lambda_j^2 and

    delta=Y_j-Y_i=(y-x)/((1+x)(1+y)).

The shifted block adds delta,-delta to the two diagonal entries of the displayed source block, leaving the phases unchanged. Its trace is one and determinant is

    D_ij=delta[(y-x)/(x+y)-delta]
       =(y-x)^2(1+xy)/[(1+x)^2(1+y)^2(x+y)].

Therefore it is positive definite when lambda_i!=lambda_j. For equal anisotropies delta=0 and the original positive rank-one projector remains. The |ii> sector still has energy one; |00> still has energy zero. Consequently h'>=0.

The exact local kernel is

    ker h'=span{|00>}
      direct-sum span{ |ij>+exp(i theta_ij)|ji> :
                       1<=i<j<=s, lambda_i=lambda_j }.

The plus sign and phase follow by taking the inner product with phi_ij: the coefficient relation is a_ji=exp(i theta_ij)a_ij for equal lambdas. No claim about simultaneous gauge removal of phases is needed.

## 3. A fixed open block has only the vacuum kernel

Partition occupied labels into groups with equal lambda. Let r be the maximum group size and set k=r+1. Then

    ker H'_k=span{|0^k>},
    H'_k=sum_(a=1)^(k-1) h'_(a,a+1).

Proof: h'>=0, so every ground vector is in each local kernel. Expand it in computational basis words.

- A word containing both 0 and an occupied label has a vacuum/particle interface somewhere. That local two-site sector is positive definite, so the word's coefficient vanishes.
- A fully occupied word using multiple equal-lambda groups has an adjacent change of group. That two-label block is positive definite, so its coefficient vanishes.
- Thus every potentially nonzero nonvacuum word lies entirely in one group of at most r species. Since k=r+1, a species repeats.
- For two adjacent distinct species in the same group, the ground-space relation exchanges them with a nonzero unit-modulus coefficient. Choose two occurrences of a repeated species with no equal species between them and swap one through the intervening distinct labels until the two coincide adjacently. The resulting coefficient is a nonzero scalar multiple of the initial coefficient. The adjacent |ii> projector forces the resulting coefficient to zero, hence the initial one was zero as well.

This does not assume any global consistency of exchange phases: only invertibility of each local coefficient relation is used. Additional loop constraints could only kill more coefficients. The vacuum survives, proving the exact kernel.

Since the block is finite-dimensional and positive, its smallest positive eigenvalue c is strictly positive and

    H'_k >= c(I-|0^k><0^k|).

When all occupied anisotropies are distinct, r=1 and k=2. A safe nonoptimized choice valid in every case is k=s+1.

## 4. Consequence for the unrestricted NN LTI hierarchy

Because

    H'_k=H_k^open(h)-Y_1+Y_k,

this is precisely the fixed-block coboundary hypothesis with onsite X=-Y. A full LTI feasible positive rho has Tr rho h_i=1 and equal onsite expectations at all positions, hence

    Tr rho H'_[a,a+k-1]=k-1.

For any site j in that block, its occupation projector n_j is bounded above by I-|0^k><0^k|. Therefore

    Tr rho n_j <= (k-1)/c.

Reset just sites 1 and n to vacuum. Let H_b denote the two core seams plus the periodic seam; the latter annihilates every output. For the squared boundary energy,

    Phi*(H_b^2) <= 2M^2(n_2+n_(n-1)),
    Tr rho Phi*(H_b^2) <= K:=4M^2(k-1)/c,

where M=||h||=1 for this normalized native model. The first operator bound follows from (A+B)^2<=2(A^2+B^2) and from the fact that either compressed seam-square is positive, has norm at most M^2, and annihilates the remaining site's vacuum. It does not depend on Tr rho.

The unchanged core has m_c=n-3 bonds. Its first moment is m_c and its second moment is at most m_c v+2M. The standard periodic spectral inequality and weighted Hilbert-Schmidt triangle give, for n>=max(k,4),

    Delta_n m_c <= [sqrt(m_c gamma_n+2M)+sqrt(K)]^2.

The usual valid-level upper bound and gamma_n<=2M then give

    gamma_n >= Delta_n - O(n^-1/2).

Together with monotonicity and the certified upper comparisons to longer periodic chains, this proves convergence of the unrestricted hierarchy to the periodic thermodynamic gap within the already specified hierarchy definitions. It does not assert any corresponding result for a restricted-Y ansatz.

No exact formula for the native multispecies full gap is needed. The familiar 1-2lambda_i/(1+lambda_i^2) source statement is sharp for a one-particle restriction and must not be silently substituted for the full many-body gap. Periodic ground uniqueness and a positive periodic lower gap also follow from the shifted fixed-block coercivity, independently of that formula.

## 5. Independent numerical checks

`check_native_pvbs_coboundary.py` builds the source interaction with seed 246031 and independent random phases for every unordered label pair. It tests local shifted positivity and dense fixed-block spectra. The output is `native_pvbs_coboundary_results.json`.

Verified cases (lambda list; predicted k; observed positive block gap c):

- [0.5,2.0]; k=2; c=0.1.
- [0.5,0.5]; k=3; c approximately 0.1315341562.
- [0.5,0.5,2.0]; k=3; c approximately 0.1315341562.
- [0.5,0.5,0.5]; k=4; c approximately 0.1468871126.
- [0.25,0.5,2.0]; k=2; c approximately 0.06962235944.

Every tested block has exactly one eigenvalue within 1e-9 of zero. Small negative local eigenvalues are at rounding scale (less than 3e-16). These checks support, but do not replace, the exact block and kernel argument.
