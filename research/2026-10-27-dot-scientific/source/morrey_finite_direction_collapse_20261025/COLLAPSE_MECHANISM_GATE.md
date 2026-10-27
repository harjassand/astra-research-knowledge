# Iterated positive contractions: exact convergence, an actual stationary root, and the missing collapse criterion

25 October 2026. This preserves the genuine two-step positive gain. It supplies a bounded decision about the proposed iteration mechanism, not a full Morrey resolution.

## Decision

Iterated exact conditional barycentring does converge, but convergence to a residual law is not convergence to zero. A finite set of null directions can fail on the ACTUAL first root law, even when the directions span R^3 and each is revisited infinitely often.

The first root nu_1 is a globally Lipschitz graph over d_1-perpendicular. Consequently it is fiber-injective along an open cone of directions around d_1. Three linearly independent null directions in that cone give an exact stationary schedule: the first d_1 step takes the original cosine law to nu_1, and all later steps do nothing. This is an actual continuous algebraic residual, not an atomic stand-in.

The successful u-axis second step lies outside that cone. It is preserved, not invalidated by this result. No obstruction to all null directions, unrestricted adaptive choices, or the actual second root's eventual collapse is claimed.

## 1. Governing actual laws

Use the unchanged source

    Z=(cos x,cos y,cos(x+y)),       mu=Law(Z),
    q(u,v,w)=uv+uw+vw,             E Z=0,
    Cov(mu)=I/2,                  E[uvw]=1/4.

Let

    d_1=(-1,2,2), d_2=(2,-1,2), d_3=(2,2,-1).

The first positive operation is nu_1=C_(d_1) mu, and the proved second operation is nu_2=C_(e_1) nu_1, where

    C_d Z=E[Z | P_d Z].

Their exact scalar variance losses s,r are strictly positive and satisfy

    Cov(nu_1)=I/2-s d_1 d_1^T,
    Cov(nu_2)=I/2-s d_1 d_1^T-r e_1 e_1^T,
    0<s<1/18,       r>0.

The second root still has the certified cubic moment

    26/125 < E_nu2[uvw] < 47/200.

The full formulas, stresses, and finite integral certificate remain in the separate positive-contraction packet.

## 2. Every exact schedule has a finite-activity limit

For a fixed sequence of valid conditional-barycenter operations, realize the iterates on the original probability space:

    Z_(n+1)=E[Z_n | P_(d_n) Z_n],
    F_n=sigma(Z_n).

Since projection is unchanged by its own contraction,

    F_(n+1)=sigma(P_(d_n) Z_n) subset F_n,
    Z_n=E[Z_0 | F_n].

Thus this is a reverse martingale. It converges almost surely and in L^2 to

    Z_infinity=E[Z_0 | intersection_n F_n].

All laws remain supported in the compact convex elliptope. The increments are orthogonal in L^2, so

    Cov(Z_0)-Cov(Z_infinity)
      =sum_n E[(Z_n-Z_(n+1))(Z_n-Z_(n+1))^T],
    E|Z_0|^2-E|Z_infinity|^2
      =sum_n E|Z_n-Z_(n+1)|^2.

Each summand is alpha_n d_n d_n^T with alpha_n>=0. The positive null stresses of the individual steps therefore sum to a finite positive null stress with source mu-nu_infinity. In the DivDiv S convention, its coefficient trace is half the dissipated coefficient energy; its physical trace is half the dissipated physical Frobenius energy. C=2S gives the (1/2)DivDiv C convention.

Collapse occurs precisely when the residual conditional mean vanishes, equivalently when the actual variance budget is exhausted. Merely having losses tend to zero is automatic for every schedule and proves nothing about residual energy. Nor does recurrence or fairness of a schedule establish exhaustion.

The schedule may depend deterministically on the current law. Arbitrarily selecting a different line direction for each individual point is not automatically the same valid conditional-barycenter operation.

## 3. An actual fiber-injective residual for a spanning finite set

The detailed proof is in ROOT_GRAPH_CONE_CHECK.md. Its key analytic points are:

