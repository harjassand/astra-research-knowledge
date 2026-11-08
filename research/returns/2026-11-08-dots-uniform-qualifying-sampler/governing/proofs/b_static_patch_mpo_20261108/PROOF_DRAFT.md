# Static noisy patch evaluation by exact rational coefficient MPOs

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. Candidate proof, NOT independently cleared. The two central review targets are the growing-layer coefficient-rank import in Section 3 and the exact-rational gauge algorithm in Section 4. All proposed sampler consequences remain conditional on those targets. This is not an early-time full-output algorithm.

## 0. Target and input

A connected N-site subset of the square lattice has nearest-neighbor two-qubit Hamiltonian terms and onsite replacement noise. All entries, time t>=0 and desired scalar error eta in (0,1] are rational. The generator is written as a sum of complete local Lindblad generators; a Hamiltonian commutator on an edge counts as one such term. The sum of local diamond-norm bounds incident to a physical qubit is at most a fixed g. Numerical time and input bit lengths are explicitly charged. Product input rho and positive product effect A satisfy Tr rho=1 and Tr A=2^N. Therefore ||A||_infinity<=2^N.

We propose to evaluate G=Tr[A exp(tL)(rho)] to error eta. The intermediate MPO need not be CP or TP; it is a numerical approximation and is not passed off as a physical oracle. Set channel error epsilon=eta*2^(-N), and E=max(1,log(1/epsilon)).

For t<=polylog(N+2) and E=O(N polylog(N+2)), the proposed work is

    poly(input bits, t) * exp[O_g(N^(7/8) polylog(N+2))].

The explicit more informative exponent below is

    O(w b + (M/b) log(qM+w+2) + q log(M+1)
      + log(b+1) log(M+2)),

where w=O(N^(3/4)), b=Theta(N^(1/8)), q=O(N/b), and M=O(g t w b + E + log q). The constants in the exponent are independent of N, t, eta and the input denominator. This is subexponential in patch size, not polynomial in N.

## 1. Paid thin layers for any connected square-lattice patch

Shift coordinates so that their magnitudes are O(N), which is possible because the patch is connected. For alpha in [0,1], place site (x,y) in layer floor(x+alpha*y). Every nearest-neighbor edge stays within a layer or crosses just one adjacent-layer interface. A connected patch has no empty layer between its extrema, and at most 2N layers.

Take alpha uniformly from {a/Q:0<=a<Q}, Q=N^2. For two distinct sites let r=max(|dx|,|dy|). If dy=0, their floors never coincide. Otherwise, a collision requires |dx+alpha*dy|<1. If this interval intersects [0,1], then |dx|<=|dy|+1, hence r<=2|dy|. The grid probability is at most min(1,4/r)+2/Q.

For a fixed site the number of lattice sites in an infinity-norm radius R square is at most (2R+1)^2. For R=floor(sqrt(N)), the shells1 throughR contain at most8r sites each and contribute at most32R; the remaining at mostN sites contribute at most4N/(R+1). Thus sum_q min(1,4/r_q)<=36 sqrt(N). If n_l is the occupancy of layer l, then

    E_alpha sum_l n_l^2 <= N+36 N^(3/2)+2N^2/Q <=64 N^(3/2)

for N>=2. Thus at least one of these Q rational slopes satisfies this bound, and its largest layer obeys w<=8 N^(3/4). Exhaustively evaluate all Q slopes using integer floors (Qx+ay)//Q and choose the best. This costs O(N^3 log N) elementary operations and O(log N) coordinate bits. Faster randomized selection is unnecessary for the theorem.

N=1 is evaluated directly. No rectangular padding by empty physical sites is used. Disconnected patches can be handled componentwise; a connected activity patch is the main application.

## 2. Rectangular Taylor truncation with CPTP backgrounds

Partition consecutive layers into q blocks of b layers. Anchor each microscopic Lindblad term to the block containing its leftmost layer. Let G_j be its anchored sum. It is a complete Lindblad generator supported on at most b+1 layers, and

    ||G_j||_diamond <= Lambda := g w b

after a harmless constant adjustment of g. Executably, use a supplied rational upper bound on each constant-dimensional local diamond norm, or a rational entrywise upper bound computed from its local matrix. The local dimension is fixed before layering, so this changes g only by a fixed factor; no exact diamond-norm optimization is assumed. Let F(lambda)=exp[t sum_j lambda_j G_j]. For lambda in [0,1]^q every background generator is Lindblad, so all time-ordered propagators appearing in a Duhamel derivative are CPTP contractions in diamond norm.

