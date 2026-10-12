# CRAY: conditional resonance integration and its unresolved global cost

Date: 12 October 2026. Research derivations and executable tests; not independently reviewed, formally verified, or historically priority-cleared.

## 0. Decision and evidence status

This investigation moved away from complex Langevin. The original onsite-quartic integral is retained; no paired quartics are inserted. Two constructions survive:

1. An intermediate-field estimator with explicit rank-local defect, phase, and second-moment bounds. Independent Gaussian draws make it inexpensive on tested strongly gapped inputs. It nevertheless loses the matched practical comparison to transfer quadrature and low-order Wick expansion, and its useful certificate requires an effectively weak-interaction regime.
2. Exact conditional integration across coupled spectral resonances. A Fourier/heat identity provides bounded continuation and finite-order remainder bounds. A genuine two-variable determinant resonance has logarithmically divergent raw second moment while its conditionally integrated answer remains finite. The local identity does not by itself solve global cancellation or acquire an inexpensive decomposition.

The benchmark veto is substantive. Do not continue to market the high-gap estimator as a sign-problem breakthrough. The conditional integration operation is an opening only if a new global acquisition/complexity theorem can make it more than familiar block integration, heat-kernel calculus, or Rao–Blackwellization.

Exact formulas below have mathematical arguments. The executable uses floating-point arithmetic and pseudorandom Gaussian draws. Its coefficient bounds are evaluated in floating arithmetic, not outward-rounded intervals. Stated probability guarantees apply to ideal arithmetic and ideal independent Gaussians. No finite-bit implementation, independent proof audit, real material application, or advantage over all specialised algorithms has been established.

## 1. Independent mechanisms considered

### 1.1 Holomorphic stochastic kernels

A kernel based on an inverse Hessian or inverse drift raises poles, noise-domain compatibility, and integration-cycle issues. This investigation did not acquire a global nonsingular kernel preserving the target cycle for ordinary quartic actions. Stable trajectories were not accepted as evidence of correctness. The old analytic-anchoring result remains research capital, not a premise.

### 1.2 Exact Gaussian-square augmentation

The auxiliary integral of exp[-S(x) -(y+q(x))^2/2] reproduces exp[-S(x)] up to a known constant. The visible q(x)^2 term may appear to supply a desirable positive interaction. At y=-q(x), however, the augmented Hessian has blocks

    [ Hess S + grad q grad q^T,  grad q ]
    [ grad q^T,                 1      ].

Its Schur complement is exactly Hess S. Thus this operation does not manufacture free convexity of the original effective action. This is a failure of this proposed argument, not a theorem excluding every augmented representation.

### 1.3 Contours and sublattice integration

Constant rotations can move the phase into the quartic coefficients and lose convergence at infinity. Integrating an onsite quartic against an imaginary linear field produces a Fourier transform that need not be nonnegative. Neither operation gives positivity for free. More sophisticated contour methods remain strong competitors [P3,P4]; they were not implemented here.

### 1.4 Intermediate fields followed by exact conditional integration

The Hubbard–Stratonovich/intermediate-field identity is established mathematics [P1,P2]. It puts the original integral into a determinant expectation. This allows two questions to be separated: how much determinant weight resides in a spectrally unsafe set, and whether genuine local determinant resonances can be integrated rather than sampled. The quantitative bounds and falsification tests below pursue these questions.

## 2. Scientific input and output

Consider

    Z = integral_R^n exp[-x^T A x/2 - g sum_i x_i^4/4 + i x^T C x/2] dx,

with explicit rational real symmetric A,C and g>0. The global estimator theorem uses

    a_min I <= A <= a_max I,   kappa I <= C <= c_max I,
    a_min>0, kappa>0.

These are ordinary onsite quartics with quadratic interactions. C can have full rank and the graph need not have low treewidth. Positive definiteness of the oscillatory quadratic C is nevertheless a major restriction: this is not a general real-time indefinite kinetic operator, a continuum-limit theorem, or a solver for critical matter.

The input consists of actual matrices, not a sampling oracle. In the benchmark the matrices are weighted Laplacians plus diagonal terms; Gershgorin/energy bounds acquire the displayed constants directly. Generic spectral certification or factorisation must be charged when that structure is absent. Inferring these coefficients from a physical apparatus is not included.

The output is the complex ratio R=Z/Z_G, where

    Z_G=(2pi)^(n/2) det(A-iC)^(-1/2),

