# S5 inverse challenge — independent nonlinear reconstruction and a radial positive theorem

Date: 2026-10-12. Scope: adversarial reconstruction of `S3.md` after the separate S5 affine-system task. S3 and the original S5 files were left untouched. This is an internal alternative derivation, not independent external verification or a priority claim.

## Verdict

The main real sign-pair construction survives the challenge. I found no gap in its ellipticity, separation, nonlinear localized-energy estimate, angular selection, or infinite-dimensional block Schur argument. An independent Schur-complement derivation below proves the same mechanism and improves its constant. The Gaussian KL **equality** needs the policy randomization included in the transcript; the stated upper bound and lower bounds survive unchanged. The lower bound is for calibrated coordinates. It does not establish a positive distance in an unrestricted diffeomorphism quotient.

The radial-shell refinement can be closed as a quantitative finite-dimensional theorem: an explicit moment determinant, a computable inverse bound, a uniform nonlinear Hessian bound, and a contraction reconstruction from D real scalar energy readouts. Its conditioning, prior amplitude, bandwidth, and forward-evaluation costs must remain explicit.

## 1. Setup and separation checked

Let n>=3, 0<r<1, and let a real nonzero psi in C_c^infinity(B_r) be invariant under rotations in the first two coordinates, with support separated from their rotation axis and ||psi||_infinity<=1. For integer s>n/2,

    h_k = psi(rho,z) cos(k theta),
    t = a k^(-s),       0<a<=1/2,
    sigma_+ = 1+t h_k,   sigma_- = 1-t h_k.

All derivatives of theta are bounded on the fixed support. Hence ||h_k||_(H^s)<=C k^s and the perturbations have uniformly bounded H^s norm. Axis separation is necessary for the stated smooth formula with fixed psi; it cannot silently be omitted.

Rotation invariance of psi and the Euclidean volume measure gives ||h_k||_2=||psi||_2/sqrt(2) for every positive integer k. Thus

    ||sigma_+-sigma_-||_2 = sqrt(2) a ||psi||_2 k^(-s).

This exact normalization is correct.

Let E=H^(1/2)(S^(n-1))/constants with harmonic-energy norm ||f||_E^2=integral_(B_1)|grad Hf|^2, where H is harmonic extension. All forms below are complexified sesquilinearly, though real voltages suffice for the statistical conclusions.

## 2. Exact Schur-complement proof, independent of the localized coercivity argument

Let V=H_0^1(B_1), with inner product

    (v,w)_V = integral grad v dot conjugate(grad w).

For fixed real h=h_k, define the bounded self-adjoint operator K:V->V and boundary coupling J:E->V by

    (Kv,w)_V = integral h grad v dot conjugate(grad w),
    (Jf,v)_V = integral h grad Hf dot conjugate(grad v).

Since ||h||_infinity<=1, ||K||<=1. If e_r(f)=||grad Hf||_(L^2(B_r)), then

    ||Jf||_V <= e_r(f).

Write the exact solution at coefficient 1+t h as u_t=Hf+w_t. Its weak equation is

    (I+tK)w_t = -t Jf,
    w_t = -t(I+tK)^(-1)Jf.

This is exact for |t|<1. Define the localized harmonic boundary form

    A(f,g)=integral h grad Hf dot conjugate(grad Hg).

Testing the boundary energy form against Hg instead of u_(t,g), whose difference is in V, gives the exact identity

    Lambda_t-Lambda_0 = t A - t^2 J^*(I+tK)^(-1)J.           (A)

Here adjoints are with respect to the stated energy Hilbert spaces; equivalently (A) is an equality of continuous boundary sesquilinear forms.

Subtracting t and -t and using the elementary resolvent identity yields

    D_t := Lambda_t-Lambda_(-t)
         = 2t A + 2t^3 J^* K(I-t^2 K^2)^(-1)J.             (B)

Because K is bounded and self-adjoint,

    ||K(I-t^2 K^2)^(-1)|| <= 1/(1-t^2).

Together with |A(f,g)|<=e_r(f)e_r(g), this proves the stronger exact bound

    |<D_t f,g>| <= [2t/(1-t^2)] e_r(f)e_r(g).               (C)

