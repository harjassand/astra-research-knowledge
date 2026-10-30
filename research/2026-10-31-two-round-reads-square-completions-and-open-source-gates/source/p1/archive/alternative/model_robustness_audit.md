# Focused audit: acquired quadratic model and numerical certificates

30 October 2026. Root's robustness and finite-precision claims independently checked. No new literature search is needed for these direct algebraic consequences.

## Transfer of a compiler guarantee through L2 model error

Fix one input law and one class of admissible observation policies. For each policy pi, let P_pi denote conditional expectation given its full transcript, including independent random seed. Conditional expectation P_pi and its complementary orthogonal projection I-P_pi are L2 contractions.

Suppose `||f-fhat||_2<=tau`. Suppose a compiler chooses a policy pi_hat and returns the exact conditional predictor `P_pi_hat fhat`, with

`||(I-P_pi_hat) fhat||_2 <= inf_{pi: cost<=k} ||(I-P_pi) fhat||_2`.

The compiler may use k+1 reads; only the right comparator class is restricted to k. Then

`||f-P_pi_hat fhat||_2`

`<= ||f-fhat||_2 + ||(I-P_pi_hat) fhat||_2`

`<= tau + inf_pi ||(I-P_pi) fhat||_2`

`<= 2tau + inf_pi ||(I-P_pi) f||_2`.

Squaring gives the stated guarantee:

`sqrt(MSE_true)<=sqrt(R_ad,true(k))+2tau`.

The last line follows because `||(I-P_pi)(fhat-f)||_2<=tau` for every comparator policy. Infima need not be attained. The same proof works for a specified benchmark policy, or any other common comparator family, and does not require a Gaussian law. The Gaussian quadratic theorem supplies the compiler guarantee in the intended application. The input law and available observation experiments must remain the same on both sides; distribution misspecification is a separate issue.

The deployed predictor is the surrogate conditional predictor. It need not be the true target's Bayes predictor; the first triangle inequality explicitly pays for this mismatch.

If calibration is random but independent of the future input, apply this statement conditional on the acquired model. The known input law is then unchanged. A calibration procedure that itself reveals the future input needs its own conditional-law accounting.

## Paid interpolation of a promised quadratic

For a promised quadratic `f(x)=x^T A x+b^T x+c`, A symmetric, query the stencil

* 0;
* +e_i and -e_i for every i;
* e_i+e_j for every i<j.

Its cardinality is `1+2n+n(n-1)/2=(n+1)(n+2)/2`, the number of quadratic coefficients. Reconstruct

`c=f(0)`,

`b_i=[f(e_i)-f(-e_i)]/2`,

`A_ii=[f(e_i)+f(-e_i)-2f(0)]/2`,

`A_ij=[f(e_i+e_j)-f(e_i)-f(e_j)+f(0)]/2`, for i<j.

If every evaluation has deterministic absolute error at most nu, then

`|delta c|<=nu`, `|delta b_i|<=nu`, and `|delta A_ij|<=2nu`.

Under X~N(0,I), the exact squared model error is

`tau^2=2||delta A||_F^2+||delta b||^2+[tr(delta A)+delta c]^2`.

Consequently the root's bound is valid:

`tau^2<=(12n^2+5n+1)nu^2`.

The mean error is included. Bounding only the centered variance would omit its final square and would not justify the transfer guarantee.

### Optional exact sharpening for this stencil

Because the errors in different coefficients share the same evaluations, the exact worst-case constant for this interpolation rule is smaller:

`tau^2<=(12n^2-4n+1)nu^2`.

It is attained by error +nu at 0 and all e_i+e_j, and -nu at every +e_i and -e_i. Then delta c=nu, delta b=0, the diagonal of delta A is -2nu and every off-diagonal entry is +2nu.

To prove the upper bound, normalize nu=1. The squared L2 error is a convex quadratic in the evaluation errors, so its maximum on their cube occurs at a vertex. Global sign symmetry permits e_0=+1. For fixed errors e_{+i}, each pair evaluation can be chosen to maximize the corresponding squared off-diagonal entry. That maximum absolute entry is 2 when both e_{+i}=e_{+j}=-1, and 1 otherwise.

All diagonal errors are nonpositive. Let S=1 plus the sum of the other diagonal errors, so S<=1. Changing e_{-i} from +1 to -1 improves the objective by at least 6 if e_{+i}=-1, and at least 2 if e_{+i}=+1: these are the changes in `2 A_ii^2+b_i^2+(S+A_ii)^2`. Thus all e_{-i}=-1 at a maximum. Next changing e_{+i} from +1 to -1 improves that same diagonal/linear/mean contribution by at least 6, while never reducing any optimally chosen off-diagonal square. Hence all e_{+i}=-1 too. The attaining errors described above follow, and the exact value is `8n^2+(1-2n)^2=12n^2-4n+1`.

