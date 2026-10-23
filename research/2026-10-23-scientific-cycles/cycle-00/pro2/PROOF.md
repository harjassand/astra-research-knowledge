# A checked finite-precision spectral-CDF operation

## 1. Scientific question and scope

For a fixed real symmetric matrix A of order n, recover a simultaneous bound
on F_A(t)=rank(1_{A<=t})/n for every real t, from a small number of matrix-vector
products and a stored finite-precision Krylov calculation. A threshold chosen
after inspecting the result must remain covered. The omitted directions are
not enumerated. This is a question about the whole spectral distribution of a
specified finite operator, not the previously closed molecular energy target.

An ordinary stochastic Lanczos quadrature (SLQ) construction already supplies
Chebyshev–Markov–Stieltjes (CMS) envelopes and simultaneous sampling bounds in
exact arithmetic: Chen, Trogdon and Ubaru (2021), Theorem 2 and Corollary 1,
https://arxiv.org/abs/2105.06595. This work does not claim those constructions.
Chen and Trogdon, https://arxiv.org/abs/2302.14842, Corollary 3.2, also prove a
nearby-starting-vector interpretation of finite-precision Lanczos under their
stated orthogonal-polynomial/regularity and sufficiently-small-error hypotheses.
Their theorem must not be described as absent or replaced in general.

Here the concrete object is an explicitly checked, arbitrary-input backward
completion, its sharp scalar error bound, and a transfer rule that accounts for
eigenvector rotation. A classical grouped-Dirichlet-spacings argument gives a
useful alternate uniform sampling radius. Historical priority of this particular
combination has not been established; the probability mechanism and much of the
numerical-analysis machinery are established. The substantive claim is the
fully specified theorem and executable finite-input operation below.

The public experiment uses the archived NIST stiffness/mass pair bcsstk08 and
bcsstm08. Its target is exactly M^(-1/2) K M^(-1/2) divided by a stated power of
two, with the printed decimal coefficients treated as exact. No assertion about
the error of that finite model relative to an actual building is made.

## 2. Hypotheses that the checker verifies

Let Abar be an exactly stored symmetric matrix and let tau>=0 satisfy
||A-Abar||_2<=tau. Let V have n rows and k columns, 1<=k<=n. Let J be symmetric
tridiagonal of order k with strictly positive subdiagonal entries (vacuous when
k=1). The entries of Abar,V,J are rational dyadics. Define P=I-e_k e_k^T.

Check upper bounds

    gamma >= ||V^T V-I||_F,      gamma < 1,
    M >= ||Abar||_2,            K0 >= ||J||_2,
    r0 >= ||(Abar V-VJ)P||_F,
    xi >= |J_kk-v_k^T Abar v_k|.

Every displayed budget is a mathematical upper bound, not a floating estimate.
In the implementation, integer matrix products give exact Gram/residual entries;
precomputed absolute-sum/Cauchy bounds prove that no int64 intermediate can
overflow. Squared-norm sums use arbitrary-precision Python integers. Integer
square roots provide outward rational root bounds. The public entry points
reject noninteger, nonsymmetric or malformed data and negative allowances.

For the generalized matrix, the parser reads every original decimal as a
Fraction, verifies positive diagonal M, and encloses each sqrt(m_i*m_j) by
rational integer-square-root bounds. It constructs interval enclosures of every
entry K_ij/sqrt(m_i*m_j)/scale, rounds a midpoint to the stored dyadic, and sums
the largest entry discrepancies by row. The maximum full-matrix row sum bounds
the spectral norm of the symmetric difference. This is tau. There is no separate
unaccounted rounded-input operator. The power-of-two scaling is exact.

## 3. Explicit completion and sharp residual bound

Let G=V^T V and Q=V G^(-1/2). This polar factor is a proof device; it is never
computed. Define

    d = gamma/(1+sqrt(1-gamma)),
    r = r0+(M+K0)d,
    z = xi+M d(1+sqrt(1+gamma)).

When k=1 set r=0. Outward scalar arithmetic may replace these by larger values.
The singular-value identity

    sum_i (sigma_i(V)-1)^2
      = sum_i (sigma_i(V)^2-1)^2/(sigma_i(V)+1)^2

proves ||Q-V||_F<=d. Consequently ||(Abar Q-QJ)P||_F<=r and
|J_kk-q_k^T Abar q_k|<=z.

Now set

    D = J-Q^T Abar Q,
    R = (I-QQ^T) Abar QP,
    E = QDQ^T-RQ^T-QR^T,
    B = Abar+E.