S3's coefficient 2t/(1-t)^2 is therefore valid but not needed. Formula (B) is also a direct explanation of why nonlinear scattering does not spoil the real sign pair: every even power of t cancels. Comparing a real oscillatory coefficient to the background zero perturbation would retain even scattering terms and does not have this cancellation.

As a cross-check, S3's original coercivity route is sound: testing the equation for w_t against itself gives ||grad w_t||<=t/(1-t)e_r(f), and hence ||grad u_t||_(B_r)<=e_r(f)/(1-t). The high-frequency boundary datum may scatter into low interior modes, but the **total** correction energy is still bounded by its exponentially small harmonic interior energy. This is why the argument does not assume that the exact solution stays in its original angular character.

## 3. Angular selection by two independent arguments

Write E as the orthogonal sum of rotation-character spaces E_p, p in Z. The harmonic and zero-boundary Dirichlet Laplacians commute with these rotations.

First, rotation by pi/k sends h_k to -h_k and therefore conjugates Lambda_t to Lambda_(-t). It conjugates D_t to -D_t. A block E_p->E_q^* can survive only if

    exp(i(p-q)pi/k)=-1,
    p-q in k(2Z+1).                                         (D)

The pullback convention can reverse p-q, but the allowed set is invariant under sign, so the selection rule is unaffected.

Second, multiplication by h_k shifts angular characters by +k or -k. The Riesz projection defining K and J commutes with rotations. Thus K shifts by +/-k, J does too, and their adjoints have the same set of possible shifts. Expanding (B) as a norm-convergent Neumann series gives

    D_t = 2t A + 2 sum_(j>=0) t^(2j+3) J^* K^(2j+1)J.

Every term has an odd total number of +/-k shifts, hence has total shift in k(2Z+1). This separately reconstructs (D), including all nonlinear orders. In particular, no zero-shift even scattering term survives in D_t.

## 4. Full DN norm: multiplicities do not invalidate the Schur bound

A spherical harmonic of degree ell has rotation weights |p|<=ell. For f_p in E_p, exact harmonic radial integration gives

    e_r(f_p)^2
      = sum_(ell>=max(1,|p|)) ell r^(2ell+n-2) ||(f_p)_ell||_2^2
      <= r^(2|p|+n-2)||f_p||_E^2.                           (E)

The estimate at p=0 deliberately has slack, since constants have been quotiented out and the sum starts at ell=1. Orthogonality in this formula holds on every concentric ball, not merely on the outer sphere.

By (C)–(E), a nonzero block has norm at most

    b_pq = [2t/(1-t^2)] r^(|p|+|q|+n-2)
                       1_(p-q in k(2Z+1)).

For each p, and likewise for each q,

    sum_q b_pq
      <= [2t/(1-t^2)] r^(n-2)
         sum_(j in Z) r^(|(2j+1)k|)
      = [4t/(1-t^2)] r^(k+n-2)/(1-r^(2k)).

Apply the ordinary scalar Schur test to the vectors of block norms (||f_p||_E)_p. The character spaces can each be infinite dimensional; the proof uses their Hilbert norms, not a count of scalar spherical-harmonic basis elements. Therefore

    ||Lambda_(sigma_+)-Lambda_(sigma_-)||_(E->E*)
      <= [4t/(1-t^2)] r^(k+n-2)/(1-r^(2k))
      <= [(16/3) r^(n-2)/(1-r^2)] a k^(-s) r^k.             (F)

This improves the constant 16 in S3 to 16/3 for t<=1/2. The exponent and mathematical consequence are unchanged. The proof extends at the scalar-conductivity level to n=2 as well, with the obvious r^(n-2)=1; n>=3 is needed for the particular conformal metric interpretation in S3.

If all allowed inputs and pairing tests have angular spectrum |p|<=L and 2L<k, every allowed block vanishes exactly. This proves exact finite-bandwidth indistinguishability. A voltage supported in a proper boundary patch generally has angular tails; patch support is not an angular cutoff.

## 5. Noise, adaptivity, and exact wording corrections