to relative accuracy, or a logarithm of R in a certified neighbourhood of its estimate. Tables report log R, not free-energy density. The Gaussian factor and large outputs are represented in logarithmic/scaled form. No expansion of exponentially many output digits is intended.

## 3. Exact real-cycle representation

Let a=sqrt(2g), sigma~N(0,I_n), and

    H(sigma)=A-i(C+a diag sigma).

The elementary Gaussian identity E exp[i sqrt(g/2) sigma_i x_i^2] = exp[-g x_i^4/4] gives

    Z=(2pi)^(n/2) E w(sigma),    w(sigma)=det H(sigma)^(-1/2).

Fubini is justified before Gaussian x integration by A>0: the modulus of the joint integrand is bounded by the integrable real Gaussian times the auxiliary Gaussian. Consequently this computes the original real cycle, rather than a stationary solution of an integration-by-parts equation.

The square-root branch is NOT obtained by taking the principal square root of the scalar determinant. With B=C+a diag sigma and real eigenvalues lambda_j of A^(-1/2) B A^(-1/2), use

    log det H = log det A + sum_j log(1-i lambda_j).

Every factor lies in the right half-plane. This fixes the Gaussian branch continuously. If no-pivot elimination is used, each Schur pivot is accretive and its logarithm gives the same branch. A pivoting implementation must account for branch winding, not only determinant parity. The prototype uses the accretive no-row-swap case and otherwise falls back to the real symmetric congruence formula.

## 4. A computational reference, not a changed physical action

Set b=kappa/4. Define the C1 scalar floor

    r(d)=-3b/2                                      if d<=-2b,
    r(d)=-3b/2+(d+2b)^2/(2b)                        if -2b<d<-b,
    r(d)=d                                         if d>=-b.

It obeys 0<=r'<=1 and 0<=r''<=1/b almost everywhere. Put

    H_tilde=A-i(C+diag r(a sigma_i)),
    w_tilde=det H_tilde^(-1/2),   f=log|w_tilde|.

The imaginary coercivity is

    C+diag r >= (5kappa/8) I.

The original representation remains exact. Using w_tilde instead is an approximation with the relative error proved in Section 6. The floor is not a secretly added physical interaction, an exact contour map, or an uncharged change of target.

Let c=5/8, G=H_tilde^(-1). Then

    ||G|| <= 1/(c kappa),
    Im G=G* (C+diag r) G >=0,
    Re G=G* A G >=0.

Real and imaginary matrix parts coincide with Hermitian parts here because H and G are complex symmetric.

## 5. Acquired curvature and phase bounds

Define the proof measure q proportional to exp[-||sigma||^2/2+f(sigma)]. The algorithm does not need its normalising constant or samples from q.

Direct differentiation gives

    partial_i f = -(a/2) r'_i Im G_ii,

    partial_ij f = -g r'_i r'_j Re(G_ij^2)
                   -g delta_ij r''_i Im G_ii.

The Hadamard square is a compression of G tensor G, so its operator norm is at most ||G||^2. The second term is negative semidefinite. It follows that

    Hess f <= beta0 I,                 beta0=64g/(25 kappa^2),
    ||Hess f|| <= beta,                beta=224g/(25 kappa^2).

The assertions hold almost everywhere and extend to strong convexity by C1 regularity; smooth approximations can justify differentiation of measures. If alpha=1-beta0>0, q is alpha-strongly log-concave.

Choose the continuous unwrapped phase theta=arg w_tilde. Its gradient is

    partial_i theta=(a/2) r'_i Re G_ii.

Since Re G<=a_max ||G||^2 I, the strongly-log-concave Poincare inequality gives

    Var_q theta <= v = 2048 n g a_max^2 /(625 alpha kappa^4).

The phase lower bound requires no winding estimate:

    |E_q exp(i theta)| >= 1-Var_q(theta)/2 >= s=1-v/2.

Indeed center theta by its mean, use cos u>=1-u^2/2, and then take the absolute value. If s<=0 this estimate is uninformative. It is not permissible to assume noncancellation outside the certified regime.

## 6. Rank-local control of spectral defects

Let S={i:a sigma_i<-b}, k=|S|. Original and reference matrices differ only on S. On the complement T they have an identical principal block. Their determinant ratio is therefore the determinant ratio of k-by-k Schur complements.

