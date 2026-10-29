# Exact-input periodic Toda prediction: end-to-end theorem candidate

2026-10-29. **Independently reviewed mathematical construction at polynomial-complexity scope, with the corrections and dependencies below.** This assembles existing derivations into a precise theorem statement, distinguishing a mathematical algorithm from a certified executable and from historical novelty. The substantive review is `latent_integrable_geometry/audit/relative_interface_20261029/POLYNOMIAL_BIT_VERDICT.md`; it accepts the repaired mathematical construction, not all software or a priority claim. No superiority over equally informed inverse-spectral methods is claimed.

## Proposed theorem

Input consists of N>=3, explicit rational a_i>0 and b_i, rational time T, and integer p>=1. Let B be the total binary input length excluding T and p. There is a deterministic algorithm returning rational approximations to every a_i(T),b_i(T) with absolute error <=2^-p in bit time polynomial in N,B,bitlength(T),p.

No spectral-gap, simple-spectrum, nonexceptional-divisor, prescribed-pivot, or lower-norming-weight promise is supplied. Small positive input a_i are charged by their actual rational bit length. The statement is for mathematical Toda instances, not physical data acquisition or approximate integrability. It is not currently a complete certified software claim.

## Exact preprocessing and representations

Compute C=product a_i and the transfer polynomial p_Toda=C tr M by polynomial-time rational arithmetic. Avoid the symbol p for this polynomial in implementation, since p is also output precision. Set F=p_Toda²−4C². Positive periodic Jacobi theory bounds branch multiplicity by two. Exact rational gcd gives K=gcd(F,F'), then reduced squarefree curve F_red=F/K². Its genus g=N−1−deg K. All polynomial coefficient heights are polynomial in N,B; polynomial gcd/division is performed over Q, not a splitting field.

The branch roots of the radical F/K include the closed nodes and have a nonzero integer discriminant after denominators are cleared. The elementary discriminant bound supplies log(1/Delta)=poly(N,B). Root magnitudes satisfy an explicit M=poly(H+1), so log M=poly(N,B). For g=0, return the unique physical isospectral point, namely the initial data.

The principal Dirichlet polynomial G of the initial (N−1)-site Jacobi matrix is computed exactly over Q. Divide G by K to retain the active divisor. Each active mu is represented by a rational isolating interval and its polynomial, with refinable rational approximations. The sheet is obtained from kappa=M11(mu) and y=2C kappa−p_Toda(mu), then y_red=y/K(mu). The denominator is nonzero at active nodes and has a derived separation/height bound. Endpoint coincidences are detected by gcd(G/K,F_red), not by waiting for floating intervals to disjoin. Closed divisor nodes are stored through K and kappa=±1, whose sign is separated by gcd(K,p_Toda∓2C).

No exact primitive element for the compositum of all branch or divisor roots is constructed. All later analytic calculations use independently refinable certified rational enclosures. This prevents a hidden exponential algebraic-field degree from entering the bit claim.

## Initialize, double, reconstruct

1. Obtain the initial physical signed-angle coordinates to the required accuracy on the fixed reduced curve. At endpoints the signed local coordinate is used; evaluating square roots may double requested precision but does not change polynomial complexity.
2. Use `LOCAL_FLOW_INITIALIZATION.md`, with its two audit corrections, to find a small-time divisor on this SAME exact curve. The exact reduced velocity is (0,...,0,-2). Choose m so tau=T/2^m lies inside the derived inverse collar; m=poly(N,B)+O(bitlength(T)).
3. Perform m relative operations E~2D−D0 using the normalized rational rounded-kernel, separated-point and same-sheet root construction. The interface audit must charge the OUTER selected-zero radius, not merely the inner existence radius. At each call, output a fresh fixed-precision signed-angle representation of a genuine physical divisor. No inherited algebraic height is propagated into the next call.
4. Reattach fixed closed nodes and use the full inverse-spectral decoder, including norming weights and finite-Jacobi reconstruction. Use separation of F/K, not merely of F_red, in bounds involving the full divisor. The established positive lower bounds on a_i and norming weights provide polynomial-log physical-output conditioning.

The mathematical group-law argument is classical; it does not require a period matrix. Every short local displacement defines a direct Abel-error lift. Relative doubling doubles the prior lift and adds the current local lift. Nonspeciality gives a unique effective degree-g representative and the explicit inverse collar converts direct error to physical coordinates even if an algebraic section had exceptional intermediate zeros.

## Bit accounting of one relative operation

Let q denote the chosen matrix rounding precision. Each section matrix entry has magnitude <=2^U where U=poly(N,B); the rounded integer matrix therefore has entry height O(q+U). A nonzero exact rational kernel vector can be produced by fraction-free elimination. Minor bounds give normalized coefficient height O(g(q+U+log g)). No lower bound on a numerical singular value is used.

The rational norm polynomial A²−F_red B² has degree at most4g and coefficient height polynomial in g,q,B. Exact gcd(A,B), squarefree factorization, zero multiplicities and the two infinity orders are therefore polynomial-bit operations. The appropriate primary root-isolation import is Mehlhorn–Sagraloff–Wang, *From approximate factorization to root isolation* (ISSAC2013 / JSC2015, DOI10.1016/j.jsc.2014.02.001): rational integer coefficient inputs admit polynomial-bit isolation/refinement of all complex roots with multiplicities. The distinct-root count is available from exact gcd, not an oracle. Their near-optimal bound is not needed; a polynomial bound suffices.

For the reduced coprime pair A0,B0, B0 is nonzero at every root of A0²−F_red B0². A nonzero integer resultant, coefficient heights and root bounds give log(1/|B0(mu)|)=poly(g,q,B), charging the sheet quotient. Common factors and ramification points are treated separately, so this assertion is never applied at a true common root.

The norm/same-sheet lemma demands q polynomial in g,B,log(1/delta); matching and projection have derived polynomial-log margins. Thus each call costs polynomial(N,B,m,p). Fresh rounding to the chosen angle representation prevents algebraic coefficient heights from multiplying across m calls.

## Error budget and outstanding review questions

Let kappa_dec be the derived physical output Lipschitz bound on the physical collar. Set delta<=2^(-m-3) min(eta_col,2^-p/kappa_dec), where eta_col is the uniform inverse-collar radius in direct Abel coordinates. Ensure initialization direct error<=delta, each relative operation adds<=delta, and final decoding error<=2^(-p-1). Then e_m<2^(m+1)delta<=min(eta_col,2^-p/kappa_dec)/4. Thus all uses of the inverse collar are valid even for coarse requested accuracy, and total physical error<=2^-p.

The independent review explicitly checked compatibility of the chart/outer-selection error budget, closed-gap extraction, physical decoder conditioning, and the root-isolation import. Its exact source is MSW arXiv:1301.4870v2 Theorem5, read in full. Remaining archival consolidation and fully certified implementation are distinct from the mathematical polynomial-complexity conclusion. The review is substantive internal review, not exhaustive external peer review of the entire classical Toda literature.

## Consequence and limit

At the repaired reviewed scope, this is a uniform bit-complexity result for full-state exact-input Toda prediction, including degenerate closed gaps. It does not establish a new physical principle, a general integrability-discovery theorem, robustness under unknown perturbations, or historical novelty. The raw hidden-Toda recognition calculation is separate and has a strong linear self-adjoint polar-kernel comparator. Known inverse-scattering methods already compute long-time Toda solutions without time stepping in other settings. Any broader significance must come from a genuinely new transfer or capability, not relabeling this classical composition.

## Initial-sheet correction, 19:28 UTC

The first assembly incorrectly wrote M22 for the initial Floquet multiplier. With T_N...T_1 acting on (psi_1,psi_0)=(1,0), the Dirichlet condition gives psi_N=0 and kappa=psi_(N+1)=M11(mu). M22 is its reciprocal and selects the conjugate sheet. The executed N=3 regression detects a different isospectral physical state if M22 is used. The theorem candidate above is corrected; the rejected regression is preserved by the physical-bridge implementation.

## Explicit bounded representation after arithmetic

Following the review's constructive interface, store each physical oval point using a rational circle coordinate, not its exact algebraic residual from the previous call. From its complex zeta near the unit circle, normalize to modulus one, choose a cardinal rotation with real part at least1/2 using a comparison with slack, and form t=Im(u)/(1+Re(u)). Round t to a fixed-precision dyadic and return the exact circle point ((1-t²)+2it)/(1+t²), rotated back. The parametrization has derivative norm<=2. The two original gap endpoints plus this rational circle point define mu and y on the fixed curve using one square root, with polynomial descriptive degree and height. The fixed D0 remains its ORIGINAL exact algebraic description; errors in interval evaluation of D0 count against each call's delta. Thus neither initial reference drift nor exponentially growing composita are hidden in the theorem.

## Whole-budget correction, 19:29 UTC

The independent review required capping accumulated direct error by eta_col as well as by requested output accuracy. This is now included above. A coarse request p=1 must not permit the proof to leave its inverse collar. The additional precision has only polynomial input size.