- Write the first root support as Gamma={h+m(h)d_1 : h in Omega}, with Omega=P_(d_1)K compact and convex.
- At projected boundary points the two physical roots coalesce, but the symmetric formula for m extends analytically; the individual square-root singularities cancel.
- At the only exceptional interior projection h*=(4/9,1/9,1/9), the lower two roots collide at the Gram vertex (1,-1,-1). The direction matrix compressed to the vertex kernel has eigenvalues 1 and 7/3. A Schur-complement argument gives Lipschitz splitting, with an explicit local bound Lip(m)<=200 on B(h*,1/192).
- A finite compact cover, followed by subdivision of line segments in convex Omega, gives a finite global Lipschitz constant L>=1.

This is an analytic proof of finiteness. A numerical value for the full global L is not asserted.

Let e=d_1/3 and P=P_(d_1). Every support chord v satisfies

    |v dot e| <= 3L |Pv|.

Hence the open cone

    C={v nonzero : |v dot e|>3L|Pv|}

contains no support chord. Projection onto n-perpendicular is injective on Gamma for every n in C, so C_n nu_1=nu_1 exactly.

An explicit family of null directions is

    d(t)=(1-t,t^2-t,t),
    B(d(t))=(1,t) tensor (1,t),
    d(2)=d_1.

With epsilon=1/[16(1+L)], all three directions d(2),d(2+epsilon),d(2-epsilon) lie in C and

    det[d(2),d(2+epsilon),d(2-epsilon)]=-2epsilon^3 != 0.

A cyclic schedule beginning with d(2) therefore sends the ACTUAL mu to nu_1, then remains at nu_1 forever, despite using a spanning finite set fairly. This residual is nonzero for the exact reason

    E_nu1 |PZ|^2 = E_mu |PZ|^2 = 1.

This example also fails the appropriate positive covariance-cone budget, as expected: near-parallel direction dyads cannot exhaust the large transverse variance. It refutes the unqualified finite-spanning criterion, not a stronger theorem already imposing a viable covariance budget and persistent transverse mass.

## 4. Exact schedule obstructions for the actual two roots

The independent audit supplies full derivations and exact checks. The useful exclusions are:

1. Directions {d_1,e_1} preserve v-w pointwise. Since E(v-w)^2=1 and E q=0,

       E|Z|^2 >= 3/4

   on all their descendants, using

       |z|^2-(3/4)(v-w)^2-q(z)=(2u-v-w)^2/4.

2. The coordinate axes preserve uvw. Starting from nu_2, energy remains greater than 78/125, since |uvw|<=|z|^2/3 on the cube.

3. The cyclic directions d_1,d_2,d_3 are orthogonal and satisfy sum d_i d_i^T=9I. Covariance feasibility alone therefore looks promising. But their common direction-affine polynomial

       P_D(z)=product_i(d_i dot z)

   has expectation 3/4 on mu and nu_1. It prevents collapse under that cyclic triple.

4. Adding e_1 to the cyclic triple still cannot collapse the actual nu_2. In the orthonormal d_i/3 coordinates, cyclic losses are diagonal, while the already-spent e_1 loss creates a nonzero off-diagonal pattern that later e_1 losses only reinforce. The exact bound is

       E|Z|^2 >= 16r/9 > 0.

5. D5={e_1,e_2,e_3,d_1,d_2} has no common global C^2 direction-affine invariant beyond affine functions and q. Nevertheless every available dyad has nonpositive uv entry, so E[uv] cannot decrease after its positive value 2s is created. Consequently all descendants of nu_1 or nu_2 satisfy

       E|Z|^2 >= 9s/2 > 0.

   Indeed D5 cannot collapse mu under any schedule: either it has positive nonaxis activity and traps Euv>0, or it is effectively axis-only and preserves Euvw=1/4. Eliminating common smooth invariants is not sufficient.

6. For D6={all three axes, all three cyclic d_i}, the necessary and sufficient POSITIVE COVARIANCE-CONE condition from nu_2 is

       r <= 1/2-9s,
       equivalently E_nu2 |Z|^2 >= 1.

   This comes from solving for nonnegative future dyad coefficients. Its truth for the actual globally contracted nu_2 has not been established here. Even if it passes, it is not a variance-realization or convergence theorem.

No additional finite contraction was performed simply to accumulate activity. These checks concern the possibility of eventual exhaustion.

## 5. Unrestricted covariance does not obstruct the adaptive problem

Every PSD covariance C with J:C=0 is a sum of null rank-one dyads. Here is a short constructive proof.