The true Schur complement has real part >=a_min I. To see this, for v on S set u=(v,-H_TT^(-1)H_TS v). Then

    Re[v* Schur(H) v] = Re[u* H u] >= a_min ||u||^2 >= a_min ||v||^2.

Thus its determinant modulus is at least a_min^k. On S the clipped diagonal is bounded by 3kappa/8 in magnitude. Its Schur complement has norm at most

    B=a_max+c_max+3kappa/8+8(a_max+c_max)^2/(5kappa).

Hence

    |w/w_tilde| <= K^k,       K=max(1,sqrt(B/a_min)).

The potentially harmful factor is local in the number of defects, not exponential in all n coordinates. This is a bound on a specified reference change, not a proof that the global sign problem is local.

### 6.1 Conditional defect probabilities under the relevant weight

Put t=kappa/(4 sqrt(2g)) and suppose t>=1. Holding every other coordinate fixed, f is nonincreasing in sigma_i. Relative to sigma_i=-t, its increase in the lower tail is at most 0.1 and its decrease on [-t,t] at most 0.4. These constants follow by integrating the bound |partial f/partial r|<=1/(2c kappa) over the relevant floor ranges.

Consequently, under q,

    P(sigma_i<-t | sigma_-i)
       <= exp(1/2) Phi(-t)/(1-2Phi(-t))
       <= p=min(1,3 exp(-t^2/2)/(t sqrt(2pi))).

This is a conditional estimate under the determinant-magnitude law, not merely the original independent Gaussian law. Iterated conditioning gives P(S contains J)<=p^|J| for every set J, without independence. Therefore

    E_q K^|S| <= (1+(K-1)p)^n.

Since |w-w_tilde|/|w_tilde| <= (K^|S|+1) 1_{|S|>0},

    |Ew-Ew_tilde| <= Delta E|w_tilde|,
    Delta=(1+(K-1)p)^n-1+2np.

If s>Delta, then |Ew|>0 and

    relative floor bias <= Delta/(s-Delta).

A tiny raw Gaussian defect probability alone would not suffice. The rank factor and determinant-weighted conditional bound are both needed.

## 7. Independent sampling: construction and second moment

The maximiser mu of f(sigma)-||sigma||^2/2 satisfies mu=grad f(mu). When beta<1, fixed-point iteration acquires it with contraction factor beta. Each dense evaluation computes a matrix factorisation and inverse diagonal. An approximate mode is accompanied by its residual r0=||grad f(mu)-mu||; its cost is not omitted.

Sample z~N(0,I), independently, set sigma=mu+z, and evaluate

    Y=exp[F(mu+z)-F(0)-mu^T z-||mu||^2/2],
    F=-log det H_tilde/2.

Then E Y = E w_tilde / w(0), the reference ratio. There is no Markov chain, burn-in, step size, or unknown proposal normaliser.

### 7.1 Second-moment theorem

For an exact mode, beta<1/2, and s>0,

    E|Y|^2/|EY|^2 -1
      <= V = exp[n beta^2/(1-2beta)^2]/s^2 -1.

Proof: let h(z)=f(mu+z)-f(mu)-mu^T z, so grad h(0)=0 and ||Hess h||<=beta. Write A(t)=log E_N exp[t h]. For 0<=t<=2 the tilted potential is (1-t beta)-strongly convex. Integration by parts gives

    E_t||z||^2 <= n/(1-t beta),

and Poincare gives

    A''(t)=Var_t h <= n beta^2/(1-t beta)^2.

The second difference A(2)-2A(1)+A(0) is the integral of A'' over a unit square and is at most n beta^2/(1-2beta)^2. Divide by the phase lower bound squared.

For an approximate mode let ell=1-2beta>0. A valid replacement exponent is

    D = [r0(1+2beta/ell)+beta sqrt(n/ell)]^2/ell.

To obtain it, integration by parts yields sqrt(E_t||z||^2)<=sqrt(n/ell)+2r0/ell. Bound ||grad h|| in L2 by r0+beta sqrt(E_t||z||^2), then apply Poincare. The executable uses this residual correction.

For N independent samples, complex Chebyshev gives

    P(|Ybar-EY|>epsilon_mc |EY|) <= V/(N epsilon_mc^2).

If delta_floor=Delta/(s-Delta), the total relative error against the original ratio is at most

    epsilon_mc(1+delta_floor)+delta_floor

