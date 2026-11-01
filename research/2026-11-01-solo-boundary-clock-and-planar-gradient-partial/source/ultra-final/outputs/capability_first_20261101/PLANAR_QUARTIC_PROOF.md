# Planar variational stability: an exact background reduction and a constructive attack

The capability is to decide whether local rank-one stability suffices for the
full planar variational inequality. A finite-valued globally rank-one convex
integrand and one actual compatible gradient with a strict negative Jensen gap
would answer Morrey's 2 by 2 question negatively. This is independent of the
cooperative recurrence and exact-stabilizer programmes.

The attack uses the classical quartic

    f_gamma(A)=|A|^4-2 gamma |A|^2 det A,    gamma=2/sqrt(3).

The following calculations give global rank-one convexity, eliminate ALL affine
backgrounds for each field, and construct compatible fields directly. No negative
gap was found. This does not prove quasiconvexity.

## 1. Global rank-one convexity, with an analytic threshold

Let H have rank one, S=|M|^2, d=det M, t=M:H, e=cof(M):H. Then

    D^2 f_gamma(M)[H,H]
      =4[(S-gamma d)|H|^2+2t^2-2 gamma t e].

By left and right SO(2) rotations reduce to H=e11, M=[[a,b],[c,d]]. Dividing
by four leaves

    3a^2+b^2+c^2+d^2-3 gamma ad+gamma bc.

At gamma=2/sqrt(3) this is exactly

    (sqrt(3)a-d)^2+(b+c/sqrt(3))^2+(2/3)c^2 >=0.

Thus the integrand is rank-one convex on ALL matrices. The first 2 by 2 block
has determinant `3-9 gamma^2/4`, giving necessity of the threshold for gamma>=0.
Changing the sign of one row treats negative gamma. This is a proof, not a
sampled ellipticity test.

## 2. Eliminate the mean exactly

Let G be a mean-zero periodic W^(1,4) gradient, vectorized in row order. Put

    J=[[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]],
    C=<G G^T>, s=trace C,
    r=<f_gamma(G)>,
    b=<4 |G|^2 G-2 gamma (|G|^2 JG+2 det(G)G)>,
    B=2s I+4C-2 gamma(CJ+JC)-gamma s J.

Since `<G>=0` and `<det G>=0`, direct expansion gives the exact identity

    <f_gamma(M+G)>-f_gamma(M) = r+b.M+M^T B M.              (1)

The determinant identity follows by periodic integration by parts and density.
For an actual gradient, its covariance is a positive sum of rank-one ray
covariances: expand its Fourier series and separate real and imaginary parts of
each vector amplitude times its frequency. Global rank-one convexity therefore
implies `M^T B M=(1/2)<D^2 f_gamma(M)[G,G]>=0` for every M. Thus B is positive
semidefinite.

If `b` is in the range of B, minimization of (1) gives

    M_*=-B^+ b/2,       inf_M gap = r-b^T B^+ b/4.           (2)

In general a component of b in ker B would instead give an unbounded negative
gap. For this particular critical quartic it cannot occur. The sum-of-squares
calculation above shows that at a nonzero M its rank-one Hessian nullspace
contains at most one rank-one line, aligned with its smaller singular direction.
If M is in ker B, every Fourier ray of G lies in that line. Write G=hH.
In the rotated coordinates M=diag(a,sqrt(3)a), H=e11, and
`Df_gamma(H):M=4a-2 gamma sqrt(3)a=0`. Therefore `b.M=<h^3> Df_gamma(H):M=0`.
This proves the range condition, including degenerate covariances.

Equation (2) is the decisive remaining inequality for this quartic: prove it
nonnegative for every actual periodic gradient, or construct a field making it
strictly negative. The four-dimensional matrix solve does not remove the
infinite field quantifier. It is an exact reduction, with no novelty claim for
quartic polarization or ordinary quadratic minimization.

## 3. Actual compatible search and exact receiving

`quartic_attack.py` represents a real periodic map by Fourier modes
`|k_x|,|k_y|<=k`, differentiates it spectrally, solves (2), and minimizes the
normalized gap `gap/<|G|^2>^2`. Uniform quadrature on `(4k+1)^2` points integrates
the quartic exactly in exact arithmetic. The optimizer remains floating point;
it uses a numerical pseudoinverse threshold near degeneracy and local starts.

Results retained:

* k=3: 12 starts, best normalized gap 0.5644294446618094.
* k=8: 48 starts, best normalized gap 0.5370339185505667.

All these are positive local-search outcomes, not certified global minima.
Their distance from zero makes this initial attack less promising than a
construction with a sign-changing witness; no failure of the full question is
inferred from that observation.

`exact_checks.py` independently rounds the best map's Fourier coefficients and
mean to a common dyadic denominator 2^20, enforces conjugate symmetry, and uses
INTEGER Gaussian-pair convolution to integrate its polynomial exactly. For this
one rationally reconstructed compatible field, write the unnormalized gap as

    U-(4 sqrt(3)/3)V,
    U=4836477694370464858107760 / 2^80,
    V=1813125122445855436928536 / 2^80.