Let delta_k be the right side of (F), or the larger valid bound in S3.

For deterministic adaptive energy probes with ||f_j||_E^2<=E_max, the response gap is <=delta_k E_max. If this is <=2nu, midpoint answers give identical transcripts under adversarial errors bounded by nu. The midpoint construction works on the actual query and does not require continuity of the policy. For randomized policies, couple the same internal seed and allow the adversary to observe the actual probe. The observation/output laws can then be made identical. Consequently the maximum expected L2 error across the pair is at least Delta_k/2, and simultaneous success probabilities greater than 1/2 at radius strictly below Delta_k/2 are impossible. A deterministic worst-case error guarantee also fails below that radius. These formulations avoid conflating a randomized risk statement with a deterministic pointwise output claim.

For independent Gaussian noise of fixed absolute variance nu^2, let R be the policy's independent seed and include R with the measured transcript Y. Conditional on (R,Y_<j), the two hypotheses use the same next probe. The exact identity is

    KL(P_+^(R,Y) || P_-^(R,Y))
      = (1/(2nu^2)) E_+ sum_j |Q_+(f_j)-Q_-(f_j)|^2
      <= delta_k^2/(2nu^2) E_+ sum_j ||f_j||_E^4.           (G)

For Y alone, data processing gives the same **upper bound**, but the displayed equality need not hold because conditional readout laws may be mixtures over unobserved policy randomness. Including the chosen action history instead is another valid formulation. Internal randomization is available to the reconstruction algorithm, so the complete transcript is the natural experiment.

Success probability at least 3/4 under each medium at error strictly less than Delta_k/2 gives a binary test with total variation >=1/2. Pinsker then gives KL>=1/2. From (G),

    E_+ sum_j ||f_j||_E^4 >= nu^2/delta_k^2.

Thus the coefficient and asymmetry of S3's energy bound are correct. Fixed maximum query counts or bounded stopping times are sufficient; arbitrary unbounded stopping rules require an additional integrability/truncation justification and are not silently included.

For the target-error asymptotic, one may choose explicitly

    k=floor((sqrt(2)a||psi||_2/(4epsilon))^(1/s))

for sufficiently small epsilon so k>=1. Then Delta_k>=4epsilon and k is bounded above and below by fixed positive multiples of epsilon^(-1/s). This makes the exponential query/energy scaling rigorous without an ambiguous rounding convention. Likewise k of logarithmic order in E_max/nu gives the bounded-noise logarithmic floor.

The noise law, physical input norm, boundary-coordinate calibration, and precision guarantees are assumptions. The argument does not model a detector whose variance falls with time or rises with excitation unless that resource law is supplied separately.

## 6. Gauge audit

For g_sigma=sigma^(2/(n-2)) times the Euclidean metric,

    sqrt(det g_sigma) g_sigma^(-1)=sigma I,

so the scalar conductivity energy is indeed the Laplace–Beltrami energy in these coordinates. The perturbations give comparable fixed-chart metric separation on the stated ellipticity interval.

The two media are rotations of each other. A quotient allowing boundary-moving rotations identifies the pair exactly and has zero separation. Boundary points and voltage patterns must be physically marked for (F) to describe distinguishability of different calibrated specimens.

A self-diffeomorphism of the ball pulling one conformally Euclidean metric to the other is Euclidean-conformal. For n>=3 it is a Möbius transformation. Fixing an open boundary patch pointwise, while preserving the ball, forces identity. The sphere inversion that fixes the sphere pointwise is not a self-map of the ball, so it is excluded. Thus exact inequivalence under that restricted gauge is credible. Nevertheless, exact inequivalence does not by itself lower-bound the infimum of coefficient distance over an unrestricted sequence of boundary-fixed diffeomorphisms. No such positive quotient-distance estimate is proved here.

## 7. Quantitative positive theorem: known ordered radial shells

Fix D>=1, n>=3, and ordered disjoint shells

    0<a_1<b_1<a_2<b_2<...<a_D<b_D<r_0<1.