on the sampling event. The results file reports sampling and floor bounds separately. The stated 95% bounds assume exact arithmetic; pseudorandomness and floating evaluations are not silently certified.

## 8. Local spectral heat continuation

The high-gap method is not enough: its useful domain is perturbatively easy. Instead of excluding a resonant local region, restore and integrate a quartic degree of freedom before sampling its determinant contribution.

Let g>0, real J!=0, Re d>=0, and Re h>0. Define

    f(x)=exp[-d x^2/2-g x^4/4],
    J_g(s)=(2pi)^(-1/2) integral_R exp[-s x^2/2-g x^4/4] dx.

A two-coordinate block with purely imaginary cross-coupling iJ yields the exact conditional factor

    F(h)=h^(-1/2) J_g(d+J^2/h).

For example, in the intermediate-field representation, conditioning all but the auxiliary variable on the quartic site gives precisely this factor. Equivalently it is the normalized integral over a Gaussian coordinate z and a quartic coordinate x with exponent -h z^2/2-d x^2/2-g x^4/4+iJzx.

With unitary Fourier convention,

    F(h)=1/(|J| sqrt(2pi)) integral fhat(k) exp[-h k^2/(2J^2)] dk
        =1/|J| [ exp(h partial_x^2/(2J^2)) f ](0).

For positive real h this follows by elementary Fourier Gaussian integration. Both sides are analytic for Re h>0, so the identity extends throughout that half-plane with the accretive Gaussian branch. Because f is Schwartz and fhat is integrable, dominated convergence extends it continuously to Re h=0.