The exact integers satisfy `U>0,V>0,3U^2>16V^2`, proving its gap is strictly
positive. The normalized value is about 0.537033927174793. This receiving checks
one field at its rounded mean, not every mean or every field.

There is also a genuine negative control. With gamma=6/5 (beyond the rank-one
convexity threshold), M=diag(1,9/5), G=(cos x)/2 e11 is an actual mean-zero
gradient, and its exact Jensen gap is `-117/3200`. Both integer convolution and
the numerical field evaluator recover it. The finite-difference directional
derivative error is below 2.5e-11 on the retained smooth control.

## 4. Governing comparisons

The strongest covering received Astra work was reread at
db0969a8586afaa38137a4371b3457c5576fadea:

* N920 compiles every original physical face once for gradients rank one after
  a common shift; it is not an arbitrary-gradient compiler.
* N921 gives exact finite-tree and stronger quadratic-well obstructions, with
  the received limiting and uniform-integrability scopes kept separate. The
  retained all-output barrier is not a planar compatible-gradient separation.
* N1475 proves a uniform positive gap for the retained fixed quartic's globally
  rank-one convex polynomial extensions on its covariance-boundary classes, and
  an exact scalar-Hessian conic formulation. Its universal actual-Hessian moment
  inequality is still an explicit quantifier. The leading form here is the
  classical ADM quartic, not an assumed instance of that retained leading form.

[Guerra–Teixeira da Costa](https://arxiv.org/abs/2006.09063) search much more general
rank-one convex functions using finite gradient laws and a discrete rank-one
envelope. Their method is a stronger general search reference; our structured
quartic search does not replace it. [Voss et al.](https://arxiv.org/abs/2201.06392)
compare finite elements, neural maps, curl penalties, and laminate methods for
a different isotropic candidate, with no separation obtained. Compatible Fourier
fields and analytic ellipticity here give a specific attack with exact receiving,
not a general numerical superiority claim.

[Cassese v3, September 2026](https://arxiv.org/html/2608.03488v3) constructs
higher-dimensional homogeneous counterexamples and explicitly retains the 2 by 2
question. Those higher-dimensional witnesses cannot simply be transposed into a
planar one. [Pedregal v5, June 2026](https://arxiv.org/html/1905.06571v5) asserts an
affirmative planar proof. Its Section 7 fixed-root construction has the elementary
obstruction below, so it is not used here as an established covering theorem.

## 5. Exact obstruction to the fixed-root step in the claimed proof

This addresses the construction actually stated in Section 7, especially its
assertion after (7.15) that the three sub-mold barycenters are fixed by u and
remain the same for every w. It is not a counterexample to Morrey's conjecture.

Take l=2, the periodic 4 by 4 grid with each square split along the diagonal
with normal (1,1). Let u be the continuous P1 nodal function equal to 1 at
(0,0) modulo the period and 0 at the other 15 nodes. Across the vertical edge
from (0,0) to (0,1/4), its adjacent triangle gradients are

    p=(-4,-4),       q=(0,-4).

Begin with all 192 occurrence weights equal to 1/192. This is an interior point
of Theta_2. That vertical edge occurs in sub-molds 1 and 2. Set delta=1/384.
In sub-mold 1 increase its p-occurrence by delta and decrease its q-occurrence
by delta. In sub-mold 2 make the opposite change. Every interface-pair sum stays
1/96; every physical face's six weights still sum to 1/32; every weight is
positive. Hence the perturbed weights still lie in Theta_2, for any coherent
labeling of these occurrences. Since each sub-mold has mass 1/3 and the original
uniform roots vanish, its new barycenters are

    U_1=3 delta(p-q)=(-1/32,0),
    U_2=(1/32,0),       U_3=0.

Now take the actual compatible map w=u/1024. Every x-component in the support
of its gradient law lies in [-1/256,1/256]. A positive probability measure
supported there cannot have barycenter U_1: its first coordinate -1/32 lies
outside that interval. Thus a sub-laminate with the claimed fixed root U_1
cannot be supported on the gradients of this w. The same obstruction persists
under sufficiently small perturbations of w; it is not repaired by genericity.

Allowing the roots to depend on w would change the fixed-root construction and
would require another proof. Matching the dimension or the linear span of
feasible images does not supply this positivity. The obstruction diagnoses
that argument; it supplies neither a globally rank-one convex separator nor a
negative actual planar variational gap.

## Executable work

`fixed_root_obstruction.py` independently reconstructs all 32 physical gradients,
all 48 periodic edges and all 192 occurrence weights using exact rational
arithmetic. It verifies every one of the 96 pair and 32 physical-face constraints,
strict positivity, all three barycenters, and the target support interval.

The standard-library command is
`env PYTHONDONTWRITEBYTECODE=1 python3 work/capability_first_20261101/fixed_root_obstruction.py`.
`exact_checks.py` uses NumPy only to read the saved array; its integration uses
integer Gaussian-pair arithmetic. Run it with the retained scientific Python
runtime named in BIRTH_CLOCK_PROOF.md. `quartic_attack.py` additionally requires
SciPy; its retained search arguments are `--k 3 --starts 12 --iterations 1400`
and `--k 8 --starts 48 --iterations 2200`, each with `--out <output-directory>`.
