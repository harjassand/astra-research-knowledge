# A finite convex operation despite every polynomial selector failing

Root construction applying established truncated-moment/SOS duality, not a
new general optimization algorithm. This uses the accepted rational-selector
F, not the newer non-PC Hopf target. External priority is UNKNOWN.

## Exact certificate interface

For EACH FIXED nonzero A, the accepted R180 identity makes

    F(A+X)-F(A)-DF(A):X-k(A)detX

SOS of degree at most four in X: division by |A|^4 divides by a constant.
No polynomial dependence of k on A is needed. Moreover the remainder
minus delta[|A|²|X|²+|X|^4] is SOS for delta=1/2400000. Use R180>=I/400000,
S3(A)>=|A|^6/6, S2(A)>=|A|^4/2 and
S2(X)-|X|^4/2=(1/2)sum X_i^4. All A quantities here are constants;
the remaining nonnegative differences are explicit SOS in X. Taking the
highest X degree also proves F-|X|^4/1600000 is SOS. At A=0 the support
is F itself, also SOS. This is a stronger interface than nonnegativity.

## Fixed finite SDP

Let y be the70 moments through degree4 in4 variables, L_y their linear
functional, and M2(y) the15x15 moment matrix indexed by monomials through
degree2. Define

    G_epsilon(B,s)=min_y L_y[F(A)+epsilon|A|²]
    s.t. M2(y)>=0, y0=1, L_y A=B, L_y detA=s.          (1)

Its value is convex in the five right-hand-side parameters. Feasibility
everywhere follows from the two actual atoms B+Y,B-Y with detY=s-detB.
Coercive SOS F-delta4|A|^4, delta4=1/1600000, bounds L_y|A|^4 on an
objective sublevel set. Moment PSD Cauchy-Schwarz then bounds all70
moments, so closed sublevel sets are compact and the minimum is attained.

At (A,detA) the Dirac moment gives upper bound W_epsilon(A). The fixed-A
SOS support is dual-feasible and gives the same lower bound. Thus

    G_epsilon(A,detA)=F(A)+epsilon|A|²

globally, including zero. Weak duality suffices, with no solver-success
premise. Primal Slater points also exist: use a full-support Gaussian of
mean B and positive covariance satisfying Cov(a,d)-Cov(b,c)=s-detB.
The strict SOS remainder makes the graph optimizer unique: equality
forces L|X|^4=0; PSD Cauchy-Schwarz forces every centered moment through
degree4 to match the Dirac point.

This is a fixed semidefinite operation, escaping scalar-polynomial-lift
failure without invoking an infinite oracle. Numerical solver output is
not an exact value/precision certificate. The following exact off-graph
slice supplies a nontrivial operational control.

## Exact off-graph slice

The literal old F has Hopf form

    F=p0 x²+Ky y²+L qx+c0 q²,
    Ky=p0/2+(p2+p3)/4>0, c0=2p0+p2,

with positive-definite(x,q) quadratic matrix. For every feasible moment,
PSD implies Jensen for this positive quadratic in x,y,q, and

    L_y T>=sqrt[(L_y x)²+(L_y y)²+4s²].

Indeed T-n·(x,y,2q) is a PSD quadratic whenever |n|<=1: the three real
symmetric Hopf matrices square to I and pairwise anticommute. Apply the
positive moment functional and maximize over n. At B=0 these lower bounds
are jointly attained: every real Hopf triple(x,y,q) is realized by a
physical A, and atoms +/-A have zero mean with that constant triple.
Minimizing over y gives y=0. Therefore exactly

    G_epsilon(0,s)=min_x[p0x²+Lsx+c0s²
                                      +epsilon sqrt(x²+4s²)].       (2)

For epsilon0 this equals[c0-L²/(4p0)]s². For epsilon>0,s>0, its unique x
is in[-Ls/(2p0),0] and solves

    2p0x+Ls+epsilon x/sqrt(x²+4s²)=0.

slice_certificate.py uses rational derivative intervals, integer square
roots and bisection to enclose four nonzero off-graph values independently
of any SDP solver. No physical hardware is acquired.

## Smoothness and ordinary comparison

This maximal lift within the SOS-dual family differs from the smaller smooth-near-graph lift
conv(h). At B0, moment PSD yields LT>=2|s| and L|A|^4>=(LT)², hence

    G_epsilon(0,s)>=2epsilon|s|+4delta4*s².

It equals0 at s0, so for positive epsilon it cannot be differentiable in
the determinant direction there. In fact it is nondifferentiable at EVERY
graph point. The strong SOS support at A remains SOS after replacing k(A)
by k(A)+zeta whenever

    |zeta|<=2(epsilon+delta|A|²),

because (epsilon+delta|A|²)|X|²-zeta detX is a PSD quadratic. These give
distinct dual supporting subgradients
(DW_epsilon(A)-(k+zeta)cofA,k+zeta) at the same graph value. For epsilon0
the same conclusion holds at every nonzero A. Thus unique primal Dirac
moments do NOT imply differentiability of the value function. A finite
global convex evaluator is acquired; a smooth entropy interface is not.

A computable strongly convex variant uses
H=F-kappa det²+(epsilon-kappa)T, 0<kappa<min(delta/4,epsilon/2). Its
support remainder loses kappa(cofA:X+detX)². The SOS bound

    (cofA:X+detX)²<=2|A|²|X|²+|X|^4/2

preserves strict SOS support. The finite moment value for H plus
kappa|(B,s)|² therefore matches W_epsilon and is globally2kappa-strongly
convex; nonsmoothness remains possible. Generic moment duality retains
its prior credit. No advantage over an equally informed moment/envelope
method, new non-PC target PC/QC, physical implementation or100/100 result
is claimed.

## Established machinery and source boundary

The generic moment/SOS/semidefinite approach is prior work, including
[Lasserre (2001)](https://epubs.siam.org/doi/abs/10.1137/S1052623400366802)
and [Parrilo (2003)](https://www.mit.edu/~parrilo/pubs/files/SDPrelaxations.pdf).
The primary abstracts/introduction were retrieved on28 October2026; their
generic method, not a target-specific exactness theorem, is credited here.
The finite target exactness is proved directly above from the accepted
certificate. The value need not equal the largest Busemann representative
away from the graph. The distinction between largest representatives and
graph-touching support families is established, for example
[Bevan (2008)](https://arxiv.org/abs/0809.3921). No theorem from an unread
portion of these sources is needed for the argument above.
