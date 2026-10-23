# Full linear-skew graph criterion for homogeneous K pullbacks

Root derivation, 22 October 2026, extending WS03's metric graph lemma.
Independent audits requested. The algebra below characterizes this
minorant architecture; it does not assert that the architecture covers
all quasiconvex integrands or settles Morrey.

Use physical conformal coordinates det A=|z|^2-|w|^2. Let

    u=w+Cz, F(A)=u^T W u+D(z), W>=0,
    h(A)=k^T u+v^T z,
    lambda=|k|^2-|C^T k+v|^2.

The vectors k,v are arbitrary. In particular h need NOT vanish on the
graph u=0. The previous v=0 restriction can lose valid certificates.
For the physical coefficient matrix H of h, put

    Lh=[[2H12,2H22],[-2H11,-2H21]].

Then det Lh=4det H=-lambda, skew(Lh A)=h(A), and

    Q(A)=-det Sym(Lh A)=h(A)^2+lambda*det A.

Choose L=+/-Lh, and put pi(z)=-tr(L A_graph(z)), where A_graph(z)
is the physical matrix with w=-Cz. Let K be the globally QC generator
that is zero on Sym B<=0 and equals -det Sym B elsewhere.

## Exact global test, including singular blocks

For lambda!=0, the following are equivalent:

    F(A)>=K(LA) for every physical A;

    (i) F(A)>=Q(A) for every A, and
    (ii) D(z)>=0 whenever pi(z)>=0.                 (1)

Condition (i) in turn is exactly the following PSD/range/profile test:

    M=W-k k^T+lambda I >=0,
    N=k v^T+lambda C,  Range(N) subset Range(M),
    D(z)+z^T[lambda(C^T C-I)-v v^T-N^T M^dagger N]z>=0
                                                    for every z. (2)

Here M^dagger is the Moore--Penrose inverse. To verify this, expand

    F-Q=u^T M u-2u^T Nz
                  +D(z)+z^T[lambda(C^T C-I)-v v^T]z,

then minimize over the free u. If the range condition fails, motion
along a kernel direction makes this expression arbitrarily negative.
If it holds, completing the PSD square gives exactly (2). This proof
does not require M to be invertible.

Necessity in (1) is immediate: K>=Q everywhere, and at a graph point
with pi>=0 the symmetric trace is nonpositive, so K(L A_graph)>=0.

For sufficiency, suppose F(A)<0. Since W>=0, the whole path

    A_t: z fixed, u_t=t u, 0<=t<=1

obeys F(A_t)=D(z)+t^2 u^T W u<=F(A)<0. By (i), Q(A_t)<0
all along it. Therefore Sym(LA_t) is definite throughout and cannot
switch between its two components. At t=0, D(z)<0 and (ii) force
pi(z)<0, so the trace is positive: Sym(LA_0) is positive definite.
The entire path is thus in K's active component. This proves that
F cannot be negative in the inactive component. There F>=0=K;
on the active branch (i) supplies F>=Q=K.

For lambda=0, L is singular and det Sym(LA)=-h(A)^2. It follows
directly that K(LA)=h(A)^2=Q(A) for every A: on its inactive
component both are zero. Thus (2) alone, with lambda=0, is exact;
the halfspace condition is then redundant.

## Contact and all transverse backgrounds

Suppose (1) holds, D(zB)=0 and pi(zB)>=0. At the graph point B0,
F(B0)=0>=Q(B0), so Sym(LB0) has nonnegative determinant and
nonpositive trace; hence it is negative semidefinite. Thus the
global minorant touches: F(B0)=K(LB0)=0. This also handles pi=0.

There is an explicit touching certificate for every background B
with this same zB and arbitrary uB. Let S have z(S)=0,w(S)=uB.
The exact identity

    F(A)=F(A-S)+2uB^T W u(A)-uB^T W uB

gives the globally touching QC minorant

    K(L(A-S))+2uB^T W u(A)-uB^T W uB.

No arbitrary balanced law is substituted for an actual gradient.
Only the separately proved global QC of K is needed for this last
consequence. The criterion allows any C, either sign of nonzero
lambda, arbitrary continuous D for which the expressions are finite,
and an arbitrary PSD transverse metric. It covers all choices of the
physical left matrix L, since skew(LA) is an arbitrary linear form in
the four physical entries. It does not cover sums/maxima of several
such primitives, affine shifts inside the global quadratic comparison,
or arbitrary additional QC mechanisms.