Let T_j mean Taylor truncation in lambda_j to degree M-1 at zero, evaluated at one, and let R_j=I-T_j. The integral remainder and mixed Duhamel formula give, for each nonempty S,

    || product_(j in S) R_j F ||_diamond
       <= product_(j in S) (t ||G_j||_diamond)^M / M!.

There is no missing factorial: summing all orders of the M|S| insertions cancels the simplex factorial, and the Mth Taylor remainder integrals contribute one 1/M! per coordinate. All unselected coordinates are one; all selected integration coordinates are between zero and one, preserving complete positivity of each background.

The commuting coordinate functionals satisfy

    I-product_j T_j = sum_(nonempty S) (-1)^(|S|+1) product_(j in S) R_j.

Writing a=(t Lambda)^M/M!, the rectangular polynomial F_<M therefore satisfies

    ||exp(tL)-F_<M||_diamond <= (1+a)^q-1.

A rational executable choice is

    M >= max(1, ceil(6 t Lambda), ceil(log_2(2q/epsilon))).

Since M!>=(M/e)^M and e<3, a<=2^-M; then q a<=epsilon/2 and the error is at most epsilon. A ceiling of log_2 can be found with integer comparisons on rational epsilon.

Define integer-degree coefficient superoperators

    P_m = [lambda^m] (sum_j lambda_j G_j)^r, r=sum_j m_j.

They obey P_0=Id and P_m=sum_(j:m_j>0) G_j P_(m-e_j). The retained polynomial is

    F_<M = sum_(0<=m_j<M) t^r/r! P_m.

There are exactly M^q coefficients and maximum degree r<=q(M-1). No claim that one coefficient per total degree suffices is made.

## 3. Growing-layer exact rank bound: explicit source dependency

The source is Mackay et al., arXiv:2609.27497v1, Supplementary Corollary 6 and Proposition 49, especially equations (864)–(873). The cut-count phase decomposition is algebraic; Hermiticity/unitarity is not used in the rank calculation. Apply it to the Liouville matrices of our superoperators and physical layers, retaining all dependence on layer size.

Fix a target layer cut and a window of b consecutive layer cuts, padding only with empty layers at an endpoint. At most three anchored blocks contain terms that cross a cut in this window. A microscopic term crosses at most one layer cut. Each retained m_j<M therefore gives total local cut occupancy Q<=3M. The source's phase decomposition is an exact sum over at most

    b(6M+1)^ceil(log_2 b)

cut/phase choices and crossing orders s<=s_max=floor(6M/b). No cut-tail remainder survives coefficient projection, because every word has that occupancy bound.

At the selected cut, the noncrossing generator is A_L tensor Id + Id tensor A_R. The crossing generator has Liouville Schmidt rank R_cross<=C w: each physical edge contributes a constant number of product superoperators and at most four edges per site cross a layer boundary. C can be chosen as128 for two-qubit Hamiltonian commutators, or enlarged harmlessly for a more general fixed local Lindblad representation.

The r-th power with s marked crossings splits into at most

    binom(r+s+1,2s+1) R_cross^s

left/right word sectors. At most two coarse variables have terms on both sides of a selected cut. Their coefficient extraction costs at most (M+1)^2 total left-degree allocations, not a fresh allocation for every word segment. Finally, moving the selected cut to the target cut through b layers moves at most wb qubits and costs at most16^(wb) in Liouville Schmidt rank.

Thus every P_m has an exact MPO with bond dimension at most

    D_* = 16^(wb) b(s_max+1)(6M+1)^ceil(log_2 b)(M+1)^2
          * max_(0<=s<=min(r,s_max)) binom(r+s+1,2s+1)(Cw)^s.

This yields

    log D_* = O(wb + (M/b)log(qM+w+2)
                + log(b+1)log(M+2) + log(qM+2)).

The local dimension at one physical layer is 2^w, and its superoperator tensor dimension is16^w. These dimensions are explicitly paid. Each G_j may be stored densely on its b+1 layers, at cost exp(O(wb)); this is sufficient, though not optimal. Partial updates in the coefficient recursion have MPO bond at most q D_* exp(O(wb)). Exact rank reduction after each completed update restores D_*.

The update count is q M^q. Therefore arithmetic work and storage are polynomial in q M^q, the local tensor dimensions and the displayed bond dimensions, with the logarithmic exponent stated in Section0. This is not an import of the source's fixed-local-dimension headline bound: every dimension-growing term has been retained explicitly here.

REVIEW TARGET: verify that the source's coefficientwise cut-count decomposition and shared-variable count apply to this anchored physical-layer Liouville representation exactly as stated. No source result about numerical stability is imported.

