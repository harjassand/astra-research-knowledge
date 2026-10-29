# Known-center Phase I for the bounded-witness discovery SDP

This closes a complexity-interface correction to `EFFECTIVE_PORT.md`.
The bounded-witness premise supplies existence of a strict certificate,
but does NOT supply that feasible center. Therefore the known-center
Turing theorem is NOT invoked directly on the original discovery SDP.
The following ordinary Phase I construction acquires its actual premise.

Controlling primary: de Klerk–Vallentin1507.03549v2, Theorem1.1 (attributed
there to Grötschel–Lovász–Schrijver). Its input includes a KNOWN rational
feasible matrix X0 and known inner/outer Frobenius radii in the equality
affine space. It returns a rational feasible point at any positive
requested objective accuracy in polynomial time in the SDP size, data
bits and logarithmic radius/accuracy parameters. Here every such input
is constructed for a Phase I problem, not assumed for the discovery set.

## 1. Known equality point

Use the degree/boxes of `EFFECTIVE_PORT.md`: k=(D-3)/2, d=k+2,
N=ell-d, n_G=6*binom(ell+3,3), A=A_P, Gamma=3B64^ell.
Let x list all homogeneous P coefficients, nu and upper-triangular Q
entries. The exact coefficient equations have rational form Ex=f.
The desired inequalities are

    Q-(m/8)D_ell >=0,
    b_i+x_i>=0, b_i-x_i>=0 for every coordinate i,

where b_i is2A for primitive coefficients,2Gamma for Gram entries,
and Lambda+2 for nu. These coordinate boxes also bound all possible
unknown normalizers; nothing is supplied by an optimizer.

There is an explicit rational equality point x0: set P=0 and nu=0, then
represent the known polynomial

    T^(N+k+1) D_0 F

by a symmetric Gram Q0 in the full basis A^alpha h_j, |alpha|=ell.
Every monomial of A-degree2ell and h-degree2 splits into two such basis
monomials. Assign its coefficient to a diagonal Gram entry, or equally to
the two symmetric off-diagonal entries. This is the same elementary exact
coefficient operation used in the original certificate qualifier. Q0 may
be indefinite; it is NOT mislabelled a feasible point. Acquisition is
finite rational monomial arithmetic, polynomial in the finite map/output
size. No alpha, min-eigenvalue, gap or convex feasibility oracle is needed.

## 2. Artificial slack with a KNOWN strict center

Introduce one real scalar t and replace all desired inequalities by

    S(x,t)=Q-(m/8)D_ell+t I >=0,
    b_i+x_i+t>=0, b_i-x_i+t>=0,
    T0+t>=0, T0-t>=0.                              (P1)

The same exact equalities Ex=f remain. Define computable rational numbers

    R_G=max_j sum_l |(Q0-(m/8)D_ell)_(jl)|,
    R_box=max_i max(0,|x0_i|-b_i),
    t0=2+R_G+R_box, T0=2t0+2.                      (P2)

At (x0,t0), Gershgorin gives S>=2I. Every scalar block in(P1) is>=2.
Thus the block-diagonal matrix

    X0=diag(S(x0,t0), {b_i+x0_i+t0,b_i-x0_i+t0}_i,
            T0+t0,T0-t0)

is an EXPLICIT rational positive-definite feasible matrix, with X0>=2I.
It is acquired without knowing the original bounded witness.

## 3. Standard SDP form and radii

Let n_x be the length of x and n_S=n_G+2n_x+2. The affine image

    X(x,t)=diag(S(x,t),{b_i+x_i+t,b_i-x_i+t}_i,T0+t,T0-t)

subject to Ex=f is a rational affine subspace of symmetric n_S matrices.
It is specified by exact rational linear equations: off-block entries are
zero and the displayed blocks have their affine relations. The map is
injective, since the difference of each paired scalar block recovers2x_i
and the last pair recovers2t. Its image/range equations can be computed by
exact rational elimination in polynomial bit cost. The objective t is a
fixed linear trace functional of the last two scalar blocks.