Let phi_j in C_c^infinity((a_j,b_j)) be supplied, real, nonzero, 0<=phi_j<=1. Consider the known finite-dimensional prior

    sigma_c(x)=1+sum_(j=1)^D c_j phi_j(|x|).

Let Y_ell be any real L2-normalized spherical harmonic of degree ell. Use the D real scalar energy probes

    f_ell=Y_ell/sqrt(ell),     ell=1,...,D,
    ||f_ell||_E=1,
    F_ell(c)=Q_(sigma_c)(f_ell).

These are D scalar readouts, not D full Neumann boundary functions. Their largest harmonic degree is D.

### Moment matrix and an explicit inverse bound

At the background c=0, the exact variational derivative gives

    M_(ell,j) := partial_j F_ell(0)
      = (2ell+n-2) integral_0^1 phi_j(r) r^(2ell+n-3) dr.    (H)

To verify the normalization, Hf_ell=r^ell Y_ell/sqrt(ell). Integrating its radial and tangential gradient energies over a sphere gives radial density (2ell+n-2)r^(2ell+n-3). Its integral from 0 to 1 is exactly one.

Set

    mu_j = integral_0^1 phi_j(r) r^(n-1)dr >0,
    d_* = [product_(ell=1)^D (2ell+n-2)]
          [product_(j=1)^D mu_j]
          [product_(i<j) (a_j^2-b_i^2)] >0.                (I)

By multilinearity of determinants,

    det M
      = [product_ell (2ell+n-2)]
        integral ... integral product_(i<j)(r_j^2-r_i^2)
                          product_j [phi_j(r_j)r_j^(n-1)dr_j]
      >= d_*.

This is a Vandermonde determinant averaged against positive measures with strictly ordered supports. It proves invertibility for arbitrary supplied smooth positive shell profiles, rather than only point masses or an informal discretization.

All entries of M are nonnegative and every row sum is <=1, because the supports are disjoint and sum_j phi_j<=1. Every row of a cofactor submatrix therefore has Euclidean norm <=1, so Hadamard bounds every cofactor by one. Consequently

    ||M^(-1)||_(infinity->infinity) <= D/d_* =: B.            (J)

This conservative bound exposes the cost of narrow shells, small masses, small gaps, and large D. The actual inverse norm may be used for a better certified B.

### A uniform nonlinear remainder bound

Take ||c||_infinity<=1/2. Disjoint supports give ||sum_j e_j phi_j||_infinity<=||e||_infinity. The coefficient stays between 1/2 and 3/2.

For a direction eta=sum_j e_j phi_j, the solution derivative v_eta has zero boundary values and satisfies

    integral sigma_c grad v_eta dot grad w
      = -integral eta grad u_(c,ell) dot grad w.

If ||c||_infinity<=rho<=1/2, coercivity and the trial harmonic extension imply

    ||grad v_eta||_2 <= ||eta||_infinity/(1-rho) ||grad u_(c,ell)||_2,
    ||grad u_(c,ell)||_2^2 <= (1+rho)/(1-rho).

The derivative of F_ell is integral eta |grad u_(c,ell)|^2. Differentiating again in a direction xi gives

    |D^2 F_ell(c)[e,d]|
      <= [2(1+rho)/(1-rho)^2] ||e||_infinity||d||_infinity
      <= 12 ||e||_infinity||d||_infinity.                   (K)

No factor D is hidden here: the disjoint shell supports control the coefficient perturbation in the infinity norm. Smooth dependence follows directly from the uniformly invertible weak operator, for example by its local Neumann series. Integrating (K) along line segments gives

    ||DF(c)-M||_(infinity->infinity) <=12||c||_infinity.      (L)

### Quantitative inverse and reconstruction

Define the explicit prior radius

    rho=min(1/2,1/(24B)).                                   (M)

If the same prescribed H^s radius eta as in the negative theorem is required, also replace rho by min(rho,eta/sum_j ||phi_j(|x|)||_(H^s)). This keeps the entire radial prior inside that smoothness ball and preserves every estimate below.

On the cube ||c||_infinity<=rho,

    ||M^(-1)DF(c)-I|| <=1/2.