It follows that

    sup_{Re h>=0}|F(h)|
       <= ||fhat||_1/(|J| sqrt(2pi))
       <= sqrt(||f||_2^2+||f'||_2^2)/(sqrt(2)|J|),

and

    lim_{h->0, Re h>=0} F(h)=1/|J|.

This is a one-sided smooth continuation. It is NOT a proof of a holomorphic removable singularity in a full disk around zero; the heat Taylor series need not converge as an infinite series.

### 8.1 Acquired finite-order error

Define

    F_p(h)=1/|J| sum_{j=0}^p (h/(2J^2))^j f^(2j)(0)/j!.

The integral Taylor remainder for exp(-h k^2/(2J^2)) has modulus at most (|h| k^2/(2J^2))^(p+1)/(p+1)! when Re h>=0. Cauchy–Schwarz with weight 1+k^2 and Plancherel give

    |F-F_p| <= (|h|/(2J^2))^(p+1)
       *sqrt(||f^(2p+2)||_2^2+||f^(2p+3)||_2^2)
       /(sqrt(2)|J|(p+1)!).

Derivative polynomials are explicitly acquired:

    P_0=1, P_(j+1)=P_j'-(d x+g x^3)P_j,  f^(j)=P_j f.

For Re d>=0, their norms can be bounded by absolute polynomial coefficients and even moments of exp(-g x^4/2):

    integral_R x^q exp(-g x^4/2) dx
        = (1/2)(2/g)^((q+1)/4) Gamma((q+1)/4),  q even.

At order two,

    F_2(h)=1/|J| [1-dh/(2J^2)+(3d^2-6g)h^2/(8J^4)].

Fixed-order acquisition and evaluation are elementary polynomial/special-function work. Large order, large |d|, small |J|, and many-dimensional blocks are not free. Gamma values and arithmetic require outward rounding for a certified numerical enclosure; that backend is not implemented.

### 8.2 Important limitation: a small pivot need not be a genuine resonance

The determinant of [[h,-iJ],[-iJ,d]] is hd+J^2. At h=0 it is J^2, not zero. Stable block factorisation already avoids the spurious h^(-1/2) divergence created by premature scalar elimination. Therefore the h->0 example alone does NOT demonstrate removal of a difficult sign problem or a numerical advantage over pivoted factorisation.

What is operationally meaningful is exact conditional averaging across a TRUE determinant-zero region, addressed next. Even that remains a local result, not a proof of improved global average phase.

### 8.3 Genuine determinant resonance: logarithmic second moment versus bounded mean

Let epsilon>0 and U~N(0,1), and set

    M_epsilon(U)=[[epsilon-i, -i],
                  [-i, epsilon-i(1+sqrt(2) U)]].

This is the two-site g=1 onsite-quartic model after conditioning the first auxiliary variable at zero. Put h=epsilon-i, d=epsilon-i, a=sqrt(2),

    m_epsilon=epsilon[1+1/(1+epsilon^2)],
    u_epsilon=-epsilon^2/[sqrt(2)(1+epsilon^2)].

Then

    |det M_epsilon(U)^(-1/2)|^2
       =1/(|h| sqrt(m_epsilon^2+a^2(U-u_epsilon)^2)).

As epsilon decreases, the determinant really vanishes at U=0 in the limiting matrix. Splitting the Gaussian integral into a small interval around u_epsilon and its complement gives

    E |det M_epsilon(U)^(-1/2)|^2
       = (1/sqrt(pi)) log(1/epsilon)+O(1).

The coefficient follows from integrating du/sqrt(m^2+a^2u^2) across both sides of zero: 2 phi(0)/a=1/sqrt(pi). The bounded remainder follows by subtracting phi(u_epsilon) locally; the Gaussian density is smooth and u_epsilon=O(epsilon^2).

In contrast, the conditional mean is exactly F(h), with d also equal to epsilon-i, and tends to

    exp(i pi/4) J_1(0),
    J_1(0)=Gamma(1/4)/(2sqrt(pi)) = 1.022765672113... .

Thus exact conditional integration removes a genuine local logarithmic variance singularity. It does not remove a demonstrated exponential global sign problem. Direct scalar special-function evaluation or block quadrature already computes this two-variable problem affordably; the local identity's historical novelty is not claimed.

### 8.4 Block extension and acquisition cost

For real invertible B of size r, complex symmetric H with Re H>0, and Schwartz f on R^r,

    det(H)^(-1/2) (2pi)^(-r/2)
       integral f(x) exp[-(B^T x)^T H^(-1)(B^T x)/2] dx
    = 1/(|det B|(2pi)^(r/2))
       integral fhat(k) exp[-k^T B^(-T)H B^(-1) k/2] dk.

The limit at H=0 within the accretive cone is f(0)/|det B|. The real invertible coupling maps all covered directions into smoothing directions. If B is singular, uncovered directions remain. If B has tiny singular values, determinant and derivative bounds may be expensive. If B is complex, accretivity of the transformed heat matrix is not guaranteed.

In many dimensions, Fourier L1 norm bounds and exact block integration can be exponential. A general graph does not automatically supply a good pairing or small blocks. Eliminating preceding coordinates can make cross-couplings complex and create nonlocal fill, so the real-B theorem cannot simply be applied recursively without proof.

## 9. Numerical and algebraic evidence

All timings are single runs in the supplied container with one BLAS thread. Floating agreement is not an interval enclosure. The nonlinear target inputs are independently seeded connected heterogeneous rational chains/grids. No samples were selected by agreement with the reference.

### 9.1 Matched 16-site chain

A=.5I+weighted real Laplacian; C=35I+another weighted Laplacian; g=1. All methods receive the same coefficients and output log(Z/Z_G).

- Transfer quadrature, 512 nodes on [-5,5]: log ratio 0.009334535727905553 - 0.0003558447543503082 i; 0.111637 seconds.
- Independent centred auxiliary estimator, 25,000 draws: 0.009350328699386512 - 0.000381454813487244 i; 0.939319 seconds sampling plus 0.000860 seconds mode acquisition. Complex log error against transfer: 3.00881e-5.
- Two-order Wick expansion: 0.009334349885733008 - 0.00035582348088394124 i; 0.000095833 seconds. Complex log error: 1.87056e-7.

Transfer orders 320 and 512 agree to approximately 6.2e-13. Order 192 was under-resolved and gave a visibly wrong answer; its output is retained. No rigorous transfer quadrature truncation/roundoff enclosure was constructed.

For completeness the Wick terms, with G=(A-iC)^(-1), are

    L_1=-(3g/4) sum_i G_ii^2,
    L_2=(9g^2/4) sum_ij G_ii G_jj G_ij^2
        +(3g^2/4) sum_ij G_ij^4.

This is an asymptotic approximation without a general remainder certificate here. Its empirical success is not a certified comparison. Nonetheless it strongly contradicts a claim that these tested inputs were unaffordable for specialised methods.

### 9.2 Connected square grids

The complete input matrices are retained in NPZ files. The reference output is not known independently at larger sizes; agreement with Wick is diagnostic only.

| Sites | kappa | Draws | Sampling seconds | Ideal 95% relative sampling bound | Relative floor bias bound |
|---:|---:|---:|---:|---:|---:|
|16|35|25,000|0.833657|0.00086447|2.60675e-7|
|64|50|25,000|2.312678|0.00085710|1.86633e-15|
|256|70|4,000|7.329843|0.00218718|3.17771e-31|

The empirical relative variances are about 7.1e-6, 7.7e-6, and 8.1e-6. The uncentred intermediate-field estimator's empirical relative variances are about 0.0063, 0.0120, and 0.0258. This is a comparison against another exact representation, not solely against direct phase averaging. The modest improvement still does not establish hard-regime superiority.

The same grid Wick calculations took approximately 0.00046, 0.00057, and 0.00851 seconds. Their proximity to the stochastic estimates does not establish their true errors or a certified full-grid ground truth.

### 9.3 The useful certificate retreats at ordinary couplings

At n=16 the conservative floor-bias bound is uninformative for kappa through 16, about 0.183 at kappa=20, 0.00378 at 25, 4.54e-5 at 30, and 2.57e-7 at 35. These are different generated fixtures from the main table, with the seed policy preserved in code.

Thus removing the previous engineered quartics did not establish a useful certificate for ordinary moderate oscillatory gaps. The regime g/kappa^2 small is precisely one where Gaussian perturbation is a serious competitor.

### 9.4 Heat and genuine-resonance checks

For g=J=1, d=.2-.7i, h=1e-4, the bare scalar pivot has magnitude 100. The conditionally integrated value is approximately

    0.9999899908129648 + 0.00003499894860666138 i.

The degree-two heat polynomial has observed error about 1.47e-12 and an analytic remainder majorant about 7.55e-9. At h=.1 the same conservative majorant is 7.55 and is useless. Both are retained. Twelve real/complex-ray checks were compared with a 70-digit Bessel-K formula, subsequently cast to double for diagnostics. They are not interval proofs.

For the genuine-resonance fixture, epsilon=1e-12 gives raw second moment about 15.81737, while the conditional mean modulus is about 1.02276567211248. The difference between the raw second moment and log(1/epsilon)/sqrt(pi) tends numerically to 0.2282368863384. This agrees with the analytic logarithmic divergence and bounded mean.

Twenty rational matrix fixtures generated 200 exact assertions concerning Schur determinant bounds, curvature, and inverse diagonal signs; all passed. An initial Python Boolean-counting issue in the diagnostic was corrected without changing a scientific formula. These are finite checks, not proof assistants or independent validation.

## 10. Resource accounting and physical scope

For dense matrices, reading and storing explicit input is O(n^2) numbers; sparse input still may create dense factorisations. Each sample in the delivered implementation uses O(n^3) arithmetic operations and O(n^2) memory. The mode iteration costs the same order per iteration and contracts at beta when the gate passes. Each sample requires n independent Gaussian variates and a known Gaussian likelihood ratio. No mixing or stochastic differential-equation bias is present.

Sample count can be chosen as ceil(V/(delta epsilon_mc^2)). This is a simple Chebyshev guarantee, not an optimal confidence dependence. Repeated independent blocks could improve confidence scaling but are not implemented or needed for the reported tests.

The Gaussian normalization uses a branch-safe factorisation. Conditional heat calculations acquire derivative coefficients explicitly. Matrix inverse norms, positive damping a_min, gap kappa, input norm bounds, small coupling-block singular values, and phase lower bounds all enter the quantitative costs. None should be replaced by an assumed compact certificate.

The executable is not a finite-bit certified solver. Completing that contract requires: outward-rounded coefficient/gate evaluation; truncation and coupling/error accounting for the Gaussian random source; interval or backward-error-controlled branch-safe matrix factors; a residual certificate for the acquired mode; and allocation of all evaluation error to the final relative target tolerance. General polynomiality in the binary lengths of arbitrarily large or ill-conditioned input coefficients is not claimed. The current statistics alone do not certify a fixed floating precision.

No experimental samples are needed for the explicitly supplied mathematical model. This does not account for calibrating a laboratory Hamiltonian/action or for model discrepancy. There are no quantum gates or physical-time speedup claims. The output is one partition ratio (or a specified finite set of observables after separate numerator bounds), not exponentially many observables for free.

## 11. Comparators and complexity boundaries

Intermediate fields, loop-vertex resummation, Laplace/mode-centred importance sampling, heat kernels, Schur complements, and conditional integration all have established antecedents [P1,P2,P5]. Their appearance cannot establish historical originality.

Optimised contours and complex normalising flows have already been demonstrated on complex scalar field calculations [P3]. The present study did not implement their strongest versions or a two-dimensional tensor-network method. No empirical or theoretical superiority over them is asserted. A chain transfer calculation is the executed tensor/contraction-style baseline; two Wick orders test whether the certificate merely selects an easy perturbative regime. Constructive interpolation/resummation algorithms remain relevant and were not exhaustively benchmarked.

Generic sign-problem hardness is known from specific fermionic constructions [P6]. It is not a reduction proving this onsite-quartic family hard. Conversely, the positive-gap restriction avoids rather than refutes those generic barriers. Contour-only lower bounds for particular complex-coupling gauge models [P4] are another caution: they do not prohibit partial integration, and they do not prove hardness of the target here.

## 12. Exact open obligation and strongest next attack

The surviving opportunity is to acquire small conditional-integration blocks that cover TRUE resonances at fixed, ordinary couplings and weak damping. A theorem must control the actual weighted contribution, not raw auxiliary probability.

Required steps, all presently unproved in the intended broad class:

1. From the actual rational lattice coefficients, construct a partition or decomposition of contributing configurations into manageable resonant blocks. If the block is chosen using an auxiliary coordinate that is later integrated out, its selection event must remain inside the conditional integral. Dropping that condition is biased.
2. Establish that blocks have affordable size and well-conditioned real coupling coverage, or provide a genuinely different operation for complex/singular couplings. Coupling singular values, Fourier norms, and fill-in must be charged.
3. Bound large-block contributions under the determinant-weighted measure. The desired coefficient-derived bound resembles summable connected-block activities, not an assumed high-temperature or cluster oracle.
4. Prove that the remaining global complex mean is large enough relative to residual absolute weights and estimator variance. Bounded local factors do not imply a polynomial global sign.
5. Compare a fully acquired implementation at identical outputs and accuracy with contour, tensor, transfer where applicable, and constructive/interpolation methods on a nonfactorising ordinary-coupling family.

A schematic goal is a coefficient-acquired activity estimate

    sup_v sum_{connected S containing v} exp(c|S|) ||actual block activity(S)|| < 1,

with constants and block-evaluation costs that do not deteriorate exponentially with damping, size, or requested precision. This is a target, NOT a supplied premise or an already obtained algorithm. Deriving only a standard weak-coupling cluster expansion would not be the desired advance over existing constructive methods.

**Research decision:** preserve the rank-local defect and exact conditional-heat results, but stop the high-gap estimator as a breakthrough direction. Do not claim the local cancellation primitive itself is historically new. The missing mathematics is a globally affordable, representation-acquired treatment of coupled resonances and their remaining phase. Without that theorem, the operation makes small blocks obtainable, not a previously unaffordable consequential many-body answer.

## Primary references

[P1] J. Magnen and V. Rivasseau, Constructive phi^4 field theory without tears, arXiv:0706.2457 (2007); Annales Henri Poincare 9, 403–424 (2008).
[P2] V. Rivasseau and Z. Wang, How to Resum Feynman Graphs, arXiv:1304.5913v2 (2013).
[P3] S. Lawrence, H. Oh, Y. Yamauchi, Lattice scalar field theory at complex coupling, Phys. Rev. D 106, 114503 (2022), arXiv:2205.12303.
[P4] S. Lawrence and Y. Yamauchi, Convex optimization of contour deformations, Phys. Rev. D 110, 014508 (2024).
[P5] C. Schillings, B. Sprungk, P. Wacker, On the Convergence of the Laplace Approximation and Noise-Level-Robustness of Laplace-based Monte Carlo Methods for Bayesian Inverse Problems, arXiv:1901.03958v4 (2020).
[P6] M. Troyer and U.-J. Wiese, Computational complexity and fundamental limitations to fermionic quantum Monte Carlo simulations, Phys. Rev. Lett. 94, 170201 (2005), arXiv:cond-mat/0408370.

These sources provide prior art and comparison context. The new inequalities above are derived in this note rather than imported from unreviewed Astra results. Source abstracts and available primary HTML were consulted selectively; this is not an exhaustive priority audit or an independent proof review of all cited papers.