Factor C=AA^T with r=rank C columns and put H=A^T J A. It is symmetric with trace zero. There exists a unit vector v with v^T H v=0, by the opposite-sign eigenvalues or H=0. Restrict to v-perpendicular; its trace is still zero. Induction produces an orthonormal basis v_1,...,v_r with v_i^T H v_i=0. Therefore

    C=sum_(i=1)^r (Av_i)(Av_i)^T,
    q(Av_i)=0.

At most three directions suffice for this algebraic decomposition in coefficient space. It does NOT follow that the law has positive conditional variance along those directions. A budget decomposition is not a mass coupling or a positive chord construction.

Accordingly, none of the finite-set covariance exclusions is an obstruction to the exact covariance of nu_2 under unrestricted adaptive directions.

## 6. Why compactness and moment matching do not close the remaining gap

For a unit null direction n define the actual dissipation

    V_n(nu)=E_nu |Z-E[Z | P_n Z]|^2.

It vanishes precisely when the law is a measurable graph over n-perpendicular. It is not lower semicontinuous under weak/W2 limits. Exact finite quadratures of the ORIGINAL cosine surface can be fiber-injective along any prescribed finite direction set, while converging to mu and matching arbitrarily many of its moments.

For completeness, choose an N-by-N uniform phase grid with N>=4 and generic offsets. For each distinct pair of grid indices, its difference does not identically lie in any fixed line as the two offsets vary; its nonzero coordinate differences have distinct phase Fourier supports. The bad offsets therefore form a proper analytic zero set. Avoiding the finite union makes every selected projection injective. Yet uniform grid averaging matches every coordinate polynomial of degree less than N exactly, and the laws converge in W2 to mu.

An explicit 16-atom example for D6, with rational coordinates and exactly matching all source moments through degree three, is verified in INDEPENDENT_CHECK.md and check_finite_directions.py.

These laws are NOT asserted reachable from mu or either actual root by positive contractions. Their role is narrower: they disprove a coercivity argument based only on compact support, moments, weak closeness, or an abstract covariance cone. Passing to a limit of small step losses also does not automatically prove that the limiting law is fiber-injective along every recurrent direction.

## 7. A geometric mass criterion that really would imply collapse

The following supplies a concrete target beyond “there exists another chord.” For a reachable law nu and a unit null direction n, disintegrate on h=P_nZ. Suppose a projected set Q has marginal mass at least m0>0 and, for almost every h in Q, two portions of the conditional fiber law:

- each have conditional probability at least eta>0;
- are separated by Euclidean distance at least ell>0.

The conditional independent-copy formula for variance gives

    V_n(nu) >= m0 eta^2 ell^2.

Thus positive transverse sheets with positive density really give positive activity, as in our second-step proof. But to establish eventual collapse one needs this mass/separation bound to persist at the relevant energy scale, not merely to be positive once.

Sufficient examples are:

- For every reachable nu, find a null direction with V_n(nu)>=c E_nu|Z|^2 for a common c>0. Choosing such a direction gives geometric energy decay.
- More weakly, for every energy threshold epsilon>0, prove a positive lower bound on the available dissipation over all ACTUALLY reachable laws with energy at least epsilon. A greedy or near-greedy schedule then cannot retain positive limiting energy.
- For a fixed cyclic schedule, prove the analogous bound on dissipation across each whole cycle.

In the two-sheet criterion, a common bound m0 eta^2 ell^2>=c E|Z|^2 suffices. For unrestricted directions one may choose a direction achieving, or within a fixed factor of, the supremum; no predetermined finite spanning set is required.

The first two positive operations prove such overlap locally, with strictly positive constants for those individual laws. They do not yet prove persistence of a uniform mass/separation bound through later contractions. Folding may weaken, conditional weights may concentrate, and weak limits need not preserve the necessary fiber structure. This is the precise missing convergence premise.

## Status

Preserved: exact S_1,S_2 with DivDiv(S_1+S_2)=mu-nu_2, strict finite activity, and the certified cubic reduction.

New: a rigorous actual-nu_1 stationary finite-direction construction; a reverse-martingale L2/finite-activity limit theorem; exact actual-law covariance and moment gates; and an explicit persistent-mass criterion sufficient for collapse.

Not established: a surviving-law class invariant ensuring that criterion, a positive stress from delta_0 to nu_2, or a full Morrey resolution. No localization policy, old map/SOS search, or numerical approximation was promoted to an exact gradient law.