Exact enumeration over every error-cube vertex for n=1,2,3 gave maxima 9,41,97, matching this formula. The simpler conservative constant is valid if preferred for the main report.

### Finite interpolation does not establish the model class

The promise that the target is quadratic is substantive. A function can agree at every acquisition point and differ arbitrarily in L2: `h(x)=L x_1(x_1^2-1)` vanishes at this entire stencil, while `E h(X)^2=10L^2`. Thus arbitrary model adequacy cannot be inferred from stencil agreement. A broader target requires an independently earned approximation guarantee tau.

## Exact certificate for an arbitrary final direction

Let U have orthonormal columns and let the noiseless first batch reveal U^T X. Write `m=UU^T X`, `Q=I-UU^T`, `D=QAQ`, and `t=Q(b+2Am)`. Conditional on this first batch, X=m+Z with Z~N(0,Q).

Choose any unit w in range(Q), measurably from the first observations, and read `z=w^T X`. The correct final conditional predictor is

`m^T A m+b^T m+c+tr(D)+(t^T w)z+(w^T A w)(z^2-1)`.

The exact risk averaged over the final read and remaining coordinates, conditional on the first stage, is

`2[||QAQ||_F^2-(w^T A w)^2]+||t||^2-(t^T w)^2`.

This follows from the first-stage residual variance `2||D||_F^2+||t||^2` and the orthogonal Gaussian first- and second-chaos gains `(t^T w)^2` and `2(w^T D w)^2`. It is also a direct numerical certificate: the linear alignment loss is nonnegative and explicit. If w is only approximately aligned, the predictor must use `t^T w`, not replace it by `||t||` without separately accounting for that coefficient error.

For an approximate residual vector `t_hat` in range(Q), choose `w=t_hat/||t_hat||`. The uncaptured linear variance satisfies

`||t||^2-(t^T w)^2=||(I-ww^T)(t-t_hat)||^2<=||t-t_hat||^2`.

If `t_hat=0`, skip the read and the same upper bound holds. Thus an absolute mean squared gradient approximation error is enough; no relative-angle accuracy is needed when t is tiny.

If the implemented decoder also uses the approximate coefficient `||t_hat||` rather than the exact t^T w, its exact risk is instead

`2[||QAQ||_F^2-(w^T A w)^2]+||t-t_hat||^2`.

Here the constant and quadratic conditional-mean correction are assumed exact. The quadratic residual is orthogonal to the linear residual `(t-t_hat)^T Z`. This version directly certifies an approximate-gradient implementation.

## Approximate angles and spectral precision

Inside a true orthogonal eigenvector pair with eigenvalues +lambda and -mu, use any normalized rotation with coefficients c,s. If the queried direction is `c e_+ - s e_-`, the unobserved direction is `s e_+ + c e_-`, whose residual Rayleigh coefficient is

`delta=lambda s^2-mu c^2`.

For disjoint true eigenpairs, the compressed matrix consists of the untouched signed tails plus these scalar delta blocks. Exact final gradient alignment therefore gives risk at most

`B(k)+2 sum_j delta_j^2`.

Rational coefficients on the unit circle can preserve exact orthonormality; for example c=(1-r^2)/(1+r^2), s=2r/(1+r^2). This statement needs no separation between eigenvalues.

For an arbitrary approximate eigenbasis, off-block residual couplings also contribute. Diagonal Rayleigh residuals alone do not certify risk: a residual block [[0,L],[L,0]] has zero diagonal and nonzero Frobenius norm. Use the full `||QAQ||_F` certificate, or a separately justified matrix-model error bound, to include these couplings. Exact inertia claims require certified eigenvalue signs; an approximate-risk theorem does not require resolving nearly zero signs exactly.

## Focused executable check

`check_model_robustness.py` writes `check_model_robustness_results.json`. It enumerated all 1,096 interpolation-error vertices in dimensions 1,2,3 using exact rational arithmetic, confirming maxima 9,41,97. It also passed 40 noiseless arbitrary-direction/approximate-gradient certificates and 27 noisy zero-compression approximate-gradient certificates by tensor three-point Gaussian quadrature. The conditional squared residuals are degree-four polynomials, so those integrations are exact in exact arithmetic. Maximum absolute discrepancies were 2.49e-14 and 4.27e-14 respectively. These finite checks supplement the proofs.