## 4. Exact rational bit accounting, separate from numerical SVD stability

Use the unscaled physical Pauli basis. A rational Hermitian two-qubit Hamiltonian has rational real Pauli coefficients; its commutator superoperator and the onsite replacement superoperators are rational real matrices in this basis. Choose a common positive integer denominator D for all local entries; its bit length is at most the sum of the input denominator bit lengths. Work with C_j=D G_j.

Then the coefficient matrices Q_m=[lambda^m](sum lambda_j C_j)^r are integer matrices, and P_m=D^(-r) Q_m. If local integer entries have B bits, a crude maximum-entry bound for every completed or partially accumulated coefficient update is

    bitlength(entry Q_m) = O(r[B+log(qN+2)]+1) =: H.

This follows either from expanding the words or from the row-sum norm of each local integer generator. Although the full matrix is exponentially large, the bound H is polynomial in the numerical degree and paid input bits.

An exact-rank MPO can be kept in an interpolation gauge with nested physical prefix sets. At each cut choose independent physical prefix rows I_k and suffix columns J_k of the tensor unfolding; the final J_k need not be nested. The interpolation coefficients are ratios of minors formed from actual integer tensor entries, with the denominator a pivot minor Q_m[I_k,J_k] and the numerator the corresponding replaced-row minor; numerator rows may be outside the selected pivot rows. For ranks at most D_*, Cramer's rule and the determinant bound give numerator/denominator bit length O(D_*[H+log(D_*+1)]). The last core consists of selected entries. Orthonormal vectors and numerical singular-value cutoffs are unnecessary.

Given an explicit MPO of raw bond R, suitable prefix/suffix bases can be found with two exact elimination sweeps. At each stage only R times the local physical tensor dimension candidate rows/columns are inspected; suffix and prefix contraction bases reduce them to finite matrices of polynomial size in R and the local dimension. All zero tests are exact rational tests. Normalize the selected pivot submatrix to the identity, so the resulting representation is the interpolation gauge just described. This is the standard exact tensor-train rank-factorization construction, with selected physical indices retained. Numerator determinant bounds apply also to the augmented/replaced physical rows used in interpolation.

For a recursive update, raw inputs come from at most q preceding canonical coefficient MPOs and a local C_j. Their core bits are polynomial in D_*, H, N and input bits. Fraction-free Gaussian elimination on the finite sweep matrices has polynomial bit cost in these parameters. The completed gauge is reset to the minor bound for the NEW true coefficient tensor, rather than multiplying a generic denominator bound through all M^q updates. The same integer-entry bound applies to partial word sums, so partial updates may also be regauged if necessary.

This would establish bit work polynomial in the arithmetic representation parameters and H. It does NOT assert a condition-number bound for floating-point SVD or practical numerical stability. Tiny nonzero minors can require many bits; those bits are explicitly bounded by the rank-dependent determinant estimate and charged.

REVIEW TARGET: the two-sweep nested interpolation implementation and its gauge-reset bit bound must be independently checked. Merely saying that the original entries are rational would not be enough.

Time weights (t/D)^r/r! and final product-boundary contractions are rational. With r_max=q(M-1), one common denominator is (D denominator(t))^r_max * r_max!, multiplied by the product of boundary denominators. This has polynomially many bits in r_max and the paid input lengths. Evaluate each completed coefficient against the product boundaries and sum using this common denominator; there is no need to assume stability of a final signed MPO as a physical channel.

## 5. Subexponential patch cost and warm-time consequence

Choose b as a power of two within a constant factor of max(1,N^(1/8)); the geometry gives w<=8N^(3/4), q<=2N/b+1. Then

    M=O_g(t N^(7/8)+E+log N),
    log work=O_g(N^(7/8)log(N+E+t+2)
                    + t N^(3/4)log(N+E+t+2)
                    + E N^(-1/8)log(N+E+t+2)),

up to lower-order logarithmic terms and a polynomial paid input-bit factor. For polylogarithmic t and E=O(N polylog N), this is N^(7/8) times a fixed polylogarithmic factor.

