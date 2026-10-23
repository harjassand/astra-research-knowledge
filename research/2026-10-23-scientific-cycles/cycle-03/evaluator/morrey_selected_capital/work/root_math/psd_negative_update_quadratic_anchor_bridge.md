# Quadratic anchor gluing with an arbitrary PSD negative update

Root derivation, 22 October 2026. Strengthens the arbitrary-rank anchor
lemma by replacing u^2 with an arbitrary positive-semidefinite quadratic
S. WS04 independently supplied/reconstructed the decisive block-inertia
argument. Full independent audits pending. Conditional on the reconstructed
global quasiconvexity theorem for K. This is not full Morrey.

Conformal coordinates: det X=X^T JX, J=diag(1,1,-1,-1). Suppose

    H0=lambda0 det+P, P>=0,
    Hi=H0+v^2-S, S>=0,
    Pi=Hi-lambdai det=P-delta J+v^2-S>=0,
    delta=lambdai-lambda0.

No rank or independence conditions are imposed on P,S,Pi or v. Let F be
continuous with F>=H0 globally and F>=Hi on {v<=0}. At a background B
where F(B)=Hi(B), v(B)<0 and Hi(B)>H0(B), a global QC minorant touches F.

Write G=P-delta J. Since G+v^2=Pi+S>=0, G has at most one negative
eigenvalue. If G>=0, the partial maximum of G and Pi on {v<=0}, equal
to G on {v>=0}, is convex: it is a local maximum of convex quadratics
away from v=0; at v=0,S(X)>0 it equals G near the point; at v=0,S(X)=0
the two gradients agree because SX=0. Along any affine line, switching
derivative jumps are upwards or zero. Adding lambdai det gives the
desired polyconvex minorant. This includes delta=0.

Assume now G has exactly one negative eigenvalue. Then delta!=0. The
spectral argument in arbitrary_rank_quadratic_anchor_k_bridge.md provides
h with hh^T<=P, h^T Jh=delta. Explicitly factor P=LL^T, take an extremal
eigenvector of L^T JL of the sign of delta, and scale it to Rayleigh
value delta. Such an eigenvalue has magnitude at least |delta|, since
otherwise G would retain the two negative eigenvalues of -delta J.
Put R=P-hh^T>=0 and QK=h^2-delta J=G-R.

This QK is the active quadratic of K(Lh X) for an invertible physical
left matrix Lh: if h(A)=H11a+H12b+H21c+H22d, take
Lh=[[2H12,2H22],[-2H11,-2H21]]. Then det Lh=delta and
skew(Lh A)=h(A). The sign of Lh chooses the inactive component.

If r lies in ker G, positivity of G+v^2 forces v(r)=0: otherwise add
a multiple of r to a G-negative vector to cancel v, a contradiction.
Now r^T Pi r=-r^T S r>=0 implies Sr=0 and Pi r=0. Thus all subsequent
forms descend to the orthogonal quotient of ker G. On this quotient G
has inertia (n-1 positive,1 negative), n=3 or4. Use Gdagger for its
quotient inverse, extended by zero.

## The matrix inequality replacing the rank-one negative update

Factor S=UU^T with q columns (q=0 is allowed). Define

    a=v^T Gdagger v, b=U^T Gdagger v,
    A0=-1-a, D0=I_q-U^T Gdagger U.

Consider the symmetric block matrix

    Bbig=[[G, U, v], [U^T,I_q,0], [v^T,0,-1]].

Schur complement at diag(I_q,-1) is Pi; consequently if rank Pi=r,
the inertia of Bbig is (q+r positive,1 negative,n-r zero). The Schur
complement at G is

    [[D0,-b],[-b^T,A0]].

Since G already contributes exactly one negative direction, this
complement has NO negative eigenvalue. Flipping its last row/column
and permuting therefore gives

    M=[[A0,b^T],[b,D0]]>=0.                         (1)

This works even when v belongs to range U. In particular A0>=0.
Direct expansion gives

    E=Pi-Pi Gdagger Pi=[v,U] M [v,U]^T>=0.

Let C=Gdagger Pi B and eB=B^T E B. Then GC=Pi B, and

    v(C)=-A0 v(B)-b^T U^T B,
    v(C)^2<=A0 eB.                                (2)

The latter is the first-row Cauchy inequality for the PSD matrix (1),
so includes A0=0 and all dependent factors. This is also derivable for
A0>0 by Sherman--Morrison from 0<=Pi<=G+v^2, but no inverse of that
possibly singular PSD upper bound is needed here.

## The translated K minorant

The set {G<0} has two opposite connected components, distinguished by
the sign of v, since a<=-1. They lie in the two opposite components
of {QK<0}, since QK=G-R. Choose the inactive K component to contain
the G-negative component v<0. Define

    T_B(X)=lambdai det X+2(Pi B).X-B^T Pi B,
    Psi_B(X)=T_B(X)+KQ(X-C).

The exact identities are

    H0(X)-T_B(X)-QK(X-C)=R(X-C)+eB>=0,
    H0(X)-T_B(X)=G(X-C)+eB.                        (3)

On the active branch, (3) gives Psi_B<=H0<=F. On the inactive branch,
if H0>=T_B we are done. Otherwise Y=X-C has G(Y)<-eB. Lorentz
Cauchy with v^T Gdagger v=-(A0+1) gives

    |v(Y)|^2> (A0+1)eB >= A0eB >= |v(C)|^2.

Thus v(X) has the same sign as v(Y), which is negative in the chosen
inactive component. Hence F(X)>=Hi(X)>=T_B(X), because Pi>=0, and
KQ(Y)=0. This proves Psi_B<=F everywhere.

At X=B, H0(B)-T_B(B)=H0(B)-Hi(B)<0. The same sign argument places
B-C strictly in the inactive component, so Psi_B(B)=Hi(B)=F(B).
Psi_B is QC: it is determinant plus affine plus a translated GL pullback
of K. This proves the gluing lemma.

## Minimal-positive-circuit application

For F=Q+Phi, Phi=sum_i (vi.X)_-^2, assume one has found S>=0 such
that S<=Phi globally and H*=Q+S is a rank-one-convex quadratic. Then
use H0=H*. Each one-active cell has Hi=Q+(vi.X)^2; its R1C completion
exists because F is globally R1C and agrees with Hi on an open cell.
Moreover F>=Hi wherever vi.X<=0, and Hi-H*=vi^2-S. The gluing lemma
therefore proves QC at every one-active-cell background (equal contact
with H* is immediate).

For a minimal positive circuit of m=r+1 normals spanning r dimensions,
the fixed-test Jensen gap is concave on any line preserving all inactive
cut values in a cell. With at least two active cuts, such a nonzero line
exists; the positive circuit forces its active slopes to have both signs,
so both cell endpoints are finite and reduce the active count. Repeated
concavity extends the one-active-cell inequality to every background;
walls follow by continuity. This is valid for r<=4 in the 2x2 setting.

The universal D-optimal construction of such S is proved separately by
WS05 in MINIMAL_POSITIVE_CIRCUIT_QUADRATIC_ANCHOR_THEOREM.md. Combining
these two proofs would establish QC for every globally R1C quadratic
plus one central minimal positive circuit of squared negative hinges,
with arbitrary common quadratic and all four matrix entries permitted.
It does not establish a decomposition of arbitrary nonminimal networks.
