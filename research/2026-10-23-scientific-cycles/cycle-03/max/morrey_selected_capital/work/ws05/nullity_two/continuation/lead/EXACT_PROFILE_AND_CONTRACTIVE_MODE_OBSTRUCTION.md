# Exact angular K profile and a stationary four-cut obstruction

This continuation does not modify the frozen previous-round package.
It answers the next architecture question negatively: not every member
of the stationary symmetric four-cut extreme family admits a homogeneous
contractive-mode K minorant of the specified graph type. It does not
disprove quasiconvexity or exclude more general K/cap certificates.

## 1. The stationary family before imposing a K certificate

Use physical coordinates z=(x,y)=((a+d)/2,(c-b)/2),
w=((a-d)/2,(c+b)/2), so det A=|z|^2-|w|^2. The general symmetric
four-cut construction has

C=[[c0,d0],[d0,c0]], alpha=c0+d0>1, 0<=beta=c0-d0<1,
u=w+Cz,
Phi=gamma(px+qy)_+^2+gamma(qx+py)_+^2+d(x_-^2+y_-^2),
M=gamma[[p^2+q^2,2pq],[2pq,p^2+q^2]],
D=Phi-z^T M z, F=|u|^2+D.

Here p>q>0, k>1, k>=p/q, lambda0>0, s0=1+lambda0, a0>0,
d=(k^2-1)a0, and

lambda0(C^2/s0-I)-M=a0[[1,k],[k,1]].                 (1)

This identity alone gives the local R1C completions from the previous
round. The stationary rank-three kernel condition is

(k-1)^2 alpha^2+(k+1)^2 beta^2=2(1+k^2)s0^2.        (2)

It makes the two rank-three kernel directions determinant-null. The
following analysis does not assume the sufficient uniform-mu K
inequalities of the previously proved relatively open QC family.

## 2. Exact finite angular profile, with one K parameter

Set e=(p-q)/(p+q), mplus=gamma(p+q)^2, and
mminus=e^2 mplus. Use orthonormal coordinates
P=(x+y)/sqrt(2), T=(x-y)/sqrt(2). Then

D(P,T)=d/2[(P+T)_-^2+(P-T)_-^2]
       -mplus/2[(P+eT)_-^2+(P-eT)_-^2].           (3)

For a canonical contractive-mode K choice put h=tau V, where
V=(u1-u2)/sqrt(2), and

kappa=tau^2(1-beta^2),
A=kappa(alpha^2-1-kappa)/(1+kappa),
B=kappa(1-beta^2)/(1-tau^2 beta^2).                 (4)

The exact global profile criterion is

D(P,T)+A P^2-B T^2>=0 for all (P,T).               (5)

It is equivalent to this particular homogeneous K being a global
minorant, with the inactive component chosen to contain the positive
graph quadrant, under D>=0 on P>=0. The latter sign condition follows
from (1), beta<1, and k>1 exactly as in the frozen family proof.
The necessary free-u condition is 1-tau^2 beta^2>0. At equality and
beta>0 the nonzero u/z cross term prevents a global inequality; above
it the free-u quadratic is negative. These boundary cases are not
omitted by the parameterization.

Equation (3) is invariant under T -> -T. Normalize |P|=1 and let
t=|T/P|>=0. The complete angular table for (5) is:

P=+1, 0<=t<=1:
  A-B t^2.
P=+1, 1<=t<=1/e:
  (d/2-B)t^2-d t+(A+d/2).
P=+1, t>=1/e:
  c t^2+(mplus e-d)t+z0.
P=-1, 0<=t<=1:
  (d-mminus-B)t^2+(A+d-mplus).
P=-1, 1<=t<=1/e:
  (d/2-mminus-B)t^2+d t+(A+d/2-mplus).
P=-1, t>=1/e:
  c t^2+(d-mplus e)t+z0,

where c=(d-mminus)/2-B and z0=A+(d-mplus)/2.
The remaining ray P=0 is exactly c>=0.

This is an exact one-variable feasibility test in kappa. Every entry
is a scalar quadratic on its displayed interval; no angular grid or
uniform radial bound is used. On a bounded interval [L,H], positivity
of a quadratic f(t)=ct^2+bt+a is equivalent to both endpoint signs
and, if c>0 and -b/(2c) lies strictly inside the interval, 4ca-b^2>=0.
For the two infinite intervals one only needs

c t^2-|d-mplus e| t+z0>=0 for t>=1/e.               (6)

