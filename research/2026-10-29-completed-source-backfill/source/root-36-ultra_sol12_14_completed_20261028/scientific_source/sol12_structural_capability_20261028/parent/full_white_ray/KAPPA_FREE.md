# A condition-number-free entire-white receiver

This root construction strengthens PROOF.md; the earlier kappa³ bound and
its independent acceptance remain valid. Use the same A0,H,r,ell and
ell0=min(ell,8/9)>0, but require ONLY C>=mI>0. Set

    a0=m ell0²/(2^18 r³), eps_max=m ell0²/(2^22 r³)=a0/16.

For EVERY0<eps<=eps_max, X=A0+epsH has

    Delta(X+aI)>=(epsell+8ra)/2, 0<=a<=a0,
    Delta(X+aI)>=(3/35)ra m²/(a+m)², a>=a0.           (1)

There is no upper C eigenvalue/condition-number input. The inherited
positive common-bath identity therefore applies for arbitrary PSD U,V.
The complete original-source derivative proof follows; no log C filter,
pointwise entropy whitening or unproved sign of a general mixture is used.

## Small noise

Normalize K=epsH+aI, w=eps+9ra, ell'=(epsell+8ra)/w>=ell0.
For a<=a0, w<10ra0<=mell0²/(2^14r²). Thus the reviewed sol11 general-ray
theorem on the actual K/w proves the first line(1). This step covers a0.

## Keep the actual weighted logs for the finite large-noise increment

Let P=P_Omega/3 tensor I, Q=I-P, R=P_antisym tensor I and S=I-R.
Write h0(a)=Delta(A0+aI). The input and E entropy increments are bounded
below by their tangent at aI+A0. The N increment is bounded above using
NH<=I and operator-log monotonicity at aI+NA0+epsI. Constant derivative
terms cancel. The exact lower bound is

    Delta(A0+epsH+aI)-h0(a)>=eps Tr[H L_eps(a,C)],
    L_eps=log(A0+aI)+E log(EA0+aI)-2N log(NA0+(a+eps)I).

All logs here are of faithful finite matrices for a>0. N is self-adjoint
and commutes with logical C functions. Since N*(R)=(I+3P)/4, N*(S)=3Q/4,
at eps0 the P,Q scalar coefficients at a logical eigenvalue c are

    LP=log[(a+3c)(a+c/3)/(a+c)²]>=0,
    LQ=log[(a+c/3)/sqrt(a(a+c))].                     (2)

The first numerator exceeds its denominator by(4/3)ac. Put x=c/a.
The second coefficient is nonnegative for x>=3. For all x>=0,

    log(1+x/3)-(1/2)log(1+x)>=-x/6,

because the derivative of the left side plus x/6 equals
x(x+7)/[6(x+3)(x+1)]>=0 and its value at0 is zero.

Therefore a negative first-order increment can come only from c<3a,
and is at most eps/(6a)sum_(c_j<3a)c_j w_j, where
w_j=Tr[Q(I_AB tensor|j><j|)H] satisfies0<=w_j<=1. Since c_j>=m,
the charge is at most eps/(6am)sum_(c_j<3a)c_j².

The baseline function g in PROOF.md obeys c g(a/c)>=(6/35)ac²/(a+c)².
When c<3a this is at least3c²/(280a). Consequently the entire first-order
negative part is at most(140/9)(eps/m)h0(a).

At finite eps, the additional negative P coefficient has magnitude
2log[1+eps/(a+c)]<=2eps/a. The Q correction is
(1/2)log[1+eps/(a+c)]+(3/2)log[1+eps/a]<=2eps/a.
Since TrH=1, the finite-eps charge is at most2eps²/a. Thus

    Delta(X+aI)>=[1-(140/9)(eps/m)]h0(a)-2eps²/a.       (3)

## Uniform baseline and closed constants

The map c/(a+c) increases with c, so the inherited scalar baseline improves
to h0(a)>=(6/35)ra m²/(a+m)², without any maximum C eigenvalue.
For a>=a0 and a0<=m, the last charge divided by this baseline is at most

    (35/3r)(eps/m)²(1+m/a)²
      <=(140/3r)(eps/a0)²<=35/(192r).

The first charge fraction is at most140/(9*2^22). Their sum is strictly
less than1/2 for all r>=1. Half the baseline survives, proving(1).

The scalar radius has O(bits(m)+2bits(ell)+log r) rational bit length.
It is256r smaller than the local positive-ray radius when ell0=ell; the
extra cost buys an ENTIRE white curve and its inherited bath lift. Matrix
reading/PSD qualification and acquiring m,ell remain required inputs.
The ell0=0/singular-leakage boundaries in PROOF.md remain unchanged.
No arbitrary-source iteration, physical implementation, global entropy
theorem, runtime advantage or priority is claimed.