These formulas define an actual self-adjoint operator on the original n-space.
They do not require a basis for its omitted complement. Direct multiplication
uses Q^T R=0 and Re_k=0 to give

    BQ=QJ+r_* e_k^T,     r_*=(I-QQ^T)Abar q_k,     Q^T r_*=0.

The last coupling r_* is allowed to be large: it is an ordinary truncation
coupling, not an early-recurrence error that must be discarded or bounded away.
This is the operation that certifies the unrepresented directions.

The best universal bound for this particular completion using only r,z is

    ||E||_2 <= Esharp(r,z) = (z+2 sqrt(z^2+3r^2))/3.             (1)

Here is the full reason. Orthogonal residual splitting gives
||(Abar Q-QJ)P||_F^2=||DP||_F^2+||R||_F^2<=r^2.
Decompose the ambient space into span(q_1,...,q_(k-1)) and its complement.
Then E has blocks [D11,C^T; C,D_kk qq^T], where
||D11||_F^2+||C||_F^2<=r^2 and |D_kk|<=z. For a unit x=(u,v), with s=||u||^2,
joint Frobenius Cauchy–Schwarz gives

    |x^T E x| <= r sqrt(s^2+4s(1-s))+z(1-s).

The maximum over 0<=s<=1 occurs, for r>0, at
s*=2/3-2z/(3 sqrt(z^2+3r^2)) and equals (1). For r=0 it equals z.

Sharpness is constructive. Put f=sqrt(4s*-3s*^2), a=r s*/f and
b=2r sqrt(s*(1-s*))/f. The matrix [a,b;b,z] has first-column norm r, last
diagonal z, and Rayleigh quotient Esharp on (sqrt(s*),sqrt(1-s*)). The bound
just proved shows that this is its operator norm. Set n=k=2,Q=V=I and choose any
irreducible J, with Abar=J-E, to realize it in the stated completion. At z=r,
one obtains E=r[1/3,2sqrt(2)/3;2sqrt(2)/3,1] and norm 5r/3.
This is sharpness given two scalar budgets for this completion, not a claim of
the smallest possible backward error for every observed V,J.

Thus the original target obeys ||A-B||<=e:=tau+Esharp(r,z).

## 4. Why this is an exact quadrature object

Tridiagonality implies e_k^T J^j e_1=0 for j<k-1. The recurrence above gives
B^j q_1=QJ^j e_1 for 0<=j<=k-1. Self-adjointness then gives
q_1^T B^ell q_1=e_1^T J^ell e_1 through ell=2k-2 by splitting ell into two
exponents at most k-1. For ell=2k-1, insert B between B^(k-1)q_1 on both sides
and use Q^T BQ=J. Hence moments match through degree 2k-1.

An irreducible symmetric Jacobi matrix has distinct real eigenvalues and
strictly positive spectral weights at e_1: a zero first eigenvector component
would force all components to vanish by the recurrence. Its k-node measure is
therefore the Gaussian quadrature rule for (B,q_1). This proof includes full
dimension and happy breakdown; no nonzero last residual is imposed.

For nodes theta_1<...<theta_k and weights w_j, the imported classical CMS theorem
gives, at every real t,

    L_J(t)=sum_(j=1)^(k-1) w_j 1{theta_(j+1)<=t}
       <= F_(B,q1)(t)
       <= U_J(t)=w_1+sum_(j=2)^k w_j 1{theta_(j-1)<=t}.       (2)

The exact endpoint convention in (2) is part of the theorem and implementation.
The executable checker isolates every J eigenvalue with integer Sturm signs,
then encloses each Christoffel weight

    w(theta)=1/sum_(j=0)^(k-1) p_j(theta)^2

by directed interval recurrence for the normalized orthogonal polynomials.
Root-bracket upper endpoints and weight lower endpoints produce a lower CMS
step function; root lower endpoints and weight upper endpoints produce an upper
one. The verifier binds every certificate to separately supplied integer J
coefficients and checks the Sturm counts and interval weights again. Success of
a floating eigensolver is never used as a certificate. The small J's Gershgorin
interval isolates its nodes; it is not asserted to contain B's entire spectrum.

## 5. The load-bearing numerical-error mechanism

Weyl eigenvalue perturbation alone cannot transfer a probe-weighted CDF.
Eigenvectors may rotate even when all eigenvalues agree. For example, let

    A=diag(0,1), B=[s^2,s sqrt(1-s^2);s sqrt(1-s^2),1-s^2],
    v=e_1, 0<s<1.