Integrating along the line segment between any c,d in this cube proves

    ||c-d||_infinity <=2B ||F(c)-F(d)||_infinity.             (N)

In particular the nonlinear data map is injective on that whole cube. This is an explicit quantitative inverse theorem, not just nonzero determinant at one point.

Suppose the true parameter satisfies ||c_*||_infinity<=rho/2, and the D measured values y obey

    ||y-F(c_*)||_infinity<=zeta,    B zeta<=rho/4.

Starting at c_0=0, perform

    c_(q+1)=c_q+M^(-1)(y-F(c_q)).                           (O)

The derivative of the update map has infinity norm <=1/2 on the cube rho. The ball of radius rho/2 about c_* is contained in that cube, and (O) maps it into itself because the displacement of c_* is <=B zeta. Banach contraction applies, with a unique fixed point c_hat there, and

    ||c_hat-c_*||_infinity<=2B zeta,
    ||c_q-c_*||_infinity
      <=2^(-q)||c_*||_infinity+2B zeta.                     (P)

The second bound follows directly from the error recurrence; it holds for finite iterations without needing the exact fixed point.

If each numerical forward evaluation F(c_q) has certified infinity error <=tau, replace zeta in the invariant-ball condition and (P) by zeta+tau. Thus both detector and computation precision are charged. The supplied matrix M also needs a certified representation/inverse if computed numerically; an inverse error must be included in the contraction certificate rather than ignored.

The physical coefficient error satisfies

    ||sigma_hat-sigma_*||_(L^2(B_1))
      <= [sum_j ||phi_j(|x|)||_2^2]^(1/2) ||c_hat-c_*||_infinity.

### Forward evaluation and the remaining computational interface

Radial symmetry reduces each forward probe to the one-dimensional equation

    (r^(n-1)sigma_c R_ell')'
      -ell(ell+n-2)r^(n-3)sigma_c R_ell=0,
    R_ell regular at 0,       R_ell(1)=1.

Because sigma_c=1 near the outer boundary,

    F_ell(c)=R_ell'(1)/ell.

Thus each iteration requires D radial forward solves, or an equivalent certified forward evaluator. The theorem supplies the convergence rate, the necessary tolerances, and the cost interface. It does not assert a uniform polynomial bit complexity for arbitrary black-box C-infinity shell profiles. Such a runtime claim requires effective supplied profiles, derivative/conditioning bounds, and a certified ODE/quadrature implementation. For explicitly computable fixed profiles these are a conventional numerical-analysis task, rather than a missing inverse-uniqueness bridge.

The positive theorem genuinely uses D scalar readouts for D supplied parameters and charges their conditioning. It does not contradict the smooth-class barrier: the dimension and shell profiles are prior information, rho may shrink rapidly with D, and B may grow rapidly. No uniformly stable reconstruction on the unrestricted H^s class follows.

## 8. Prior-art boundary

[Mandache, *Exponential instability in an inverse problem for the Schrödinger equation*, 2001](https://doi.org/10.1088/0266-5611/17/5/313) is the primary predecessor for exponential inverse instability and EIT consequences. [Isaev, arXiv:1012.2193v1, Theorem 2.4](https://arxiv.org/html/1012.2193v1) explicitly uses a complex angular perturbation proportional to k^(-m)exp(ik theta), and distinguishes that construction from the real-potential entropy argument. The remark immediately after (2.19) says explicit real examples are difficult because of nonlinearity. The sign-pair subtraction in (B) directly addresses the even-order obstruction, but that old remark does not establish present-day novelty; it may concern comparison with zero rather than a pair of rotated real media.

The bounded searches did not settle priority for the real sign-pair formulation, the improved elementary constant, or the exact-bandwidth corollary. They also did not establish novelty for the radial moment inverse, which is a conventional finite-dimensional perturbative inverse argument. [Koch–Rüland–Salo, *On instability mechanisms for inverse problems*](https://arxiv.org/abs/2012.01855), and the finite-prior work cited by S3, remain essential broader comparisons. The defensible outcome is a fully written candidate theorem with explicit interfaces and an internal alternative proof, not an established breakthrough.