Conditional on Sections3–4, this is relevant to the previous one-level warmstart as follows. Write L=1+log(n/epsilon). Before the global mixing cutoff, tau=O(L). The existing dimensionless warmtime action is sigma=s_base+2ceil log_2(tau+2)=O_rho(log(L+2)), with both large constants and the old qualifying-time condition retained. Apply the patch theorem to the normalized generator L/gamma at numerical time t=sigma, whose local strength is O_rho(1). Rational division by gamma adds paid input bits, not an uncharged inverse-gamma action. Evaluate this warm-time scalar by the already-audited connected-activity expansion at sigma, not by recursively constructing a still-earlier Pauli list. Its activity patches contain at most O_rho(sigma^2+sigma L') qubits, where the required one-level log precision L'=O_rho(L). Hence N<=O_rho(L log(L+2)), and their channel log precision is E=O(N+L') after paying the effect norm2^N.

If N<=C_rho L', dense evaluation already costs exp(O_rho L'). Otherwise N>L', so E=O_rho N and the preceding patch bound is exp[O_rho((L log L)^(7/8) polylog L)] = exp(O_rho L). Activity enumeration, classical Ursell arithmetic and the earlier one-level discovery/propagation calls are also exp(O_rho L), with paid finite bits and confidence. The fixed factor L'<=A_rho L is incurred only once, so it does not accumulate through log* time descent.

If all these steps clear review, this would improve the prior qualifying-time exp[L exp(O_rho(log* tau))] construction to a uniform polynomial in n/epsilon and the paid input/action factors. It would still NOT cover the unqualified early/intermediate constant-time interval below the old accumulated-noise threshold. It would not be a practical runtime claim. No such improvement is asserted as established until the growing-layer rank and finite-bit construction are audited.

## 6. Prior boundary

The coordinatewise polynomial compression and exact-arithmetic coefficient MPO algorithm are prior in arXiv:2609.27497v1, Supplementary XI–XII. The proof here proposes a deliberately loose geometrical slicing bound, an explicit growing-layer accounting, a rational exact-gauge bit closure, and a specific application to the earlier noisy warmstart. No priority or novelty claim is made. The source itself explicitly does not supply a uniform finite-precision stability theorem; the separate rational argument above is a proposed way to pay bits for this narrower input model, not a quotation from it.

### Section4 implementation detail: finding the interpolation gauges from an MPO

This expands the constructive claim in Section4 rather than invoking a numerical rank routine.

If T is identically zero, represent it by a zero scalar core and identity/rank-one remaining cores; no inverse or empty pivot is taken. Otherwise let the supplied raw MPO for a coefficient tensor T have cores A_k of bond at most R and local tensor dimension d_k<=16^w. In a right-to-left pass, write B_k for the raw suffix contraction, an R_k by (all suffix indices) matrix. Choose a spanning column set J_k^raw as follows: extend every already chosen suffix in J_(k+1)^raw by one local index, form the resulting at most d_(k+1) R columns using A_(k+1) and the stored B_(k+1) values, and choose independent columns by exact elimination. This spans all columns of B_k by induction. Store their actual physical suffix strings and their finite R_k-vector values. For arbitrary rational raw cores, take a common denominator equal to the product of ALL raw-core entry denominators. If S<=h d_max R^2 is the number of stored entries, that denominator has at most S B_raw bits. Each contracted monomial uses each participating core once, so a safe numerator/denominator bound is O(S B_raw+h B_raw+h log(R+1)); this is polynomial in the materialized raw representation. An entrywise B_raw bound alone would not justify O(h[B_raw+log R]) bits for a sum of unrelated rational denominators.

Now proceed left to right. Suppose I_(k-1) is a row basis of the full tensor unfolding at cut k-1, stored as actual physical prefix strings and raw prefix contractions. Every row at cut k is a linear combination of rows in I_(k-1) times one local index. Evaluate those candidate rows on J_k^raw. Because J_k^raw spans the raw suffix columns, this finite matrix detects their true rank. Select independent rows to define nested I_k, and select the corresponding number of independent columns from J_k^raw to define J_k. The intersection T[I_k,J_k] is nonsingular. No full physical unfolding is materialized.

Use cores

    C_k(I_(k-1),i_k,I_k) = T[I_(k-1),i_k,J_k] * T[I_k,J_k]^(-1)

for k<h, with C_h=T[I_(h-1),i_h]. The exact rank identity

    T(prefix,suffix)=T(prefix,J_k) T(I_k,J_k)^(-1) T(I_k,suffix)

and the nesting of I_k prove that their tensor contraction is exactly T. The suffix sets J_k need not themselves be nested after the second pass. Every displayed T entry is an entry of the true coefficient tensor, with the integer bound H; hence the minor-based output bit bound follows. All finite matrices have sizes polynomial in R, d_k and h. Pivot search and inversion are exact rational operations; fraction-free elimination gives polynomial bit work in these sizes and input bit lengths.

This explicit two-pass interpolation construction is the proposed bridge from an arithmetic operation count to a Turing bit bound. Its proof uses bounded integer entries of each exact coefficient and an exact-rank representation. It would not justify rounding away small singular values of an arbitrary floating-point tensor network.