Then ||A-B||=s and both spectra are {0,1}, yet
F_(A,v)(0)=1 > 1-s^2=F_(B,v)(s). A horizontal shift by the operator error alone
is invalid. This disproves that tempting shortcut, rather than merely warning
that it might be inaccurate.

The valid arbitrary-input transfer, for every eta>0, is

    F_(B,v)(t-eta)-min(1,e/eta)
       <= F_(A,v)(t)
       <= F_(B,v)(t+eta)+min(1,e/eta).                        (3)

To prove it, let P=1_(A<=t), Q=1_(B<=t+eta). The Sylvester equation for
P(I-Q) has ordered spectra separated by eta. Its semigroup integral bounds
||P(I-Q)||<=e/eta. For arbitrary orthogonal projections P,Q the largest
eigenvalue of P-Q is at most ||P(I-Q)|| (the two-dimensional canonical-angle
blocks, or a direct Schur-complement argument, prove this, including unequal
ranks). Thus P<=Q+min(1,e/eta)I. Reverse the roles for the lower inequality.
The detailed gap-free endpoint proof and a sharp two-projection refinement are
in notes/projection_lemma.md. The linear leakage constant is sharp in the
unrestricted projection comparison. The experiment uses the simpler additive
version; it does not claim to optimize all available perturbation bounds.

Let u be the normalized stored probe. A checkable starting-vector allowance
beta>=||u-Ve_1||+d bounds |u^T T u-q_1^T T q_1| for every orthogonal projector T.
The factor is one, not two: the two nonzero eigenvalues of
uu^T-q_1 q_1^T are plus/minus sqrt(1-|u^T q_1|^2), which is at most ||u-q_1||.
The norm ||u-Ve_1|| is bounded from exact dot products and an interval for
||g||, not by trusting a floating normalization.

Combining (2),(3) and beta yields a deterministic lower/upper enclosure of the
original probe's spectral measure. B is allowed to depend on the probe; the
stochastic theorem below is applied to the fixed original A, never to B.

## 6. Uniform sampling, with its actual distribution specified

Let s=2m be a positive even integer, n>=2, and let g_1,...,g_s be independent
standard real Gaussian vectors independent of A. Set

    H_A(t)=sum_l g_l^T 1_(A<=t) g_l / sum_l ||g_l||^2.

This is the norm-squared-weighted average of spherical probe measures. It is
not the usual equally weighted spherical SLQ estimator. For every epsilon>0,

    Pr{sup_t |H_A(t)-F_A(t)|>epsilon}
        <= 2 exp(-(ns-2)epsilon^2).                           (4)

Proof: in an eigenbasis of A the n aggregate directional squared norms are
independent chi-square_s. Their normalized weights are Dirichlet(m,...,m).
They are grouped spacings of N=nm-1 independent uniforms, so the cumulative
weight at rank r has joint law U_(rm). Its target r/n=(rm)/(N+1) lies between
(rm-1)/N and (rm)/N. Therefore every |U_(rm)-r/n| is at most the ordinary
empirical Kolmogorov statistic of those N uniforms. The classical two-sided
Dvoretzky–Kiefer–Wolfowitz–Massart theorem gives (4), because 2N=ns-2. Repeated
eigenvalues merely restrict the ranks considered. n=1 is trivial.

This imports DKWM, with a short modern primary proof at
https://arxiv.org/html/2403.16651v1. Dirichlet/order-statistic uses of DKWM exist
elsewhere; no new probability principle or historical priority is asserted.
The complete reduction and a separate raw-Gaussian martingale bound appear in
notes/uniform_probe_bound.md. Odd s is not covered by this integer-spacings
proof. An adaptive number of probes requires confidence spending or another
valid sequential theorem; this experiment fixes s before drawing.

The radius sqrt(log(2/delta)/(ns-2)) has no log(n) term. The CTU2021 comparator
radius sqrt(log(2n/delta)/(s(n+2))) applies to the equal-weight spherical mean.
These are different estimators: the equal-weight mean actually has smaller
pointwise variance for s>1. A better displayed bound is not universal variance
dominance or a demonstrated speedup over all modern SLQ results.

## 7. Finite random inputs and complete confidence contract

The executable generator draws and stores finite uniform bit cells once. It
uses an explicit Box–Muller construction with fixed-point integer interval
logarithm, trigonometry and square root, then rounds to denominator 2^40. Its
checker replays the bits, every arithmetic enclosure and the resulting integer
probe matrix. Ideal continuous uniforms are coupled to the saved bit cells.
A radial cell touching zero causes a declared abort, never a silent redraw.
The excluded-cell allowance and all arithmetic errors are recorded.