If c=0 this requires d=mplus e and z0>=0. If c>0, check the endpoint
when |d-mplus e|/(2c)<=1/e, and otherwise check
4c z0-(d-mplus e)^2>=0. If c<0 it fails. Thus the feasibility is
finite and exact, with all coefficients rational in kappa and the
specified parameters.

For admissible (1), d>mminus. Consequently the first negative-P
interval requires A>=mplus-d once c>=0; the first positive-P
interval requires A>=B. The positive-P middle interval has the sole
possible extra interior minimum at t=d/(d-2B); if it lies in
(1,1/e), its test reduces to A>=dB/(d-2B). The negative-P middle
interval has no interior minimum: it is either increasing or concave.
The table remains the primary exact test, avoiding boundary ambiguity.

## 3. A fully rational stationary member outside this K architecture

Choose

k=2, p=4, q=3, lambda0=1/10, s0=11/10,
C=[[286/205,33/82],[33/82,286/205]],
alpha=737/410, beta=407/410,
gamma=6829/2185300,
a0=7398/546325,
d=22194/546325.

All parameters are positive with the required strict inequalities.
Identity (1) holds exactly, as does

alpha^2+9 beta^2=10 s0^2.                          (7)

Indeed C/s0=[[52/41,15/41],[15/41,52/41]], so the two boundary
kernel vectors are

r2=(1,-2,-22/41,89/41),
r3=(2,-1,-89/41,22/41),

and both have determinant zero. Their w vectors are independent and
have nonzero dot product 3916/1681. Thus the same direct face proof
as in the frozen stationary member gives rank (2,3,3), unique
multipliers (0,1/10,1/10), and an extreme ray modulo determinant in
this fixed four-cut dictionary. This is a member of the stationary
extreme family, not merely a general R1C perturbation.

The contractive free-u condition requires

0<kappa<(1-beta^2)/beta^2=2451/165649.              (8)

The exact angular test at P=-1,T=0 requires

A>=mplus-d=49169/437060.                          (9)

But for every kappa in (8),

A<kappa(alpha^2-1)
 <[(1-beta^2)/beta^2](alpha^2-1)
 =24845787/752583700.                            (10)

The required lower bound in (9) exceeds the upper bound in (10) by

388826417/4891794050>0.                           (11)

Therefore no admissible tau works. This obstruction uses the exact
negative-diagonal angular cone, so removing the earlier uniform-mu
estimate cannot repair it. tau=0 would give the zero/nonnegative
degenerate atom and cannot minorize this F, which takes negative
values. At or above the endpoint (8), the free-u condition fails as
described above. The opposite inactive orientation does not change
the necessary inequality F>=Q and cannot repair the obstruction.

Ordinary nonpolyconvexity also persists for this exact new member.
At a positive-quadrant graph B, F=DF=0 and the cell14 multiplier is
uniquely zero. At the graph ray z=(-1,-1), one has
F=2(d-mplus)=-49169/218530<0. This proves ordinary non-PC by the
same support argument. It does not prove a quasiconvexity violation.

## 4. Extension to arbitrary graph-vanishing homogeneous single K

The obstruction is not limited to choosing h exactly along V. Let
h=vplus U+vminus V be any linear form of the two u coordinates and
suppose its active physical K quadratic is Q=h^2+kappa det with

kappa=(1-beta^2)vminus^2-(alpha^2-1)vplus^2>0.

Since K>=Q everywhere, a global F>=K would imply F>=Q. Its free-u
quadratic matrix is (1+kappa)I-vv^T, which must be PSD. Consequently

|v|^2<=1+kappa,
kappa<=(1-beta^2)|v|^2<=(1-beta^2)(1+kappa),

so kappa<=(1-beta^2)/beta^2. At the negative expanding graph ray
u=0,P=-1,T=0, the necessary comparison is

kappa(alpha^2-1)>=mplus-d.

It is contradicted by the same strict rational bound (11), even if
the upper endpoint is allowed. Adding any nonnegative PSD quadratic
in u to the proposed minorant only reduces its available free-u
budget and leaves this contradiction intact.

This stronger statement still does not exclude h with additional z
dependence, translated K atoms, arbitrary ordinary-PC residuals,
several K atoms, other QC generators, or a QC proof by another method.
The restricted obstruction leaves quasiconvexity undecided. A subsequent
universal tilted-skew certificate, proved in the companion
UNIVERSAL_TILTED_K_FAMILY_QC.md, proves this member QC using a nonzero
cut-coordinate term. Thus its current internal status is QC conditional
on the inherited K theorem. Full Morrey remains NOT_ACHIEVED.