The intersection of this affine image with X>=0 is exactly(P1). The known
X0 has a Frobenius inner ball of radius r0=1/2 in this affine space because
its smallest eigenvalue is>=2; no unknown-center theorem is used here.

For a known outer radius, put bmax=max_i b_i and

    C0=2bmax+2T0+(m/8)4^ell+1.

For EVERY Phase I feasible point, |t|<=T0, and the paired scalar
inequalities imply |x_i|<=b_i+T0. Each matrix entry of X is bounded byC0:
the diagonal of S additionally pays(m/8)D_ell, whose entries are<=
(m/8)4^ell. Hence ||X||F<=n_S C0. X0 is feasible as well, so the known
outer radius about X0 can be chosen

    R0=2n_S C0+1.                                  (P3)

All numbers have polynomial bit size in the finite map size/ell and the
given rational data. In particular no logarithm of an unknown center's
distance appears in(P2),(P3).

## 4. A known accuracy forces a usable certificate

The bounded-witness construction, whose center is unknown, proves there
EXISTS x* with

    Q* >=(m/4)D_ell,
    |P*_coefficient|<=A, |Q*ij|<=Gamma,
    |nu*|<=Lambda+1.

Set the known positive rational

    s=min(m/16,A/2,Gamma/2,1/2).                    (P4)

Then (x*,-s) is Phase I feasible: its PSD slack is at least(m/16)I;
the doubled boxes retain positive slack, and |s|<=1/2<T0. Therefore
the optimum of min t over(P1) is at most-s.

Now apply the PRIMARY known-center theorem to THIS Phase I SDP, with its
acquired X0,r0,R0 and objective accuracy s/2. It returns an exact rational
Phase I feasible matrix with t<=-s/2<0. Recover its rational x by the
paired-block differences. Then

    Q-(m/8)D_ell >= -t I >0,

and the original, unrelaxed boxes hold. The coefficient equalities are
exact as part of the rational affine image. Consequently a valid strict
rational angular certificate has actually been acquired. Final coefficient
identity/PSD verification is still performed; a particular floating solver
is not the algorithm guaranteed by this complexity theorem.

The weighted floor gives a direct full-domain strong Jensen margin
m/[576(1+|nu_out|)] by the already paid bound
|D_nu |A|^4|<=24(1+|nu|)T|h|² and quartic Bregman inequality. No largest
multinomial factor in ell is lost.

There is also a sound finite FAILURE interpretation. On an arbitrary input,
if the exact near-optimal feasible output has t_out>=0, the theorem's
objective guarantee implies val>=t_out-s/2>=-s/2>-s. This rigorously excludes
EVERY witness satisfying the DECLARED eta,W,Lambda bounds, because such a
witness would force val<=-s. Thus the operation always returns either an
actual QC certificate or a qualified rejection of that bounded witness
contract. A successful certificate need not itself have C2 norm<=W, so
this is not exact membership decision of the bounded class. Rejection
does not refute QC, a weaker-margin or larger-norm witness, or the entire
unbounded heat-form class. No unqualified finite-SDP-failure inference is
made.

## 5. Cost and scope

This gives a polynomial Turing acquisition guarantee in the finite Phase I
size/data bits and log(R0/r0),log(1/s), under the explicit bounded-witness
promise of `EFFECTIVE_PORT.md`. The dimensions there are polynomial in the
NUMERICAL W,eta^-1,Lambda,H_F at fixed physical dimension, with a very
large exponent. This is not a practical generic runtime, a bit-polynomial
bound in those magnitudes, a bound obtained from F alone, or QC-completeness.

Phase I and the known-center complexity theorem are established ordinary
tools; no generic optimization novelty is claimed. The acquired operation
is the full bound-and-search composition for this smooth heat-form class,
including the center that a direct invocation would have left unpaid.
No source/optimizer fixture or new physical operation was run here. The
generic Phase I/Turing solver is specified and proved, not implemented
end-to-end; actual finite execution remains the separate frozen input
certificate and its independent exact consumers.