For ideal Gaussian block G and saved block Gtilde, a proved coupling
||G-Gtilde||_F<=r_g implies, uniformly over every projector T,

    | ||TG||_F^2/||G||_F^2 - ||TGtilde||_F^2/||Gtilde||_F^2 |
      <= min(1,r_g/||Gtilde||_F)=rho.                        (5)

This follows by flattening the blocks, applying the rank-two projector-distance
identity, and bounding the distance of Gtilde to span(G). Per-column versions
supply the equal-weight comparator's rounding allowance. The bit-level
construction and derivative bounds are documented separately.

The random-bit model is an explicit premise: independent uniform bits. An OS
generator implements the draw; no experiment or checker proves its entropy law.
This is the ordinary probabilistic-computation assumption, not an omitted
floating-point error. The checker proves every deterministic claim for the
saved realization. Probability statements are unconditional failure bounds for
the randomized operation; do not silently condition them on successful
generation or on observing a favorable interval. At fixed delta, adding the
recorded excluded-cell bound gives a conservative wrong-return probability.

For the stored normalized probes u_l and exact norm weights alpha_l, choose any
positive margins eta_l. Combining the preceding results gives

    F_A(t) >= sum_l alpha_l L_l(t-eta_l)
              -sum_l alpha_l(e_l/eta_l+beta_l)-epsilon-rho,
    F_A(t) <= sum_l alpha_l U_l(t+eta_l)
              +sum_l alpha_l(e_l/eta_l+beta_l)+epsilon+rho.   (6)

Clip to [0,1]. One event proves (6) at every threshold, every checked Krylov
depth, and every margin choice for those same fixed probes. Thus intersections
over the prespecified margin grid and threshold choices made after inspection
are valid without another union bound. Reusing the same probes does not permit
choosing A adaptively. Candidate and classical comparator each use their own
delta=0.01 bound; a simultaneous claim about both would use a 0.02 union bound,
plus their stated bit allowances. The dense comparator is deterministic.

## 8. Ordinary verified comparator and honest costs

For a full square dyadic eigenvector proposal W and diagonal D0, check
gamma0>=||W^T W-I||_F<1 and r_full>=||Abar W-WD0||_F. Sorted eigenvalues satisfy

    |lambda_i(A)-sort(D0)_i|
      <= tau+r_full/sqrt(1-gamma0).                          (7)

The complete proof is in notes/full_spectrum_comparator_audit.md: a putative
ordered spectral gap selects a rectangular block of an eigenbasis-transformed
W whose norm is at least sigma_min(W), by a dimension/kernel argument. The
separated Sylvester equation bounds its norm above by residual/gap. Both gap
signs give (7), including multiplicities. This is an ordinary full-spectrum
comparison, not an extension of the rectangular-probe completion.

Counting D0_i+e<=t and D0_i-e<=t yields deterministic all-threshold CDF bounds.
Its floating diagonalization is a proposal only; the full integer Gram and
residual checks pay for completeness. The stronger residual bound is used so
the baseline is not artificially weakened.

For s probes and depth k, proposals and exact residual checks use
O(s*nnz(A)*k+s*n*k^2) arithmetic and O(s*n*k) stored basis entries. The root/weight
certifier adds exact-integer Sturm bisection and interval polynomial recurrences;
its bit costs and runtime are included, not hidden behind k being small.
The present full dense comparator has cubic diagonalization/Gram work and
quadratic storage. Envelope construction and optimization, failed attempts,
independent replay, input construction and source retrieval are also costs.
Measured process receipts are not model-inference, hardware-energy or monetary
accounting; those unobservable costs are explicitly unmeasured.

## 9. What this does and does not settle

The sharp completion theorem and the eigenvector-rotation counterexample hold
for arbitrary finite symmetric inputs satisfying their stated hypotheses.
The implementation gives an actual operation that validates stored proposals
against original coefficients. It does not prove that SLQ is preferable for
small matrices, that global CDF bounds resolve exact ranks cheaply, or that a
large spectral cluster can be resolved by small k at negligible cost.

The actual-data outcome, failures, measured resource table and precise next
scientific boundary are recorded in RESULT.md after the fixed experiment.
All retired molecular results remain closed under their proved scope. No new
claim about that target follows from this different spectral-distribution work.
